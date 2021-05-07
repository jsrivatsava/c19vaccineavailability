import requests, json, hashlib, smtplib, ssl, time
from datetime import datetime, date, timedelta
from . import mail_credentials as mc

recepient_emails, pincodes, check_hash = None, None, None 

def check_last_hexdigest(curr_hexdigest):
    global check_hash
    if not check_hash:
        check_hash = curr_hexdigest
        return True
    elif check_hash != curr_hexdigest:
        check_hash = curr_hexdigest
        return True
    else:
        return False

def send_email(mail_txt):
    global recepient_emails
    port = mc.port
    smtp_server = mc.smtp_server
    sender_email = mc.sender_email
    password = mc.password  
    subject = "CoViD Vaccine availability at " + datetime.now().strftime("%H:%M, %b %d %Y")
    message = 'Subject: {}\n\n{}'.format(subject, mail_txt)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recepient_emails, message)

def mail_recipients(vaccine_report):
    mail_txt = str()
    for vaccine in vaccine_report:
        mail_txt += '\n\n*** ' + vaccine + ' ***\n\n'
        mail_txt += '\t\t\tDOSES\t\tAGE LIMIT\tCENTER\n'
        mail_txt += '\t\t\t--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n'
        for cvc in vaccine_report[vaccine]:
            for session in cvc['sessions']:
                #mail_txt += session['date'] + ': ' + str(session['available_capacity']) + ' doses are available at ' + cvc['name'] + ' with age limit ' + str(session['min_age_limit']) + '\n'
                mail_txt += session['date'] + ':\t' + str(session['available_capacity']) + '\t\t\t' + str(session['min_age_limit']) + '+\t\t' + cvc['name'] + ' (' + cvc['address'] + ' / ' + str(cvc['pincode']) + ')\n'

    mail_txt += "\n\nBook an appointment at https://selfregistration.cowin.gov.in"

    # Calculate hash
    mail_txt_hash = hashlib.md5(bytes(mail_txt, 'utf-8'))
    curr_hexdigest = mail_txt_hash.hexdigest()    

    if(check_last_hexdigest(curr_hexdigest)):
        send_email(mail_txt)

def fix_day_month(ip_no):
    return '0' + str(ip_no) if ip_no < 10 else str(ip_no)

def prepare_report(ip_date, vaccine_report):    
    basepath = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'    
    query_date = fix_day_month(ip_date.day) + '-' + fix_day_month(ip_date.month) + '-' + str(ip_date.year)
        
    for pincode in pincodes:
        query_url = basepath + '?pincode=' + str(pincode) + '&date=' + query_date              
        req_header = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12'
        }
        res = requests.get(query_url, headers=req_header)
        
        # When the call state is 403, wait for some time and try again in next pass
        if res.status_code == 403:
            time.sleep(60)
            break
            
        res_json = res.json()        
        centers = res_json['centers']
        
        for center in centers:
            include_center = False
            cvc = {
                'name':center['name'],
                'address':center['address'],
                'pincode':center['pincode'],
                'fee_type':center['fee_type'],
                'sessions':[]
            }
            for session in center['sessions']:
                if session['available_capacity'] > 0:
                    include_center = True
                    if session['vaccine'] not in vaccine_report:
                        vaccine_report[session['vaccine']] = []

                    
                    rep_obj = {
                        'available_capacity': session['available_capacity'],
                        'min_age_limit': session['min_age_limit'],
                        'date':session['date']
                    }

                    cvc['sessions'].append(rep_obj)

            if include_center:
                vaccine_report[session['vaccine']].append(cvc)

    return vaccine_report

def execute_passes():
    td = date.today()
    pass1_report = prepare_report(date.today(), {})
    pass2_report = prepare_report(date.today() + timedelta(days=7), pass1_report)
    final_report = prepare_report(date.today() + timedelta(days=14), pass2_report)

    if final_report:
        mail_recipients(final_report)

# Execute Report Preparation
if __name__ == '__main__':
    while(True):
    
        # Load pincodes
        with open('pincodes.json') as f:
            pincodes = json.load(f)
        
        # Load Reecepient emails
        with open('recipients.json') as f:
            recepient_emails = json.load(f)

        if pincodes and recepient_emails:        
            execute_passes()

        # Wait for next check
        time.sleep(120)

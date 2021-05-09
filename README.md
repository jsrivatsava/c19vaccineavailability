# c19vaccineavailability
CoViD 19 Vaccine Tracker: Tracks vaccine availability upto 3 weeks

## Mail Credentials
Please update SMTP details in [Mail Credentials](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/mail_credentials.py)

## Run instructions
1. Update [pincodes](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/pincodes.json) with all pincodes you want to track. Eg. ["424524","534243"]
2. Update [recipient_emails](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/recipients.json) with all emails who is interested to receive report. Eg. ["abc@xyz.com","123@xyz.com"]
3. Update [vaccines](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/vaccines.json) with all vaccines (case insensitive) you'd like to track. If you leave it blank, report will track all available vaccines by default. Eg. ["Covishield","COVAXIN"]
4. Execute command `python3 cvcalerts.py` to invoke lean scheduler (2min duration)

## Runs on Android
If running an app like this all the time either in your laptop or on any cloud server is not very pocket friendly for you, then you can run this program in your android mobile using [Termux](https://play.google.com/store/apps/details?id=com.termux&hl=en_IN&gl=US)
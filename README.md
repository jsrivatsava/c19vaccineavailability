# c19vaccineavailability
CoViD 19 Vaccine Tracker: Tracks vaccine availability upto 3 weeks

## Mail Credentials
Please update SMTP details in [Mail Credentials](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/mail_credentials.py)

## Run instructions
1. Update [pincodes](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/pincodes.json) with all pincodes you want to track. Eg. ["424524","534243"]
2. Updat [recipient_emails](https://github.com/jsrivatsava/c19vaccineavailability/blob/main/recipients.json) with all emails who is interested to receive report. Eg. ["abc@xyz.com","123@xyz.com"]
3. Execute command `python3 cvcalerts.py` to invoke lean scheduler (2min duration)
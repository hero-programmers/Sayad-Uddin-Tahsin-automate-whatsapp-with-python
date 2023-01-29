import pywhatkit

phone = input("Enter the Recipient Number (include the country code). Ex. +8801*********\n>>> ")
message = input("Enter the message\n>>> ")
time = input("Enter the desired time in 24 Hours. Format: HH:MM\n>>> ")
hour, minute = time.split(":", 1)
hour = int(hour) if not str(hour).startswith("0") else int(str(hour).replace("0", "", 1))
minute = int(minute) if not str(minute).startswith("0") else int(str(minute).replace("0", "", 1))

pywhatkit.sendwhatmsg(phone_no=phone, message=message, time_hour=hour, time_min=minute, tab_close=True)

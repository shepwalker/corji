import csv
import sys

from twilio.rest import TwilioLookupsClient, TwilioRestClient


from corji.settings import Config


client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
lookup_client = TwilioLookupsClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)

def send_message_to_number(number, message, media):
    return client.messages.create(
        body = message,
        to = number,
        media_url = media,
        from_=Config.TWILIO_PHONE_NUMBER
        )

def verify_number(test_number):
    lookup_result = lookup_client.phone_numbers.get(test_number)
    return lookup_result.phone_number or None

if __name__ == "__main__":
    """
    Super nifty script to spam people using Twilio. Expects that 
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER 
    are all populated correctly.
    Takes in 4 MANDATORY arguments.  
    arg1 - path to a file filled with phone numbers (one number per line)
    arg2 - message to be sent to those phone numbers
    arg3 - url to a picture to be sent to those phone numbers
    arg4 - your personal phone numer to make sure it all works before spamming 
    tons of people.
    """
    recipient_list_file_path = sys.argv[1]
    message = sys.argv[2]
    media = sys.argv[3]
    test_number = sys.argv[4]
    with open(recipient_list_file_path, newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        if(verify_number(test_number)):
            send_message_to_number(test_number, message, media)
            input_var = input("Enter 'confirm' if message was successfully received by test number: ")
            if input_var != "confirm":
                print("Confirmation not received, exiting...")
                exit(2)
        else:
            raise AttributeError("Improper parameters!")
        for row in csvreader:
            if(verify_number(row[0])):
                message_sid = send_message_to_number(row[0], message, media)
                print("Message successfully sent to: {} with confirmation SID: {}".format(row[0], str(message_sid)) )

                




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

def verify_number(number):
	lookup_result = lookup_client.phone_numbers.get(number)
	return lookup_result.phone_number or None

if __name__ == "__main__":
	recipient_list = sys.argv[1]
	message = sys.argv[2]
	media = sys.argv[3]
	test_number = sys.argv[4]
	with open(recipient_list, newline='') as csvfile:
		csvreader = csv.reader(csvfile)
		if(verify_number(test_number)):
			send_message_to_number(test_number, message, media)
			input_var = input("Enter 'confirm' if message was successfully received by test number: ")
			if input_var != "confirm":
				print("Confirmation not received, exiting...")
				exit()
		else:
			raise AttributeError("Improper parameters!")
		for row in csvreader:
			if(verify_number(row[0])):
				message_sid = send_message_to_number(row[0], message, media)
				print("Message successfully sent to: " + row[0] + " with confirmation SID: " + str(message_sid))

				




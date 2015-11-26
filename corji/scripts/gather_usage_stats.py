import csv

from twilio.rest import TwilioRestClient

from corji.settings import Config


client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
if __name__ == "__main__":
	"""
	Expects TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID to be filled in with 
	appropriate values.
	Gathers ALL twilio message logs and dumps them itno a CSV.  
	"""
	with open("./.usage/test1.csv", "w+", newline = '') as csvfile:
		csvwriter = csv.writer(csvfile)
		for message in client.messages.iter(page_size=1000): 
			csvwriter.writerow([message.from_, message.to, message.body, message.date_sent, message.num_media, message.status, message.direction, message.error_message or ""])
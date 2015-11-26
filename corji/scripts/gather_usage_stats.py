import csv

from twilio.rest import TwilioRestClient

from corji.settings import Config


client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
if __name__ == "__main__":
	with open("./.usage/test1.csv", "w+", newline = '') as csvfile:
		csvwriter = csv.writer(csvfile)
		t = 0
		for message in client.messages.iter(page_size=1000): #Note, user .iter() in the future.
			if(t>300000):
				break
			csvwriter.writerow([message.from_, message.to, message.body, message.date_sent, message.num_media, message.status, message.direction, message.error_message or ""])
			t += 1
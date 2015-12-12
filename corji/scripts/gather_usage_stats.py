import csv
import sys

from twilio.rest import TwilioRestClient

from corji.settings import Config

PAGE_SIZE = 1000
client = TwilioRestClient(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
if __name__ == "__main__":
    """
    Expects TWILIO_AUTH_TOKEN and TWILIO_ACCOUNT_SID to be filled in with 
    appropriate values.
    Gathers ALL twilio message logs and dumps them itno a CSV.  
    Optional command line argument for target destination of CSV,
    otherwise dumps to ./.usage/usage_stats.csv
    """
    TARGET_FILE = ""
    if len(sys.argv) > 1: 
    	TARGET_FILE = sys.argv[1]
    else:
    	TARGET_FILE = "./.usage/usage_stats.csv"
    with open(TARGET_FILE, "w+", newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        for message in client.messages.iter(page_size = PAGE_SIZE): 
            csvwriter.writerow([message.sid, message.from_, message.to, message.body, message.date_sent, message.num_media, message.status, message.direction, message.error_message or ""])
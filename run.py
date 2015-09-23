# This Python file uses the following encoding: utf-8

from flask import Flask, request
import requests
import twilio.twiml
import os
import urllib.request
import emoji

app = Flask(__name__)

# TODO: make composable.
# TODO: move URL to .env variable
url = "https://spreadsheets.google.com/feeds/list/1vDkS3vwXrT4mSyI8JVHQ_Z7GGRF90GnUTbX8p0zoqNM/od6/public/values?alt=json"
payload = requests.get(url).json()
raw_data = payload['feed']['entry']
corgis = {i['gsx$emoji']['$t']: i['gsx$url']['$t'] for i in raw_data}

cacheDir = os.getenv('CORJI_CACHE_PATH', './cache')
for i in corgis:
    corgi = corgis.get(i, None)
    if not corgi:
        continue

    #emojiDir = str(i.encode('unicode_escape')).replace("\\", "").replace("'", "")
    emojiDir = emoji.demojize(i).replace(":","")
    try:
        print(emojiDir)
    except:
        #TODO: insert debugging logic so we know where we're failing to successfully demojize
        continue

    directory = cacheDir + '/' + emojiDir
    if not os.path.exists(directory):
        os.makedirs(directory)
        try:
            urllib.request.urlretrieve(corgi, directory +"/01.jpg")
        except:
            print("FAILED ON:" + emojiDir)
    

@app.route("/", methods=['GET', 'POST'])
def corgi():
    """Respond to incoming calls with a simple text message."""

    emoji = request.values.get("Body") or ""

    print(emoji)
    print(len(corgis.keys()))
    corgi = corgis.get(emoji, None)

    message = ""
    if not corgi:
        message = "No corgi :("

    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        if corgi:
            m.media(corgi)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

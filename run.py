# This Python file uses the following encoding: utf-8

from flask import Flask, request, send_from_directory, abort
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

cache_dir = os.getenv('CORJI_CACHE_PATH', './cache')

for i in corgis:
    corgi = corgis.get(i, None)
    if not corgi:
        continue

    emoji_dir = emoji.demojize(i).replace(":", "")
    try:
        print(emoji_dir)
    except:
        # TODO: insert debugging logic so we know where we're failing to
        # successfully demojize
        continue

    directory = cache_dir + '/' + emoji_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
        try:
            urllib.request.urlretrieve(corgi, directory + "/01.jpg")
        except:
            print("FAILED ON:" + emoji_dir)


@app.route("/emoji/<path:file_name>", methods=['GET'])
def get_image(file_name):
    print(file_name)
    full_file_name = cache_dir+"/"+file_name
    split_name = file_name.split('/')
    if(os.path.exists(full_file_name)):
        return send_from_directory(cache_dir + "/"+split_name[0], split_name[1])
    else:
        abort(404)


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

    possible_corji_dir = emoji_dir + "/" + emoji.demojize(i).replace(":", "")

    if(os.path.exists(possible_corji_dir + "/01.jpg"))
        corgi = os.path.exists(possible_corji_dir + "/01.jpg"

    resp=twilio.twiml.Response()
    with resp.message(message) as m:
        if corgi:
            m.media(corgi)
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

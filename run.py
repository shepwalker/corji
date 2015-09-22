# This Python file uses the following encoding: utf-8

from flask import Flask, request
import requests
import twilio.twiml

app = Flask(__name__)

corgis = {}


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    emoji = request.values.get("Body") or ""

    corgi = corgis.get("👃", None)

    message = ""
    if not corgi:
        message = "No corgi :("

    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        if corgi:
            m.media(corgi)
    return str(resp)


if __name__ == "__main__":
    sheetsu_url = "https://spreadsheets.google.com/feeds/list/1vDkS3vwXrT4mSyI8JVHQ_Z7GGRF90GnUTbX8p0zoqNM/od6/public/values?alt=json"
    payload = requests.get(sheetsu_url).json()
    raw_data = payload['feed']['entry']
    corgis = {i['gsx$emoji']['$t']: i['gsx$url']['$t'] for i in raw_data}
    app.run(debug=True)


# alt ice cream http://www.google.com/imgres?imgurl=http://happyfeminist.typepad.com/happyfeminist/images/img_1244_1.jpg&imgrefurl=http://happyfeminist.typepad.com/happyfeminist/corgis_and_collies_and_scotties_oh_my/&h=450&w=600&tbnid=w8bKiJRn79Bz-M:&docid=QbmFgEsH-ih0FM&ei=16D_VcTaD4LRoATumr-IDA&tbm=isch&ved=0CDUQMygPMA9qFQoTCISi8p-9h8gCFYIoiAodbs0PwQ

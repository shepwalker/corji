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
    encoded_emoji = unicode(emoji, "utf-8")

    corgi = corgis.get(encoded_emoji, None)

    message = ""
    if not corgi:
        message = "No corgi :("

    resp = twilio.twiml.Response()
    with resp.message(message) as m:
        if corgi:
            m.media(corgi)
    return str(resp)


if __name__ == "__main__":
    sheetsu_url = "http://sheetsu.com/apis/23efc212"
    payload = requests.get(sheetsu_url).json()
    raw_data = payload['result']
    corgis = {i['emoji']: i['url'] for i in raw_data}
    app.run(debug=True)


# alt ice cream http://www.google.com/imgres?imgurl=http://happyfeminist.typepad.com/happyfeminist/images/img_1244_1.jpg&imgrefurl=http://happyfeminist.typepad.com/happyfeminist/corgis_and_collies_and_scotties_oh_my/&h=450&w=600&tbnid=w8bKiJRn79Bz-M:&docid=QbmFgEsH-ih0FM&ei=16D_VcTaD4LRoATumr-IDA&tbm=isch&ved=0CDUQMygPMA9qFQoTCISi8p-9h8gCFYIoiAodbs0PwQ

# This Python file uses the following encoding: utf-8

from flask import Flask, request
import twilio.twiml

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming calls with a simple text message."""

    body = request.values.get("Body")

    corgis = {
        "🍁": "https://s-media-cache-ak0.pinimg.com/736x/ef/94/21/ef9421da2b6da030dca07a3a5fa48107.jpg",
        "🏀": "https://s-media-cache-ak0.pinimg.com/236x/6b/bf/37/6bbf3751b876a4dbdf73ff3f6ac3d3e2.jpg",
        "⚽️": "https://s-media-cache-ak0.pinimg.com/236x/d4/60/f0/d460f0a6937afa805f134ae677d617fe.jpg",
        "😇": "https://s-media-cache-ak0.pinimg.com/736x/8c/eb/80/8ceb803530a236f9195bcf3b46a68793.jpg",
        "🍻": "http://4.bp.blogspot.com/-ArbPqi52e_w/UCQp-d48yVI/AAAAAAAAAJA/BQINPm8Mj_8/s1600/beer.png",
        "🌈": "http://1.bp.blogspot.com/-b2n0g39iiI8/T8JbyMeSyBI/AAAAAAAAAZQ/9L7K_cGcshE/s1600/corgi+funny+_8.jpg",
        "😎": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcTOHllIRRtOXNV0ulv82ku06xuhCrre4zE3QfTIovadWfTEOzY",
        "😈": "https://s-media-cache-ak0.pinimg.com/236x/96/72/c6/9672c637cf665aed51dc6e24106de95e.jpg",
        "😪": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQSpAh3lGdtAv85qjoWViDoQqEfXm4zeEehG7CaJglpp0ASBzjqwg",
        "🐳": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTgOtVCOxMlkQBvOdSmTiFR0KR-kGEZFkdJ38l9JVN0TES8SfFTPQ",
        "📪": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcR3B91Arcb_8s74f8pWH-2Mv9Ov2O8_LeRyX8S80MGNqsFY2A2Wqw",
        "📫": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcR3B91Arcb_8s74f8pWH-2Mv9Ov2O8_LeRyX8S80MGNqsFY2A2Wqw",
        "📬": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcR3B91Arcb_8s74f8pWH-2Mv9Ov2O8_LeRyX8S80MGNqsFY2A2Wqw",
        "📭": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcR3B91Arcb_8s74f8pWH-2Mv9Ov2O8_LeRyX8S80MGNqsFY2A2Wqw",
        "🍷": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRiZ3JWMGUx0j6zziqdPKcotI3W7XdatLFvWRKHsO3iPLRTeoJQ",
        "👑": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcR3fahn145p4cOILMdLYnOy42TAYbKIaBkSo_y0TpV4jwLO7YdF",
        "👸": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcR3fahn145p4cOILMdLYnOy42TAYbKIaBkSo_y0TpV4jwLO7YdF",
        "🎩": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRxqQWFEuZnDkM9nRqVksL8coXBFPygo7Z_Bxf1WQyov95P10HDTg",
        "🐸": "http://cache1.asset-cache.net/gc/535206753-corgi-in-frog-oufit-gettyimages.jpg?v=1&c=IWSAsset&k=2&d=Ezy53KzByHOX7H2Kk%2FU%2BjHkINpFPU59iELHj13yz3llwZEYqf8KZOsBzReYnQ0kQ",
        "😧": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcT-NJwj9SKMq2eg-K8alDFvkGBNv9te9SB1pX8qplA55nYf3wMi",
        "🐴": "http://poolhouse.s3.amazonaws.com/blog-assets-two/2015/03/corgihorse.jpg",
        "🐎": "http://25.media.tumblr.com/tumblr_m1atc5Ecuv1r3qnbmo1_1280.jpg",
        "🍦": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcTR4go0E-aDmoUjMy7rQPAs-kc2aUqUCLm7rIe2-pxKyw6QZhg3",
        "🚥": "https://s-media-cache-ak0.pinimg.com/736x/af/88/22/af88222990bf031b3334057f094141d6.jpg",
        "🚦": "https://s-media-cache-ak0.pinimg.com/736x/af/88/22/af88222990bf031b3334057f094141d6.jpg",
        "😐": "https://wordsofwisdomfromthemanwholivesalone.files.wordpress.com/2012/07/happy-corgi.jpg",
        "💩": "http://33.media.tumblr.com/tumblr_lxvqlbrIAd1qzrlhgo1_400.gif",
        "🐢": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcRqFkp62uBtwZkyHwdEXOg9KbZsOK_7zP1IkgaFGi_G9jAcX7Kv"
    }
    corgi = corgis.get(body, None)
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

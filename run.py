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
        "😱": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcT-NJwj9SKMq2eg-K8alDFvkGBNv9te9SB1pX8qplA55nYf3wMi",
        "🐴": "http://poolhouse.s3.amazonaws.com/blog-assets-two/2015/03/corgihorse.jpg",
        "🐎": "http://25.media.tumblr.com/tumblr_m1atc5Ecuv1r3qnbmo1_1280.jpg",
        "🍦": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcTR4go0E-aDmoUjMy7rQPAs-kc2aUqUCLm7rIe2-pxKyw6QZhg3",
        "🚥": "https://s-media-cache-ak0.pinimg.com/736x/af/88/22/af88222990bf031b3334057f094141d6.jpg",
        "🚦": "https://s-media-cache-ak0.pinimg.com/736x/af/88/22/af88222990bf031b3334057f094141d6.jpg",
        "😐": "https://wordsofwisdomfromthemanwholivesalone.files.wordpress.com/2012/07/happy-corgi.jpg",
        "💩": "http://33.media.tumblr.com/tumblr_lxvqlbrIAd1qzrlhgo1_400.gif",
        "🐢": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcRqFkp62uBtwZkyHwdEXOg9KbZsOK_7zP1IkgaFGi_G9jAcX7Kv",
        "🎅": "http://api.ning.com/files/pG8qvUF5OwBCc1AI4s-Quwk4qvRV2zsCPC2QvRp-WnIiFFSP6wniu-5sxt6pVCMBcyFWFnXwxl7ZKzM7Xok*6ty3lIBdA3AM/SantaReindeer_v1.jpg",
        "👙": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRF9mTQtoHC7Rv2L8mYVKpECnqHOiwWTrKBJG82mCbvmeYzd7DC",
        "🌵": "http://1.bp.blogspot.com/-xNoys4tXN64/UWUizovxVjI/AAAAAAAACaE/u6rp1hZY_a4/s1600/cactuscorgie_BD.jpg",
        "😠": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSWkWV1nZbO3BSE0xid--k41vCwY-2MCOoNtggS0Sp5LHlqN9LRhg",
        "🍜": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcTBLHfexrtqNvcZTdVxQuP-o-tx5qOt_CMh6mobzi75s9a1ucD6",
        "🎃": "http://i.huffpost.com/gen/2150196/images/o-CORGI-facebook.jpg",
        "👼": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRMjbTDXEyOHnxiMSZ5vGogX1B6ThTLPwQLqIliJSofOQ9ftGXUzQ",
        "🎹": "http://img.ifcdn.com/images/923e062a80977d7a388ab4e354f9d70ef4d7df63485b7def23c12ac9c1128ee9_1.gif",
        "⛵️": "https://s-media-cache-ak0.pinimg.com/736x/81/4a/5b/814a5b4fc0df5c43fdda8899ed7f3a6c.jpg",
        "👔": "https://secure.static.tumblr.com/1687a491d59689834536edd549fea8f9/ctpb9fo/gDsn12kik/tumblr_static_buisnesscorgi.jpg",
        "💊": "https://s-media-cache-ak0.pinimg.com/736x/6c/4a/b1/6c4ab17ec84f251a78fa5c421d20d5fa.jpg",
        "😷": "http://www.dogster.com/wp-content/uploads/2015/05/9af45e667b469121fcae1ec29f215d96.jpg",
        "😛": "http://cdn.dailycute.net/2013/8/22/18cf382b38ce32f7765ac3f1fc36bff1.jpg",
        "😏": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcRTN0NLbojXcn8bEaVuQ4-971TL7cGtpKFBMmXSTiX4hBRzrOJ_",
        "👅": "http://41.media.tumblr.com/tumblr_lm6nmaz2DA1qbwakso1_500.jpg",
        "🛀": "https://encrypted-tbn3.gstatic.com/images?q=tbn%3AANd9GcQfrKFHWxbDwdzRiSqSqqmUFn-0piyvUQmjjmAiB9MphJazxXid8w",
        "🛁": "https://s-media-cache-ak0.pinimg.com/236x/2d/0c/01/2d0c0147d006cc2418ff818c5c326599.jpg",
        "🍔": "http://33.media.tumblr.com/tumblr_ljk8ycyY7F1qbidbp.jpg",
        "": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcTxVMmf3lvGecWqbmkOillsfKWt8gkWVBqv8xZJcizLt6h4Ym1l",
        "🐝": "http://36.media.tumblr.com/tumblr_lyfjdjuJox1qzjmtno1_500.jpg",
        "🍓": "https://s-media-cache-ak0.pinimg.com/236x/e7/1c/e2/e71ce2c117779f644e5d4b8e76dc98cf.jpg",
        "🍌": "https://s-media-cache-ak0.pinimg.com/736x/bd/87/5b/bd875bb1d4f120f5e60ea676642a7167.jpg",
        "🏂": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcQ0SsW_C8Wv_3jlM54hb4mcyl-M1v_fbdsOhSW19YQe2buG8U4Saw",
        "🚒": "http://www.mybs.com/wp-content/uploads/2013/03/tumblr_mc9c68cM1d1qbwakso1_500.jpg",
        "💎": "http://img.whenwomentalks.com/2014/07/01/ydlbfc.jpg",
        "🍞": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcRFvors_GWLBJNj3cxdgqQMzakufUtjK4zjotQrMRIRJFJBbZlxQg",
        "☕️": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcQg24UN_ZaCicByRbw5VaTl9erVgDP3G4NnS8qFCAI1w7-Z5kcufg",
        "🍂": "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSgNt2JfpwMF5lsVUkfwTwuuBMVZCH_1axZw4KV9g6oO3xPP7s0ug",
        "🍀": "http://www.theirishstore.com/blog/wp-content/uploads/2014/09/irish-dog-costume.jpg",
        "🐞": "https://randyscorgistories.files.wordpress.com/2013/09/ladybugcorgi02.jpg",
        "🙌": "https://encrypted-tbn1.gstatic.com/images?q=tbn%3AANd9GcRCDjPr8OGgSC7Cb6W69lvKdWXFLNw0T3KiHq2w9htNYsct0yA6DA",
        "🙏": "https://s-media-cache-ak0.pinimg.com/236x/72/08/bd/7208bdf96f2e327f83efaf5b3c3e654b.jpg",
        "💸": "https://randyscorgistories.files.wordpress.com/2013/08/money-corgi.jpg",
        "🎁": "http://www.alisonjackson.com/wp-content/uploads/pippa-christmas6.jpg",
        "🎀": "https://s-media-cache-ak0.pinimg.com/236x/8e/aa/8a/8eaa8a3e0e3012fa90f910a6ce14ac99.jpg",
        "🎣": "https://s-media-cache-ak0.pinimg.com/236x/f8/e2/3b/f8e23b77f3fe683024d3091bdc5ee08c.jpg",
        "❄️": "http://barkpost.com/wp-content/uploads/2014/01/cori.jpg",
        "😧": "https://encrypted-tbn2.gstatic.com/images?q=tbn%3AANd9GcTloV67lCnK3G1-oxs7b51UlrJhS2ufvaggBJD3wlxpsDW62hue1A",
        "👨‍❤️‍👨": "https://s-media-cache-ak0.pinimg.com/236x/b4/3b/5f/b43b5f508f251bfa591796e731bee5e0.jpg",
        "🌹": "http://www.blogcdn.com/travel.aol.co.uk/media/2013/02/corgi.jpg",
        "🍕": "http://41.media.tumblr.com/tumblr_m97vn82Te91rcxvfjo1_540.jpg"
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


# alt ice cream http://www.google.com/imgres?imgurl=http://happyfeminist.typepad.com/happyfeminist/images/img_1244_1.jpg&imgrefurl=http://happyfeminist.typepad.com/happyfeminist/corgis_and_collies_and_scotties_oh_my/&h=450&w=600&tbnid=w8bKiJRn79Bz-M:&docid=QbmFgEsH-ih0FM&ei=16D_VcTaD4LRoATumr-IDA&tbm=isch&ved=0CDUQMygPMA9qFQoTCISi8p-9h8gCFYIoiAodbs0PwQ

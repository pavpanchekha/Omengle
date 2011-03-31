import urllib
import json

KEY = "AIzaSyAOwKRQu-HHuSFso_Zz3qfyyzC5C_g7BxI"
URL = "https://www.googleapis.com/language/translate/v2"

class TranslateError(Exception): pass

def translate(s, sourcelang="en", targetlang="en"):
    if sourcelang == targetlang: return s

    request_url = URL + "?" + urllib.urlencode({"q": s, "key": KEY, "source": sourcelang, "target": targetlang})

    data = urllib.urlopen(request_url)
    body = data.read()

    if data.getcode() != 200:
        raise TranslateError("{code}: {msg}".format(code=data.getcode(), msg=body))
    else:
        out = json.loads(body)
        return out["data"]["translations"][0]["translatedText"]

def detect_language(s):
    request_url = URL + "?" + urllib.urlencode({"q": s, "key": KEY, "target": "en"})
    data = urllib.urlopen(request_url)
    out = json.loads(data.read())

    if data.getCode():
        raise TranslateError("{code}: {msg}".format(code=data.getCode(), msg=out))
    else:
        return out["data"]["translations"][0]["detectedSourceLanguage"]


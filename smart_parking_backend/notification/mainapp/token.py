import jwt
from datetime import datetime

key = "56q`uyNxe}dNG|b(.+R7/00|i{cN:A"


def token_encode(payload):
    datetime_string = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    payload.update({"datetime": datetime_string})
    encoded = jwt.encode({'payload': payload}, key, algorithm='HS256')
    return encoded


def decode(encoded):
    print("referenced 1")
    try:
        decoded = jwt.decode(encoded, key, algorithms='HS256')
        return decoded
    except Exception as e:
        print(e)




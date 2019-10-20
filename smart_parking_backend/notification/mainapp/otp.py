import http.client


trial_message = "Use 3456 as your one time password which will be valid for next 5 minutes."

trial_message_1 = "Hey {} {} "


def otpsender(otp, message, mobile, expiry):
    conn = http.client.HTTPSConnection("control.msg91.com")
    payload = ""
    message = "%20".join(message.split())
    uri = "/api/sendotp.php?otp_length=5&otp_expiry={}&sender=QWERTY&message={}&mobile={}&authkey=294458AY1uO4Rgtjz5d8077e2&otp={}".format(
        expiry, message, mobile, otp)
    print(uri)
    conn.request("POST", uri, payload)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return data.decode("utf-8")


def otpverify(mobile, otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    payload = ""

    headers = {'content-type': "application/x-www-form-urlencoded"}

    conn.request(
        "POST", "/api/verifyRequestOTP.php?authkey=294458AY1uO4Rgtjz5d8077e2&mobile={}&otp={}".format(mobile, otp), payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return data.decode("utf-8")


def bulk_message(payload_data, message):
    conn = http.client.HTTPSConnection("api.msg91.com")
    common_part = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ "
    sub_payload_1 = '{ \"message\": \"'
    sub_payload_2 = '\", \"to\": [ \"'
    sub_payload_3 = '\"] }'
    print(payload_data.values())
    for i in payload_data:
        individual_message = trial_message_1.format(i.first_name, i.last_name) + message
        print(individual_message)
        phone = i.user.mobile
        common_part = common_part + sub_payload_1 + individual_message + sub_payload_2 + str(phone) + sub_payload_3
        common_part += ", "
    common_part = common_part[:-2]
    common_part += " ] }"
    print("This part is ", common_part, "ends here")

    #payload = "{ \"sender\": \"SOCKET\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\": \"Message1\", \"to\": [ \"7980674536\", \"98261XXXXX\" ] }, { \"message\": \"Message2\", \"to\": [ \"98260XXXXX\", \"98261XXXXX\" ] } ] }"

    headers = {
        'authkey': "294458AY1uO4Rgtjz5d8077e2",
        'content-type': "application/json"
    }

    conn.request("POST", "/api/v2/sendsms?country=91", common_part, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    return data.decode("utf-8")

# ToDo : No auth right now
# ToDo : Restrict user signup based on number
# ToDo : Change status name in models - Done
# ToDo : Document on swagger

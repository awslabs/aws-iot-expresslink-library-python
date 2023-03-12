import time
import datetime
import json
from aws_iot_expresslink import ExpressLink

el = ExpressLink(port="/dev/tty.usbserial-14440")

if not el.onboarded:
    el.config.SSID = "MyHomeWiFi"
    el.config.Passphrase = "super!secret"
    el.config.Endpoint = "abcd1234-ats.iot.some-region.amazonaws.com"
    el.reset()

el.connect()
el.config.set_topic(1, "hello/world")

while True:
    j = {
        "time": datetime.datetime.now().isoformat(),
        "message": "Hello World!",
    }
    el.publish(topic_index=1, message=json.dumps(j))
    time.sleep(5)

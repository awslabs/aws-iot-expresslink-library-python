import time
import json
from machine import Pin
from aws_iot_expresslink import ExpressLink

el = ExpressLink(
    uart_id=0,
    rx=Pin(1),
    tx=Pin(0),
    event_pin=Pin(10),
    wake_pin=Pin(11),
    reset_pin=Pin(12),
)

el.connect()
el.config.set_topic(1, "hello/world")

while True:
    j = {
        "message": f"Hello World from {el.config.ThingName}!",
    }
    el.publish(topic_index=1, message=json.dumps(j))
    time.sleep(5)

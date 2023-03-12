import time
import json
import board
from aws_iot_expresslink import ExpressLink

el = ExpressLink(rx=board.RX, tx=board.TX)

el.connect()
el.config.set_topic(1, "hello/world")

while True:
    j = {
        "message": f"Hello World from {el.config.ThingName}!",
    }
    el.publish(topic_index=1, message=json.dumps(j))
    time.sleep(5)

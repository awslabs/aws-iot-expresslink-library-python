import time
import json
import busio
import board
import adafruit_sht31d
from aws_iot_expresslink import ExpressLink

el = ExpressLink(
    rx=board.RX,
    tx=board.TX,
    event_pin=board.GP10,
    wake_pin=board.GP11,
    reset_pin=board.GP12,
)

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

el.connect()
el.config.set_topic(1, "wind_turbine/telemetry")

while True:
    j = {
        "temperature": sensor.temperature,
        "humidity": sensor.relative_humidity,
    }
    el.publish(topic_index=1, message=json.dumps(j))
    time.sleep(5)

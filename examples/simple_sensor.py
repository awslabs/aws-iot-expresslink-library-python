import time
import json
import busio
import board
import adafruit_sht31d
from aws_iot_expresslink import ExpressLink

uart = busio.UART(board.TX, board.RX, receiver_buffer_size=4096)
el = ExpressLink(uart, board.GP10, board.GP11, board.GP12)

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_sht31d.SHT31D(i2c)

el.config.set_topic(1, "wind_turbine/telemetry")
el.connect()

while True:
    j = {
        "temperature": sensor.temperature,
        "humidity": sensor.relative_humidity,
    }
    el.send(1, json.dumps(j))
    time.sleep(5)

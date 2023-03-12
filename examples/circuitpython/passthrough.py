import board
from aws_iot_expresslink import ExpressLink

el = ExpressLink(rx=board.RX, tx=board.TX)
el.passthrough()
# ... and follow the instructions printed to the serial console!

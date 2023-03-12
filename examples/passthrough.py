import busio
import board
from aws_iot_expresslink import ExpressLink

uart = busio.UART(board.GP1, board.GP0, receiver_buffer_size=4096)
el = ExpressLink(uart, board.GP10, board.GP11, board.GP12)
el.passthrough()
# ... and follow the instructions printed to the serial console!

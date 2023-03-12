import board
from aws_iot_expresslink import ExpressLink, Event

el = ExpressLink(
    tx=board.TX,
    rx=board.RX,
    event_pin=board.GP10,
    wake_pin=board.GP11,
    reset_pin=board.GP12,
)

el.connect()
el.subscribe(1, "hello/world")

while True:
    event_id, parameter, mnemonic, detail = el.get_event()
    if event_id == Event.MSG:
        topic_name, message = el.get_message(parameter)
        if topic_name and message:
            print("New message received:", message)
    elif event_id is not None:
        print(
            f"Ignoring unhandled event: {event_id=}, {parameter=}, {mnemonic=}, {detail=}"
        )

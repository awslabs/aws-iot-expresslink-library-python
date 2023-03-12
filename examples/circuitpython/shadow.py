import json
import board
from aws_iot_expresslink import ExpressLink, Event


def handle_shadow_doc(line):
    if line.startswith("1 "):
        line = line[2:]
    elif line.startswith("0 "):
        print("Shadow doc rejected:", line)
        return

    state = json.loads(line)["state"]
    if "desired" in state:
        # first: handle delta updates and unfinished desired
        handle_desired_shadow_state(state["desired"])
    elif "reported" in state:
        # second: handle initial shadow doc from previous reported
        handle_desired_shadow_state(state["reported"])
    else:
        handle_desired_shadow_state(state)


def handle_desired_shadow_state(desired_state):
    payload = {}
    payload["state"] = {}
    payload["state"]["desired"] = {}
    payload["state"]["reported"] = {}

    # Iterate over all desired state keys and update the Demo Badge components accordingly
    for k, v in desired_state.items():
        if k == "display_brightness":
            b = float(v)
            print(f"Pretend to set display_brightness to {b}%... done.")
            payload["state"]["desired"][k] = None
            payload["state"]["reported"][k] = b

    el.shadow_update(json.dumps(payload))


el = ExpressLink(
    tx=board.TX,
    rx=board.RX,
    event_pin=board.GP10,
    wake_pin=board.GP11,
    reset_pin=board.GP12,
)

el.connect()
el.config.enable_shadow = True
el.shadow_init()
el.shadow_doc()
el.shadow_subscribe()

while True:
    if el.event_signal.value:
        event_id, parameter, mnemonic, detail = el.get_event()
        if event_id == Event.SHADOW_DOC:
            # process the initial shadow document after booting up
            success, line, err = el.shadow_get_doc()
            handle_shadow_doc(line)
        elif event_id == Event.SHADOW_DELTA:
            # process incoming shadow document delta updates
            success, line, err = el.shadow_get_delta()
            handle_shadow_doc(line)
        elif event_id == Event.SHADOW_UPDATE:
            # shadow document was updated (maybe unsucessful)
            success, line, err = el.shadow_get_update()
            if success and line.startswith("0"):
                print("Shadow update was rejected:", line)
        elif event_id is not None:
            print(f"Ignoring event: {event_id} {parameter} {mnemonic} {detail}")

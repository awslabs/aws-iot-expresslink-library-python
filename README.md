# AWS IoT ExpressLink - Python library

This project is a library to interface with AWS IoT ExpressLink modules with Linux/macOS/Windows devices running [Python](https://www.python.org/downloads/) or microcontrollers running [CircuitPython](https://circuitpython.org/) and [MicroPython](https://micropython.org/). It uses AT commands and provides a thin Python wrapper for parsing and integrating into your Python-based projects.

It currently follows and implements the AWS IoT ExpressLink [Technical Specification v1.1](https://docs.aws.amazon.com/iot-expresslink/latest/programmersguide/elpg-history.html). You can find the full programmer's guide and [further documentation here](https://docs.aws.amazon.com/iot-expresslink/index.html).

Tested and built for Python 3.7+ using [pySerial](https://pyserial.readthedocs.io/) on Linux/macOS/Windows, [CircuitPython 7](https://circuitpython.org/), and [MicroPython 1.19](https://micropython.org/) on compatible microcontrollers.

## Related libraries and resources

If you are using the Arduino framework, you can use the [awslabs/aws-iot-expresslink-library-arduino](https://github.com/awslabs/aws-iot-expresslink-library-arduino) library for C++.

For additional resources, tutorials, workshops, and videos, please see the [aws/iot-expresslink](https://github.com/aws/iot-expresslink) repository.

## Dependencies

On Python using Linux/macOS/Windows, you need [pySerial](https://pyserial.readthedocs.io/) to access the UART serial interface.

On CircuitPython, there are no hard dependencies apart from the built-in modules.

On MicroPython, there are no hard dependencies apart from the built-in modules.

## Installation

On Python using Linux/macOS/Windows, download and copy the `aws_iot_expresslink.py` file from this repository into your project or package folder. You can also install it as pip package using `pip install git+https://github.com/awslabs/aws-iot-expresslink-library-python.git`

On CircuitPython, download and copy the `aws_iot_expresslink.py` file from this repository into your `CIRCUITPY/lib/` folder.

On MicroPython, download and copy the `aws_iot_expresslink.py` file from this repository into your `/pyboard/` folder using [rshell](https://github.com/dhylands/rshell).

## Documentation

See the auto-generated [API documentation](https://awslabs.github.io/aws-iot-expresslink-library-python). This documentation can also be generated locally using [pdoc](https://pdoc.dev/): `pip install pdoc && pdoc aws_iot_expresslink.py`

See the `examples/` folder in this repository for full examples.

## Usage

First, import the library:

```python
import board
from aws_iot_expresslink import ExpressLink
```

Second, create the `ExpressLink` object and pass necessary signal pins:

```python
el = ExpressLink(port='/dev/tty.usbserial-14440') # pySerial on Linux
el = ExpressLink(rx=board.RX, tx=board.TX) # CircuitPython
el = ExpressLink(rx=Pin(1), tx=Pin(0)) # MicroPython
```

Third, use the methods to interact with the AWS IoT ExpressLink module using the AT commands:

```python
el.connect()
el.config.set_topic(1, "hello/world")
el.publish(1, "Hello from your device using AWS IoT ExpressLink!")
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

import pytest

from aws_iot_expresslink import ExpressLink


class MockUART:
    def __init__(self, commands, responses):
        self.commands = [c.encode() for c in commands]
        self.responses = [r.encode() for r in responses]

        self.baudrate = 0
        self.timeout = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        assert len(self.commands) == 0
        assert len(self.responses) == 0

    def __repr__(self) -> str:
        return f"MockUART {self.commands=} {self.responses=}"

    def write(self, payload):
        assert payload == self.commands.pop(0)

    def readline(self):
        return self.responses.pop(0)

    def reset_input_buffer(self):
        pass


@pytest.mark.parametrize("line_ending", ["\n", "\r\n"])
def test_self_test(line_ending):
    with MockUART(commands=["AT\n", "AT\r\n"], responses=["OK" + line_ending]) as uart:
        xl = ExpressLink(uart)  # also calls self_test() once
        xl.self_test()  # call a second time with different line ending


@pytest.mark.parametrize(
    "line_ending", ["\n", "\r\n"]
)  # this test covers enough code paths relevant for line ending checks
def test_config_get_endpoint(line_ending):
    with MockUART(
        commands=["AT\r\n", "AT+CONF? Endpoint\r\n"],
        responses=["OK" + line_ending, "OK foobar.example.com" + line_ending],
    ) as uart:
        xl = ExpressLink(uart)
        assert xl.config.Endpoint == "foobar.example.com"


def test_config_set_endpoint():
    with MockUART(
        commands=["AT\r\n", "AT+CONF Endpoint=foobar.example.com\r\n"],
        responses=["OK\r\n", "OK\r\n"],
    ) as uart:
        xl = ExpressLink(uart)
        xl.config.Endpoint = "foobar.example.com"


@pytest.mark.parametrize("connected", [True, False])
def test_connected(connected):
    s = "1" if connected else "0"
    with MockUART(
        commands=["AT\r\n", "AT+CONNECT?\r\n"],
        responses=["OK\r\n", f"OK {s} 0 foo bar\r\n"],
    ) as uart:
        xl = ExpressLink(uart)
        assert xl.connected == connected


@pytest.mark.parametrize("onboarded", [True, False])
def test_onboarded(onboarded):
    s = "1" if onboarded else "0"
    with MockUART(
        commands=["AT\r\n", "AT+CONNECT?\r\n"],
        responses=["OK\r\n", f"OK 0 {s} foo bar\r\n"],
    ) as uart:
        xl = ExpressLink(uart)
        assert xl.onboarded == onboarded


def test_connect():
    with MockUART(
        commands=["AT\r\n", "AT+CONNECT\r\n"], responses=["OK\r\n", "OK CONNECTED\r\n"]
    ) as uart:
        xl = ExpressLink(uart)
        assert xl.connect() == (True, "CONNECTED", None)


def test_escaping():
    with MockUART(
        commands=["AT\r\n", "AT+SEND1 foo\\Abar\\Dsome\\\\thing\r\n"],
        responses=["OK\r\n", "OK\r\n"],
    ) as uart:
        xl = ExpressLink(uart)
        assert xl.publish(topic_index=1, message="foo\nbar\rsome\\thing")


def test_unescaping():
    with MockUART(
        commands=["AT\r\n", "AT+CONF Topic1=test\r\n", "AT+GET1\r\n"],
        responses=["OK\r\n", "OK\r\n", "OK foo\\Abar\\Dsome\\\\thing\r\n"],
    ) as uart:
        xl = ExpressLink(uart)
        xl.config.set_topic(1, "test")
        assert xl.get_message(topic_index=1) == ("test", "foo\nbar\rsome\\thing")

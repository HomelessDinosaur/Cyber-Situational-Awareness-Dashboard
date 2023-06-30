from dataclasses import dataclass
from datetime import datetime
import pytest
from .main import PyShark


@dataclass
class FakeIP:
    src: str
    dst: str


@dataclass
class FakeProtocol:
    srcport: int
    dstport: int


@dataclass
class FakePacket:
    ip: FakeIP
    sniff_time: str
    transport_layer: str
    tcp: FakeProtocol

    def __getitem__(self, index):
        return {
            "ip": self.ip,
            "sniff_time": self.sniff_time,
            "transport_layer": self.transport_layer,
            "tcp": self.tcp,
        }[index]


def test_process_successful_packet():
    PyShark.process_packet(
        FakePacket(
            FakeIP("192.168.1.1", "192.168.1.5"),
            datetime.now(),
            "tcp",
            FakeProtocol(80, 80),
        )
    )


def test_process_successful_src_integer():
    PyShark.process_packet(
        FakePacket(
            FakeIP(250100, "192.168.1.5"),
            datetime.now(),
            "tcp",
            FakeProtocol(80, 80),
        )
    )


def test_process_successful_dst_integer():
    PyShark.process_packet(
        FakePacket(
            FakeIP("192.168.1.1", 250106),
            datetime.now(),
            "tcp",
            FakeProtocol(80, 80),
        )
    )


def test_process_invalid_timestamp():
    with pytest.raises(Exception):
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                20,
                "tcp",
                FakeProtocol(80, 80),
            )
        )


def test_process_invalid_protocol():
    with pytest.raises(Exception):
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                datetime.now(),
                80,
                FakeProtocol(80, 80),
            )
        )


def test_process_invalid_src_port():
    with pytest.raises(Exception):
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                datetime.now(),
                "tcp",
                FakeProtocol(-80, 80),
            )
        )
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                datetime.now(),
                "tcp",
                FakeProtocol("invalid", 80),
            )
        )


def test_process_invalid_dst_port():
    with pytest.raises(Exception):
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                datetime.now(),
                "tcp",
                FakeProtocol(80, -80),
            )
        )
        PyShark.process_packet(
            FakePacket(
                FakeIP("192.168.1.1", "192.168.1.5"),
                datetime.now(),
                "tcp",
                FakeProtocol(80, "invalid"),
            )
        )

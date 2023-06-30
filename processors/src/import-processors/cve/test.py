from dataclasses import dataclass
from datetime import datetime
import pytest
from .main import CVEProcessor


class FakeDescriptionData:
    value: str

    def __init__(self, val) -> None:
        self.value = val

    @property
    def description_data(self):
        return [self]


class FakeCVEData:
    val: str

    def __init__(self, val) -> None:
        self.val = val

    @property
    def description(self):
        return FakeDescriptionData(self.val)


@dataclass
class FakeCSV:
    id: str
    url: str
    v3score: int
    cve: FakeCVEData


def test_successful_cve():
    CVEProcessor.process_cve(
        FakeCSV("1", "https://test.com", 10, FakeCVEData("description"))
    )


def test_number_id():
    CVEProcessor.process_cve(
        FakeCSV(0, "https://test.com", 10, FakeCVEData("description"))
    )


def test_no_url():
    CVEProcessor.process_cve(
        FakeCSV("1", None, 10, FakeCVEData("description"))
    )


def test_invalid_description():
    with pytest.raises(Exception):
        CVEProcessor.process_cve(FakeCSV(0, "https://test.com", 10, None))

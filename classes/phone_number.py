from dataclasses import dataclass
from datetime import datetime


@dataclass
class PhoneEvent:
    date: datetime
    to: str
    from_: str
    size: str
    type_: str


class Phone:
    def __init__(self, number="000-000-0000"):
        self.number = number
        self.log = []

    def __getitem__(self, item):
        return getattr(self, item, "")

    def __repr__(self):
        return self.number

    def _add_to_log(self, datetime, to_, from_, size, type_):
        self.log.append(PhoneEvent(datetime, to_, from_, size, type_))

    def make_call(self, outbound_number, date, duration="10 minutes"):
        self._add_to_log(date, outbound_number, self.number, duration, "Outbound Call")
        outbound_number._add_to_log(
            date, self.number, outbound_number, duration, "Inbound Call"
        )

    def send_text(self, outbound_number, date, size="100 characters"):
        self._add_to_log(date, outbound_number, self.number, size, "Sent Text")
        outbound_number._add_to_log(
            date, self.number, outbound_number, size, "Received Text"
        )

    def send_media(self, outbound_number, date, size="1.9 MB"):
        self._add_to_log(date, outbound_number, self.number, size, "Sent Media")
        outbound_number._add_to_log(
            date, self.number, outbound_number, size, "Received Media"
        )

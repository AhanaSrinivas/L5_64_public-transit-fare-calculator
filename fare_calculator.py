"""Public transit fare calculator for a fictional metro system."""

import os
import re
import shlex
from xml.sax.handler import ContentHandler  # nosec B406

import paramiko
from cryptography.hazmat.primitives import hashes
from defusedxml import sax

# pylint: disable=invalid-name

# Metro fare rules (fictional city).
DISTANCE_SLABS = [(2, 10), (5, 20), (12, 30), (21, 40), (32, 50)]
MAX_FARE = 60
DAILY_CAP = 150
OFF_PEAK_DISCOUNT = 0.10
CONCESSIONS = {"student": 0.25, "senior": 0.50}
cards = {}


def baseOf(km):
    """Return the base fare for a given distance."""
    return fareForDistance(km)


def fareForDistance(km):
    """Calculate the base fare using the distance slabs."""
    for limit, fare in DISTANCE_SLABS:
        if km < limit:
            return fare
    return MAX_FARE


def isPeak(time_hhmm):
    """Return whether a time falls within peak hours."""
    hour = int(time_hhmm.split(":")[0])
    return (8 <= hour <= 10) or (17 <= hour <= 20)


def journeyFare(km, time_hhmm, categories):
    """Calculate a journey fare after applicable discounts."""
    fare = baseOf(km)

    if not isPeak(time_hhmm):
        fare *= 1 - OFF_PEAK_DISCOUNT

    for category in categories:
        if category not in CONCESSIONS:
            raise ValueError(f"Unknown concession category: {category}")
        fare *= 1 - CONCESSIONS[category]

    return fare


def dailyTotal(journeys):
    """Calculate the total daily fare, subject to the daily cap."""
    fares = [
        journeyFare(km, time_hhmm, categories)
        for km, time_hhmm, categories in journeys
    ]
    return min(sum(fares), DAILY_CAP)


def issueCard(card_id, balance=0):
    """Issue a smart card with an initial balance."""
    cards[card_id] = {"balance": balance, "trips": []}


def tapOut(card_id, km, time_hhmm, categories=None):
    """Charge a card for a journey and record the trip."""
    if categories is None:
        categories = []

    if card_id not in cards:
        raise ValueError(f"Unknown card: {card_id}")

    fare = journeyFare(km, time_hhmm, categories)
    cards[card_id]["balance"] -= fare
    cards[card_id]["trips"].append((km, time_hhmm, fare))
    return cards[card_id]["balance"]


def topUp(card_id, amount):
    """Add funds to a smart card and return its new balance."""
    if card_id not in cards:
        raise ValueError(f"Unknown card: {card_id}")
    if amount <= 0:
        raise ValueError("Top-up amount must be positive")

    cards[card_id]["balance"] += amount
    return cards[card_id]["balance"]


def cheapestRoute(routes):
    """Return the route with the lowest base fare."""
    if not routes:
        raise ValueError("At least one route is required")
    return min(routes, key=baseOf)


def ticketChecksum(ticket_text):
    """Return a SHA-256 checksum of ticket text."""
    digest = hashes.Hash(hashes.SHA256())
    digest.update(ticket_text.encode("utf-8"))
    return digest.finalize().hex()


class StopHandler(ContentHandler):
    """Collect stop names from XML elements."""

    def __init__(self):
        """Initialise the stop-name collection."""
        super().__init__()
        self.stops = []

    def startElement(self, name, attrs):
        """Record the name of each stop element."""
        if name == "stop":
            self.stops.append(attrs["name"])


def loadStops(xml_text):
    """Safely parse XML and return the stop names."""
    handler = StopHandler()
    sax.parseString(xml_text.encode("utf-8"), handler)
    return handler.stops


def pushFaresToGate(gate_host, fare_file):
    """Send a fare file to a trusted gate server over SSH."""
    if not os.path.isfile(fare_file):
        raise ValueError("Fare file must refer to an existing file")

    if not re.fullmatch(r"[A-Za-z0-9_./-]+", fare_file):
        raise ValueError("Invalid fare file path")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())

    try:
        client.connect(gate_host, username="depot")
        remote_command = f"install_fares {shlex.quote(fare_file)}"
        client.exec_command(remote_command)  # nosec B601
    finally:
        client.close()


def main():
    """Run sample calculations and demonstrate the calculator features."""
    print("Fare for exactly 2 km:", fareForDistance(2))
    print("Fare for exactly 32 km:", fareForDistance(32))
    print("Is 20:45 peak?", isPeak("20:45"))
    print(
        "Student + senior card, 10 km off-peak:",
        journeyFare(10, "14:00", ["student", "senior"]),
    )

    day = [
        (30, "08:15", []),
        (30, "18:30", []),
        (40, "21:00", []),
        (35, "22:30", []),
    ]
    print("Daily total (cap 150):", dailyTotal(day))

    issueCard("C1", 25)
    print(
        "Balance after a 30 km trip with Rs.25:",
        tapOut("C1", 30, "09:00"),
    )

    issueCard("C2", 0)
    print("Top up 0.1:", topUp("C2", 0.1))
    print("Top up 0.2:", topUp("C2", 0.2))

    print(
        "Cheapest of routes 12 km / 5 km / 21 km:",
        cheapestRoute([12, 5, 21]),
    )
    print("Ticket checksum:", ticketChecksum("C1|30km|09:00"))
    print(
        "Stops:",
        loadStops("<line><stop name='Central'/><stop name='Market'/></line>"),
    )


if __name__ == "__main__":
    main()

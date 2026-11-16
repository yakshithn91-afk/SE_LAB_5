"""Calculate and save demonstration electricity bills from meter readings."""

import json
from pathlib import Path

from defusedxml import ElementTree as ET

SLABS = [(100, 3.5), (200, 5.0), (300, 6.5)]
HIGH_RATE = 8.0
FIXED_CHARGE = 75
METER_XML = (
    "<meters>"
    "<meter id='M1' prev='1200' curr='1350'/>"
    "<meter id='M2' prev='5000' curr='5420'/>"
    "<meter id='M3' prev='800' curr='760'/>"
    "</meters>"
)
bills = []


def read_meters(xml_text):
    """Return each meter ID and its previous and current readings."""
    root = ET.fromstring(xml_text)
    return [
        (meter.get("id"), int(meter.get("prev")), int(meter.get("curr")))
        for meter in root.findall("meter")
    ]


def calculate_units(previous, current):
    """Calculate usage, treating a backward meter reading as zero usage."""
    if current < previous:
        print("Warning: meter reading went backwards")
        return 0
    return current - previous


def energy_charge(units):
    """Calculate energy charges using progressive tariff slabs."""
    charge = 0
    lower_bound = 0
    remaining = units
    for limit, rate in SLABS:
        slab_units = min(remaining, limit - lower_bound)
        if slab_units > 0:
            charge += slab_units * rate
            remaining -= slab_units
        lower_bound = limit
    return charge + remaining * HIGH_RATE


def generate_bill(meter_id, units, tax_rate=0.05, extras=None):
    """Create a bill and add it to the current in-memory bill list."""
    if extras is None:
        extras = {}
    amount = energy_charge(units) + FIXED_CHARGE + sum(extras.values())
    bill = {
        "meter": meter_id,
        "units": units,
        "amount": round(amount * (1 + tax_rate), 2),
    }
    bills.append(bill)
    return bill


def average_bill():
    """Return the average of the current bills, or zero when there are none."""
    if not bills:
        return 0
    return round(sum(bill["amount"] for bill in bills) / len(bills), 2)


def save_bills(file_name="bills.json"):
    """Write the current bill list as UTF-8 JSON."""
    with Path(file_name).open("w", encoding="utf-8") as output_file:
        json.dump(bills, output_file, indent=2)


def main():
    """Run the sample billing scenario and save its results."""
    for meter_id, previous, current in read_meters(METER_XML):
        units = calculate_units(previous, current)
        generate_bill(meter_id, units)
    generate_bill("M4", 50, extras={"late_fee": 25})
    for bill in bills:
        print(
            bill["meter"],
            "used",
            bill["units"],
            "units, bill Rs.",
            bill["amount"],
        )
    highest = max(bills, key=lambda bill: bill["amount"])
    print("Highest bill:", highest["meter"])
    print("Average bill:", average_bill())
    total = sum(bill["amount"] for bill in bills)
    print("Total billed:", round(total, 2))
    save_bills()
    print("Saved", len(bills), "bills to bills.json")


if __name__ == "__main__":
    main()

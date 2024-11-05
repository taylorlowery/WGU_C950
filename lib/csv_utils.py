import csv
from datetime import datetime, time
from models.package import Package
from lib.delivery_data_structure import DeliveryHashTable, DeliveryStatus
from copy import deepcopy


def parse_delivery_time(time_str: str) -> datetime.time:
    if time_str == "EOD":
        return time(23, 59)
    try:
        parsed_time = datetime.strptime(time_str, "%H:%M %p").time()
        return parsed_time
    except ValueError as e:
        raise ValueError(f"Invalid delivery time: {time_str}") from e


def csv_to_packages(filepath: str) -> DeliveryHashTable:
    packages: DeliveryHashTable = DeliveryHashTable(40)

    with open(filepath) as package_file:
        package_reader = csv.reader(package_file, delimiter=",")
        next(package_reader)  # skip header
        for row in package_reader:
            try:
                package_id = int(row[0])
                delivery_address = row[1]
                delivery_city = row[2]
                delivery_state = row[3]
                delivery_zip_code = row[4]
                delivery_deadline_str = row[5]
                delivery_deadline = parse_delivery_time(delivery_deadline_str)
                package_weight = float(row[6])
                special_note = row[7] if row[7] else None

                package = Package(
                    package_id=package_id,
                    delivery_address=delivery_address,
                    delivery_city=delivery_city,
                    delivery_state=delivery_state,
                    delivery_zip_code=delivery_zip_code,
                    package_weight=package_weight,
                    delivery_deadline=delivery_deadline,
                    special_notes=special_note,
                )
                packages.insert(package_id=package_id, package=package)
            except Exception as e:
                print(f"Error: {e}")
                continue

    return packages


def csv_to_distances(filepath: str) -> dict:
    locations: list[str] = []
    distance_map: dict = dict()

    rows = []  # list to hold rows
    with open(file=filepath, encoding="utf-8-sig") as distance_file:
        rows = list(csv.reader(distance_file, delimiter=","))

    # iterate through once, gathering all locations
    for row in rows:
        title = row[1]
        locations.append(title)
        distance_map[title] = dict()

    for i, location in enumerate(locations):
        row = rows[i]
        for j, distance in enumerate(row[2:], start=0):
            if distance == "":
                break  # once we hit empty strings, move to next row
            to_location = locations[j]
            distance_map[location][to_location] = float(distance)
            distance_map[to_location][location] = float(distance)

    return distance_map

import csv
from models.Package import Package
from lib.delivery_data_structure import DeliveryStatus

def csv_to_packages(filepath: str) -> list[Package]:
    packages: list[Package] = []

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
                delivery_deadline = row[5]
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
                packages.append(package)
            except Exception as e:
                print(f"Error: {e}")
                continue

    return packages

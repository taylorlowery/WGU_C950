from typing import Optional
import pytest
from datetime import datetime, time
from lib.csv_utils import csv_to_distances, csv_to_packages
from lib.delivery_algorithm import package_status_at_provided_time, deliver_packages
from lib.delivery_data_structure import DeliveryHashTable
from models.package import Package, DeliveryStatus
from models.truck import Truck


@pytest.fixture
def sample_package():
    """Simulate package after algorithm runs.

    `time_delivered` will be populated and `delivery_status` will be DELIVERED.
    """
    package = Package(
        1, "Test Address", "City", "State", "12345", time(9, 0), "10", "Notes"
    )
    package.delivery_status = DeliveryStatus.DELIVERED
    package.time_loaded_onto_truck = time(8, 0)
    package.time_delivered = time(10, 0)
    package.truck_id = 1
    return package


def test_package_at_hub(sample_package):
    current_time = time(7, 0)  # Before loading time
    result = package_status_at_provided_time(sample_package, current_time)
    assert f"Package 01 - {DeliveryStatus.AT_HUB}" in result


def test_package_en_route(sample_package):
    current_time = time(9, 0)  # En route (already picked up, before delivery)
    result = package_status_at_provided_time(sample_package, current_time)
    assert f"Package 01 - {DeliveryStatus.EN_ROUTE} to Test Address (12345) on truck 1" in result


def test_package_delivered(sample_package):
    current_time = time(11, 0)  # After delivery
    result = package_status_at_provided_time(sample_package, current_time)
    assert f"Package 01 - {DeliveryStatus.DELIVERED}" in result
    assert "10:00:00" in result


def test_unprocessed_package():
    # generate package in unprocessed state
    unprocessed_package = Package(
        2, "Test Address", "City", "State", "12345", time(9, 0), "10", "Notes"
    )
    current_time = time(8, 0)
    result = package_status_at_provided_time(unprocessed_package, current_time)
    assert f"Package 02 - {DeliveryStatus.AT_HUB}" in result


def test_delivery_algorithm():
    packages: DeliveryHashTable = csv_to_packages("data/WGUPSPackageFile.csv")
    distance_table: dict[str, dict[str, float]] = csv_to_distances(
        "data/WGUPSDistanceTable.csv"
    )

    late_packages: list[Package] = []

    packages, total_mileage = deliver_packages(packages, distance_table=distance_table)
    for package_id in packages.package_ids:
        package = packages.lookup(package_id)

        if package.required_truck_id is not None:
            assert package.truck_id == package.required_truck_id

        assert package.delivery_status == DeliveryStatus.DELIVERED

        if package.earliest_load_time is not None:
            assert package.time_loaded_onto_truck >= package.earliest_load_time

        # assert package.time_delivered <= package.delivery_deadline
        if package.time_delivered > package.delivery_deadline:
            late_packages.append(package)

        assert len(late_packages) == 0, late_packages
        assert total_mileage < 140.0

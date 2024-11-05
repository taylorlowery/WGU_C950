from typing import Optional
import pytest
from datetime import datetime, time
from lib.csv_utils import csv_to_distances, csv_to_packages
from lib.delivery_algorithm import package_status_at_provided_time, deliver_packages
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
    assert f"Package 1 {DeliveryStatus.AT_HUB}" in result


def test_package_en_route(sample_package):
    current_time = time(9, 0)  # En route (already picked up, before delivery)
    result = package_status_at_provided_time(sample_package, current_time)
    assert f"Package 1 - {DeliveryStatus.EN_ROUTE} on truck 1" in result


def test_package_delivered(sample_package):
    current_time = time(11, 0)  # After delivery
    result = package_status_at_provided_time(sample_package, current_time)
    assert f"Package 1 {DeliveryStatus.DELIVERED}" in result
    assert "10:00:00" in result


def test_unprocessed_package():
    # generate package in unprocessed state
    unprocessed_package = Package(
        2, "Test Address", "City", "State", "12345", time(9, 0), "10", "Notes"
    )
    current_time = time(8, 0)
    result = package_status_at_provided_time(unprocessed_package, current_time)
    assert f"Package 2 {DeliveryStatus.AT_HUB}" in result


def test_delivery_algoritm():
    packages: list[Package] = csv_to_packages("data/WGUPSPackageFile.csv")
    distance_table: dict[str, dict[str, float]] = csv_to_distances(
        "data/WGUPSDistanceTable.csv"
    )

    packages = deliver_packages(packages, distance_table=distance_table)


def test_get_closest_package(
    current_package: Optional[Package], package: list[Package], distance_table: dict
): ...

def test_delivery_time_calculation():
    # Setup
    truck = Truck(1)
    initial_time = time(8, 0)  # 8:00 AM
    truck.current_time = initial_time
    truck.current_location = "HUB"
    
    # Create test package 10 miles away (at 18 mph = ~33 min drive)
    package = Package(1, "TEST_ADDR")
    truck.distance_table = {
        "HUB": {"TEST_ADDR": 10.0},
        "TEST_ADDR": {"HUB": 10.0}
    }
    truck.packages.append(package)
    
    # Act
    truck.deliver_package(package)
    
    # Assert
    expected_time = time(8, 33)  # Should be ~8:33 AM
    assert truck.current_time.hour == expected_time.hour
    assert truck.current_time.minute == expected_time.minute
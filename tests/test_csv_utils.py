import datetime
import pytest
import lib.csv_utils as csv_utils
from lib.delivery_data_structure import DeliveryStatus


def test_package_csv_load():
    """Simple integration test to validate that packages can be loaded from csv."""
    file_path = "data/WGUPSPackageFile.csv"
    packages_from_csv = csv_utils.csv_to_packages(file_path)
    # Package(3, 233 Canyon Rd, Salt Lake City, 84103, 2.0, EOD, AT_HUB, Can only be on truck 2)
    package = packages_from_csv.lookup(3)
    assert package.package_id == 3
    assert package.delivery_address == "233 Canyon Rd"
    assert package.delivery_city == "Salt Lake City"
    assert package.delivery_state == "UT"
    assert package.delivery_zip_code == "84103"
    assert package.package_weight == 2.0
    assert package.delivery_deadline == datetime.time(23, 59)
    assert package.delivery_status == DeliveryStatus.AT_HUB
    assert package.special_notes == "Can only be on truck 2"


def test_distance_csv_load():
    """Simple integration test to validate distance map can be loaded from csv."""
    filepath = "data\WGUPSDistanceTable.csv"
    distance_map = csv_utils.csv_to_distances(filepath)
    assert distance_map["6351 South 900 East (84121)"]["HUB"] == 3.6

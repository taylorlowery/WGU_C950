import pytest
import lib.csv_utils as csv_utils
from lib.delivery_data_structure import DeliveryStatus


def test_package_csv_load():
    """Simple integration test to validate that packages can be loaded from csv."""
    file_path = "data/WGUPSPackageFile.csv"
    packages_from_csv = csv_utils.csv_to_packages(file_path)
    # Package(3, 233 Canyon Rd, Salt Lake City, 84103, 2.0, EOD, AT_HUB, Can only be on truck 2)
    assert packages_from_csv[2].package_id == 3
    assert packages_from_csv[2].delivery_address == "233 Canyon Rd"
    assert packages_from_csv[2].delivery_city == "Salt Lake City"
    assert packages_from_csv[2].delivery_state == "UT"
    assert packages_from_csv[2].delivery_zip_code == "84103"
    assert packages_from_csv[2].package_weight == 2.0
    assert packages_from_csv[2].delivery_deadline == "EOD"
    assert packages_from_csv[2].delivery_status == DeliveryStatus.AT_HUB
    assert packages_from_csv[2].special_notes == "Can only be on truck 2"


def test_distance_csv_load():
    """Simple integration test to validate distance map can be loaded from csv."""
    filepath = "data\WGUPSDistanceTable.csv"
    distance_map = csv_utils.csv_to_distances(filepath)
    assert (
        distance_map["Wheeler Historic Farm 6351 South 900 East"][
            "Western Governors University 4001 South 700 East, Salt Lake City, UT 84107"
        ]
        == 3.6
    )

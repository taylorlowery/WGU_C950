from lib import delivery_data_structure
import pytest
from lib.delivery_data_structure import DeliveryHashTable, DeliveryStatus, Package


@pytest.mark.parametrize("length", [1, 2, 3])
def test_init_table(length: int):
    hash_table = DeliveryHashTable(length)
    assert len(hash_table.table) == length
    for linked_list in hash_table.table:
        assert linked_list.length == 0
        assert linked_list.head is None
        assert linked_list.tail is None


@pytest.mark.parametrize("length", [0, -1])
def test_init_table_invalid_length(length: int):
    with pytest.raises(ValueError):
        _ = DeliveryHashTable(length)


@pytest.mark.parametrize(
    "length, package_id, expected_index",
    [
        (10, 3, 3),
        (10, 13, 3),
        (11, 121, 0),
        (11, 122, 1),
        (13, 115, 11),
        (1, 1337, 0),
    ],
)
def test_table_hash_function(length: int, package_id: int, expected_index: int):
    hash_table = DeliveryHashTable(length)
    actual_index = hash_table.hash_index(package_id)
    assert actual_index == expected_index


@pytest.mark.parametrize("length", [10])
def test_table_insert(length):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    linked_list = hash_table.table[test_package.package_id]
    assert len(linked_list) == 1
    assert linked_list.head.package == test_package

    for i, ll in enumerate(hash_table.table):
        if i != hash_table.hash_index(test_package.package_id):
            assert len(ll) == 0
            assert ll.head is None
            assert ll.tail is None


@pytest.mark.parametrize("length", [10])
def test_table_multiple_insert_multiple_packages_no_collision(length: int):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_2 = Package(
        package_id=2,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    hash_table.insert(package_id=test_package_2.package_id, package=test_package_2)

    linked_list_1 = hash_table.table[test_package.package_id]
    linked_list_2 = hash_table.table[test_package_2.package_id]

    assert len(linked_list_1) == 1
    assert linked_list_1.head.package == test_package

    assert len(linked_list_2) == 1
    assert linked_list_2.head.package == test_package_2

    for i, ll in enumerate(hash_table.table):
        if i != hash_table.hash_index(
            test_package.package_id
        ) and i != hash_table.hash_index(test_package_2.package_id):
            assert len(ll) == 0
            assert ll.head is None
            assert ll.tail is None


@pytest.mark.parametrize("length", [10])
def test_table_insert_with_collision(length: int):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_2 = Package(
        package_id=2,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_3 = Package(
        package_id=test_package.package_id + length,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    hash_table.insert(package_id=test_package_2.package_id, package=test_package_2)
    hash_table.insert(package_id=test_package_3.package_id, package=test_package_3)

    linked_list_1 = hash_table.table[test_package.package_id]
    linked_list_2 = hash_table.table[test_package_2.package_id]

    assert len(linked_list_1) == 2
    assert linked_list_1.head.package == test_package
    assert linked_list_1.tail.package == test_package_3

    assert len(linked_list_2) == 1
    assert linked_list_2.head.package == test_package_2
    assert linked_list_2.tail.package == test_package_2

    for i, ll in enumerate(hash_table.table):
        if i != hash_table.hash_index(
            test_package.package_id
        ) and i != hash_table.hash_index(test_package_2.package_id):
            assert len(ll) == 0
            assert ll.head is None
            assert ll.tail is None


@pytest.mark.parametrize("length", [10])
def test_table_lookup(length: int):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_2 = Package(
        package_id=2,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_3 = Package(
        package_id=test_package.package_id + length,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    hash_table.insert(package_id=test_package_2.package_id, package=test_package_2)
    hash_table.insert(package_id=test_package_3.package_id, package=test_package_3)

    found_package = hash_table.lookup(test_package.package_id)
    assert found_package == test_package
    # validate that lookup has not removed the package from the table
    ll_1 = hash_table.table[hash_table.hash_index(test_package.package_id)]
    assert ll_1.head.package == test_package
    assert len(ll_1) == 2

    # validate that we can still look up other packages
    found_package = hash_table.lookup(test_package_2.package_id)
    assert found_package == test_package_2

    found_package = hash_table.lookup(test_package_3.package_id)
    assert found_package == test_package_3


@pytest.mark.parametrize("length", [10])
def test_table_remove(length: int):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_2 = Package(
        package_id=2,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    test_package_3 = Package(
        package_id=test_package.package_id + length,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_state="CA",
        delivery_zip_code="90210",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    hash_table.insert(package_id=test_package_2.package_id, package=test_package_2)
    hash_table.insert(package_id=test_package_3.package_id, package=test_package_3)

    removed_package = hash_table.remove(test_package.package_id)
    assert removed_package == test_package
    # validate that the package has been removed from the table
    ll_1 = hash_table.table[hash_table.hash_index(test_package.package_id)]
    assert ll_1.head.package == test_package_3
    assert len(ll_1) == 1

    # validate that we can still look up other packages
    found_package = hash_table.lookup(test_package_2.package_id)
    assert found_package == test_package_2

    found_package = hash_table.lookup(test_package_3.package_id)
    assert found_package == test_package_3

    # remove last item from list
    removed_package = hash_table.remove(test_package_3.package_id)
    assert removed_package == test_package_3
    assert ll_1.length == 0
    assert ll_1.head is None
    assert ll_1.tail is None


@pytest.mark.parametrize("length", [10])
def test_table_remove_nonexistent_package_id(length: int):
    test_package = Package(
        package_id=1,
        delivery_address="123 thing st",
        delivery_city="Coolsville",
        delivery_zip_code="90210",
        delivery_state="CA",
        package_weight=7.0,
        delivery_status=DeliveryStatus.AT_HUB,
        delivery_deadline="10am",
    )

    hash_table = DeliveryHashTable(length)
    hash_table.insert(package_id=test_package.package_id, package=test_package)
    removed_node = hash_table.remove(package_id=3)

    assert removed_node is None

    ll = hash_table.table[hash_table.hash_index(test_package.package_id)]
    assert len(ll) == 1
    assert ll.head.package == test_package
    assert ll.tail.package == test_package

def test_csv_load():
    """Simple integration test to validate that packages can be loaded from csv."""
    file_path = "data/WGUPSPackageFile.csv"
    packages_from_csv = delivery_data_structure.csv_to_packages(file_path)
    # Package(1, 195 W Oakland Ave, Salt Lake City, 84115, 21.0, 10:30 AM, AT_HUB)
    assert packages_from_csv[0].package_id == 1
    assert packages_from_csv[0].delivery_address == "195 W Oakland Ave"
    assert packages_from_csv[0].delivery_city == "Salt Lake City"
    assert packages_from_csv[0].delivery_state == "UT"
    assert packages_from_csv[0].delivery_zip_code == "84115"
    assert packages_from_csv[0].package_weight == 21.0
    assert packages_from_csv[0].delivery_deadline == "10:30 AM"
    assert packages_from_csv[0].delivery_status == DeliveryStatus.AT_HUB

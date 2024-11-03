"""This module contains the main functionality for the C950 Data Structures and Algorithms II WGUPS Delivery Task 2.

"""

from models import Truck
from models.package import Package, DeliveryStatus
from datetime import datetime


START_TIME = datetime.strptime("08:00:00", "%H:%M:%S")


def package_status_at_provided_time(
    selected_package: Package, current_time: datetime.time
) -> str:
    """Print the status of a package at a given time.

    After the packages are passed through the delivery algorithm,
    they will all have been assigned to trucks and have a marked delivery time.

    This function will simulate a package status at different times
    depending on whether the provided "current time" is
    before or after the package's pickup and/or delivery times
    """
    # default state -- AT_HUB
    if (
        selected_package.time_delivered is None
        or current_time < selected_package.time_loaded_onto_truck
    ):
        return f"Package {selected_package.package_id} {DeliveryStatus.AT_HUB}"

    if selected_package.time_delivered < current_time:
        # since this will only be run against packages
        # that have already been run through the algo
        # should be "DELIVERED"
        return f"Package {selected_package.package_id} {selected_package.delivery_status.value} at {selected_package.time_delivered}"

    # current time is before time_delivered and package was loaded on a truck, so it's en route
    return f"Package {selected_package.package_id} - {DeliveryStatus.EN_ROUTE} on truck {selected_package.truck_id}"


def deliver_packages(packages: list[Package], distance_table: dict[str, dict[str, float]]):
    """Nearest-Neighbor Greedy Algorithm to deliver packages.

    Assumptions:
        •  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
        •  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
        •  There are no collisions.
        •  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
        •  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
        •  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
        •  There is up to one special note associated with a package.
        •  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
        •  The distances provided in the "WGUPS Distance Table" are equal regardless of the direction traveled.
        •  The day ends when all 40 packages have been delivered.

    """

    # three trucks are available, but only two drivers, so only two can be utilized.
    truck_1 = Truck(truck_id=1, distance_table=distance_table)
    truck_2 = Truck(truck_id=2, distance_table=distance_table)

    # load distances
    # distances need to be parsed according to their weirdnesses

    # since some packages are delayed til 9:05,
    # start one truck delivering all the other early packages,
    # second truck will be loaded at 9:05 and start delivering all those before 10:30
    # once all 10:30am deliveries are complete,
    # nearest neighbor deliveries til all are delivered
    i: int = 0
    while i < len(packages):
        j = 0
        while j < 16:
            truck_1.load_package(package=packages[j])
            j += 1
            i += 1
        truck_1.deliver_all_packages()

    # total truck mileage must be less than 140 miles
    total_mileage = truck_1.current_mileage + truck_2.current_mileage
    print(f"Total Mileage: {total_mileage}")

    return packages

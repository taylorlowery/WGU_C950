"""This module contains the main functionality for the C950 Data Structures and Algorithms II WGUPS Delivery Task 2.

"""

from typing import Optional
from lib.delivery_data_structure import DeliveryHashTable
from models import Truck
from models.package import Package, DeliveryStatus
import datetime


START_TIME = datetime.datetime.strptime("08:00:00", "%H:%M:%S")


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
        return f"Package {selected_package.package_id} - {DeliveryStatus.AT_HUB}"

    if selected_package.time_delivered < current_time:
        # since this will only be run against packages
        # that have already been run through the algo
        # should be "DELIVERED"
        return f"Package {selected_package.package_id} - {selected_package.delivery_status.value} by truck {selected_package.truck_id} at {selected_package.time_delivered} (delivery deadline was {selected_package.delivery_deadline})"

    # current time is before time_delivered and package was loaded on a truck, so it's en route
    return f"Package {selected_package.package_id} - {DeliveryStatus.EN_ROUTE} on truck {selected_package.truck_id}"


def deliver_packages(
    packages: DeliveryHashTable, distance_table: dict[str, dict[str, float]]
):
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
    current_package_truck_1: Optional[Package] = None
    current_package_truck_2: Optional[Package] = None
    while i < len(packages):
        j = i
        while j < i + 16 and j < len(packages):
            current_package_truck_1 = get_next_closest_package(
                current_package=current_package_truck_1,
                packages=packages,
                distance_table=distance_table,
                current_time=truck_1.current_time,
                truck_id=truck_1.truck_id,
            )
            if current_package_truck_1 is not None:
                truck_1.load_package(current_package_truck_1)

            current_package_truck_2 = get_next_closest_package(
                current_package=current_package_truck_2,
                packages=packages,
                distance_table=distance_table,
                current_time=truck_2.current_time,
                truck_id=truck_2.truck_id,
            )
            if current_package_truck_2 is not None:
                truck_2.load_package(current_package_truck_2)

            j += 1
        truck_1.deliver_all_packages()
        truck_2.deliver_all_packages()
        i += 16

        # double-check that no packages were missed
        # if all other packages are delivered before the earliest load time of a package,
        # the delivery loop can end without trucks every picking up the package.
        if current_package_truck_1 is None and current_package_truck_2 is None:
            needs_reset = False
            # iterate through packages and make sure all have been loaded onto a truck
            for package_id in packages.package_ids:
                package = packages.lookup(package_id)
                # if any were never loaded,
                # allow some time to pass and restart delivery loop
                # only undelivered packages will be attempted to be delivered on next loop
                if package.truck_id is None:
                    needs_reset = True
                    # allow some time to pass
                    truck_1.current_time = datetime.time(
                        truck_1.current_time.hour,
                        (truck_1.current_time.minute + 10) % 60,
                    )
                    truck_2.current_time = datetime.time(
                        truck_2.current_time.hour,
                        (truck_2.current_time.minute + 10) % 60,
                    )
                    # reset the loops
                    i = 0
                    current_package_truck_1 = None
                    current_package_truck_2 = None
                    break

            if not needs_reset:
                break

    # total truck mileage must be less than 140 miles
    total_mileage = truck_1.current_mileage + truck_2.current_mileage
    print(f"Total Mileage: {total_mileage}")

    return packages


def get_next_closest_package(
    *,
    current_package: Optional[Package],
    packages: DeliveryHashTable,
    distance_table: dict,
    current_time: datetime.time,
    truck_id: int,
) -> Optional[Package]:
    closest_package: Optional[Package] = None
    min_distance: float = float("inf")

    if current_package is None:
        current_package = packages.lookup(1)

    for candidate_id in packages.package_ids:
        # make sure it's not the same package
        if candidate_id == current_package.package_id:
            continue

        candidate: Package = packages.lookup(candidate_id)

        if candidate.delivery_status != DeliveryStatus.AT_HUB:
            continue

        # only packages not on trucks qualify
        if candidate.time_loaded_onto_truck is not None:
            continue

        if (
            candidate.earliest_load_time is not None
            and current_time < candidate.earliest_load_time
        ):
            continue

        # package 9 cannot be loaded til 10:20am (when its correct address becomes known)
        # after that time, correct the address
        if candidate.package_id == 9:
            candidate.delivery_address = "410 S State St"
            candidate.delivery_city = "Salt Lake City"
            candidate.delivery_state = "UT"
            candidate.delivery_zip_code = "84111"

        if (
            candidate.required_truck_id is not None
            and candidate.required_truck_id != truck_id
        ):
            continue

        distance_to_candidate = distance_table[current_package.address][
            candidate.address
        ]

        if distance_to_candidate < min_distance:
            closest_package = candidate
            min_distance = distance_to_candidate

    return closest_package

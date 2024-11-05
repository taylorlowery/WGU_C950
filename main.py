"""
Author: Taylor Lowery
Student ID: 011681727

Requirements:
- [x] Develop a hash table, without using any additional libraries or classes, that has an insertion function that takes the package ID as input and inserts each of the following data components into the hash table:
    - delivery address
    - delivery deadline
    - delivery city
    - delivery zip code
    - package weight
    - delivery status (i.e., at the hub, en route, or delivered), including the delivery time

- [x] Develop a look-up function that takes the package ID as input and returns each of the following corresponding data components:
    - delivery address
    - delivery deadline
    - delivery city
    - delivery zip code
    - package weight
    - delivery status (i.e., at the hub, en route, or delivered), including the delivery time

- [ ] Write an original program that will deliver all packages and meet all requirements using the attached supporting documents "Salt Lake City Downtown Map," "WGUPS Distance Table," and "WGUPS Package File."
    - [x] Create an identifying comment within the first line of a file named "main.py" that includes your student ID.
    - [ ] Include comments in your code to explain both the process and the flow of the program.

- [ ] Provide an intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time and the total mileage traveled by all trucks. (The delivery status should report the package as at the hub, en route, or delivered. Delivery status must include the time.)
    - [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 8:35 a.m. and 9:25 a.m.
    - [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 9:35 a.m. and 10:25 a.m.
    - [ ] Provide screenshots to show the status of all packages loaded onto each truck at a time between 12:03 p.m. and 1:12 p.m.

- [ ] Provide screenshots showing successful completion of the code that includes the total mileage traveled by all trucks.

- [ ] Justify the package delivery algorithm used in the solution as written in the original program by doing the following:
    - [ ] Describe two or more strengths of the algorithm used in the solution.
    - [ ] Verify that the algorithm used in the solution meets all requirements in the scenario.
    - [ ] Identify two other named algorithms that are different from the algorithm implemented in the solution and would meet all requirements in the scenario.
        - [ ] Describe how both algorithms identified in part F3 are different from the algorithm used in the solution.

- [ ] Describe what you would do differently, other than the two algorithms identified in part F3, if you did this project again, including details of the modifications that would be made.

- [ ] Verify that the data structure used in the solution meets all requirements in the scenario.
    - [ ] Identify two other data structures that could meet the same requirements in the scenario.
        - [ ] Describe how each data structure identified in H1 is different from the data structure used in the solution.
"""

from lib.delivery_algorithm import deliver_packages, package_status_at_provided_time
from lib.delivery_data_structure import DeliveryHashTable
from models import Package, Truck
from datetime import datetime, timedelta
from lib.csv_utils import csv_to_packages, csv_to_distances


def main():
    print("Welcome to the WGUPS delivery system!")
    print("Loading package information...")

    packages: DeliveryHashTable = csv_to_packages("data/WGUPSPackageFile.csv")
    distance_table: dict[str, dict[str, float]] = csv_to_distances(
        "data/WGUPSDistanceTable.csv"
    )

    packages = deliver_packages(packages, distance_table=distance_table)

    print("Package info loaded!")
    print("Press 'q' to quit at any time.")
    try:
        _input = ""
        while _input.lower() != "q":

            # Get user's desired package
            _input = input(
                f"Please enter a package id (1 - {len(packages)}) to view its status, or -1 to print all package statuses."
                "\nPress q to quit\n>> "
            )
            try:
                package_id = int(_input)

                # get the desired time user would like to see package status
                current_time = ask_for_current_time()

                # user selects valid ID, so print its status
                if 1 <= package_id <= len(packages):
                    selected_package = packages[package_id - 1]
                    print(
                        package_status_at_provided_time(
                            selected_package=selected_package, current_time=current_time
                        )
                    )

                # User wants to see all package statuses
                elif -1 == package_id:
                    for p in packages:
                        print(
                            package_status_at_provided_time(
                                selected_package=p, current_time=current_time
                            )
                        )
                else:
                    print(
                        "Invalid package ID. Please enter a number between 1 and",
                        len(packages),
                    )

            except ValueError:
                if _input.lower() != "q":
                    print("Invalid input.")

    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting...")

    print("Goodbye!")


def ask_for_current_time():
    """Ask user to input the time they would like to see package statuses for."""
    try:
        current_time_str = input("Please enter the current time (HH:MM):\n>> ")

        current_time = datetime.strptime(current_time_str, "%H:%M")
        return current_time

    except ValueError:
        print("Invalid time format. Please enter the time in HH:MM format.")


if __name__ == "__main__":
    main()

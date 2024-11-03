"""
Author: Taylor Lowery
Student ID: 011681727

Description:
This module contains the main functionality for the C950 Data Structures and Algorithms II WGUPS Delivery Task 2.
Assumptions:
•  Each truck can carry a maximum of 16 packages, and the ID number of each package is unique.
•  The trucks travel at an average speed of 18 miles per hour and have an infinite amount of gas with no need to stop.
•  There are no collisions.
•  Three trucks and two drivers are available for deliveries. Each driver stays with the same truck as long as that truck is in service.
•  Drivers leave the hub no earlier than 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed.
•  The delivery and loading times are instantaneous (i.e., no time passes while at a delivery or when moving packages to a truck at the hub). This time is factored into the calculation of the average speed of the trucks.
•  There is up to one special note associated with a package.
•  The delivery address for package #9, Third District Juvenile Court, is wrong and will be corrected at 10:20 a.m. WGUPS is aware that the address is incorrect and will be updated at 10:20 a.m. However, WGUPS does not know the correct address (410 S. State St., Salt Lake City, UT 84111) until 10:20 a.m.
•  The distances provided in the “WGUPS Distance Table” are equal regardless of the direction traveled.
•  The day ends when all 40 packages have been delivered.

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

- [ ] Write an original program that will deliver all packages and meet all requirements using the attached supporting documents “Salt Lake City Downtown Map,” “WGUPS Distance Table,” and “WGUPS Package File.”
   - [x] Create an identifying comment within the first line of a file named “main.py” that includes your student ID.
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

from models import Package, Truck
from lib.csv_utils import csv_to_packages  # Import the function


def main():
    truck_1 = Truck()
    truck_2 = Truck()
    truck_3 = Truck()
    
    packages = csv_to_packages('data/WGUPSPackageFile.csv')  # Load packages from CSV

    # ...existing code...


if __name__ == "__main__":
    main()
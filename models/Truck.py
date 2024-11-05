import datetime
from typing import Optional, Deque
from models.package import Package, DeliveryStatus
from dataclasses import dataclass, field


TRUCK_SPEED_MPH: float = 18.0


@dataclass
class Truck:
    truck_id: int
    distance_table: dict[str, dict[str, float]] = field(default_factory=dict)
    packages_to_deliver: Deque[Package] = field(default_factory=Deque)
    delivered_packages: list[Package] = field(default_factory=list)
    current_package: Optional[Package] = None
    current_location: str = "HUB"
    current_time: datetime.time = datetime.time(8, 0)
    active: bool = False
    current_mileage: float = 0.0

    def load_package(self, package: Package):
        """Load packages onto truck.

        The order they are loaded determines delivery order,
        which will be determined on the main algorithm.
        Marks the package as having been loaded onto this truck.
        """
        package.time_loaded_onto_truck = self.current_time
        package.truck_id = self.truck_id
        self.packages_to_deliver.append(package)

    def next_package(self) -> Optional[Package]:
        """Retrieve next package from queue, or return None if empty"""
        if len(self.packages_to_deliver) == 0:
            return None
        p = self.packages_to_deliver.popleft()
        return p

    def deliver_package(self, package: Package):
        """Deliver a package.

        Using the distance map and current time,
        calculate dilvery time to next address,
        and update truck and package fields to state after delivery.
        """
        # get distance and time to delivery
        distance = self.distance_table[self.current_location][package.address]
        elapsed_time = distance / TRUCK_SPEED_MPH

        # move truck through time and space to delivery location
        self.current_location = package.address
        self.current_mileage += distance
        current_datetime = datetime.datetime.combine(
            datetime.date.today(), self.current_time
        )
        current_datetime = current_datetime + datetime.timedelta(hours=elapsed_time)
        self.current_time = current_datetime.time()

        # set package status to delivered
        package.delivery_status = DeliveryStatus.DELIVERED
        package.time_delivered = self.current_time
        self.delivered_packages.append(package)

    def deliver_all_packages(self):
        # one by one, dequeue and deliver packages
        while (package := self.next_package()) is not None:
            self.deliver_package(package=package)

        # return home
        distance_home = self.distance_table[self.current_location]["HUB"]
        elapsed_time = distance_home / TRUCK_SPEED_MPH
        self.current_mileage += distance_home
        self.current_location = "HUB"
        current_datetime = datetime.datetime.combine(
            datetime.date.today(), self.current_time
        )
        self.current_time = (
            current_datetime + datetime.timedelta(hours=elapsed_time)
        ).time()

import datetime
from typing import Optional, Deque
from models.package import Package, DeliveryStatus
from dataclasses import dataclass, field


TRUCK_SPEED_MPH: float = 18.0


@dataclass
class Truck:
    truck_id: int
    distance_map = dict()
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
        if self.packages_to_deliver.count() == 0:
            return None
        p = self.packages_to_deliver.popleft()
        return p

    def deliver_package(
        self, package: Package
    ):
        distance = self.distance_map[self.current_location][package.delivery_address]
        elapsed_time = distance / TRUCK_SPEED_MPH
        self.current_location = package.delivery_address
        self.current_mileage += distance
        self.current_time = self.current_time + datetime.timedelta(hours=elapsed_time)
        package.delivery_state = DeliveryStatus.DELIVERED
        package.time_delivered = self.current_time
        self.delivered_packages.append(package)

    def deliver_all_packages(self):
        # one by one, dequeue and deliver packages
        while (package := self.next_package()) is not None:
            # TODO: Parse distances and get distance map
            self.deliver_package(package=package, distance_map=None)

        # return home
        distance_home = self.distance_map[self.current_location]["HUB"]
        elapsed_time = distance_home / TRUCK_SPEED_MPH
        self.current_mileage += distance_home
        self.current_location = "HUB"
        self.current_time += datetime.timedelta(hours=elapsed_time)

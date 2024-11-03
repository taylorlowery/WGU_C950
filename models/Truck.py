from typing import Optional, Deque
from models.Package import Package, DeliveryStatus
from dataclasses import dataclass


TRUCK_SPEED_MPH: float = 18.0

@dataclass
class Truck:
    packages_to_deliver: Deque[Package] = Deque()
    delivered_packages: list[Package] = list()
    current_package: Optional[Package] = None
    active: bool = False

def next_package(self) -> Optional[Package]:
    """Iterate through the list of packages and get the next to be delivered"""
    for p in self.packages_to_deliver:
        if p is None or p.delivery_status != DeliveryStatus.DELIVERED:
            return p
    return None

from enum import StrEnum
from typing import Optional
import datetime
from dataclasses import dataclass


class DeliveryStatus(StrEnum):
    AT_HUB = "AT_HUB"
    EN_ROUTE = "EN_ROUTE"
    DELIVERED = "DELIVERED"


@dataclass
class Package:
    package_id: int
    delivery_address: str
    delivery_city: str
    delivery_state: str
    delivery_zip_code: str
    package_weight: float
    delivery_deadline: datetime.time
    special_notes: Optional[str] = None
    delivery_status: DeliveryStatus = DeliveryStatus.AT_HUB
    time_loaded_onto_truck: Optional[datetime.time] = None
    time_delivered: Optional[datetime.time] = None
    truck_id: Optional[int] = None

    @property
    def address(self) -> str:
        # return the address in the form matching the distance table
        # ex, `1060 Dalton Ave S (84104)`
        return f"{self.delivery_address} ({self.delivery_zip_code})"

    @property
    def required_truck_id(self) -> Optional[int]:
        if (
            self.special_notes is not None
            and "Can only be on truck" in self.special_notes
        ):
            return int(self.special_notes[-1])

    @property
    def earliest_load_time(self) -> Optional[datetime.time]:
        """Return the earliest time the package can be loaded onto a truck.
        If there is a note about when it will arrive at the depot, extract the time and return it.
        If the wrong address is listed, return the time the  address will be corrected (10:20am)
        """
        if (
            self.special_notes is not None
            and "will not arrive to depot until" in self.special_notes
        ):
            time_str = self.special_notes.split("until ")[1].strip()
            hour, minute = map(int, time_str[:-2].split(":"))
            if time_str.endswith("pm") and hour != 12:
                hour += 12
            return datetime.time(hour=hour, minute=minute)
        elif (
            self.special_notes is not None
            and "Wrong address listed" in self.special_notes
        ):
            return datetime.time(hour=10, minute=20)
        return None

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
    time_delivered: Optional[datetime.time] = None
    truck_id: Optional[int] = None
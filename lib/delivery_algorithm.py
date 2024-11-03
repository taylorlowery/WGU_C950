from models.package import Package, DeliveryStatus
from datetime import datetime

def print_package_status_at_provided_time(
    selected_package: Package, current_time: datetime.time
) -> str:
    """Print the status of a package at a given time.
    
    After the packages are passed through the delivery algorithm, 
    they will all have been assigned to trucks and have a marked delivery time.

    This function will simulate a package status at different times
    depending on whether the provided "current time" is 
    before or after the package's pickup and/or delivery times 
    """
    if current_time < selected_package.time_loaded_onto_truck:
        return f"Package {selected_package.package_id} {DeliveryStatus.AT_HUB}"

    if (
        selected_package.time_delivered < current_time
    ):
        # since this will only be run against packages 
        # that have already been run through the algo
        # should be "DELIVERED"
        return f"Package {selected_package.package_id} {selected_package.delivery_status.value} at {selected_package.time_delivered}"
            
    return f"Package {selected_package.package_id} - {DeliveryStatus.EN_ROUTE} on truck {selected_package.truck_id}"

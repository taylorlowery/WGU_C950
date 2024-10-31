import csv
from enum import StrEnum
from typing import Optional


class DeliveryStatus(StrEnum):
    AT_HUB = "AT_HUB"
    EN_ROUTE = "EN_ROUTE"
    DELIVERED = "DELIVERED"


class Package:
    def __init__(
        self,
        package_id: int,
        delivery_address: str,
        delivery_city: str,
        delivery_state: str,
        delivery_zip_code: str,
        package_weight: float,
        delivery_deadline: str,
        delivery_status: DeliveryStatus,
    ) -> None:
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip_code = delivery_zip_code
        self.package_weight = package_weight
        self.delivery_deadline = delivery_deadline
        self.delivery_status = delivery_status

    def __repr__(self) -> str:
        return f"Package({self.package_id}, {self.delivery_address}, {self.delivery_city}, {self.delivery_zip_code}, {self.package_weight}, {self.delivery_deadline}, {self.delivery_status})"



class Node:
    def __init__(self, package: Package) -> None:
        self.package: Package = package
        self.next: Optional[Node] = None
        self.previous: Optional[Node] = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.length: int = 0

    def __len__(self) -> int:
        return self.length

    def insert_package(self, package: Package):
        new_node: Node = Node(package=package)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def remove_node(self, node: Node) -> Node:
        if node == self.head:
            self.head = node.next
            node.next = None
            if self.length == 1:
                self.tail = None
        elif node == self.tail:
            self.tail = node.previous
            node.previous.next = None
            node.previous = None
        else:
            node.previous.next = node.next
            node.next.previous = node.previous
            node.previous = None
            node.next = None
        self.length -= 1
        return node

    def find_node(self, package_id: int) -> Node | None:
        current: Node = self.head
        while current is not None:
            if current.package.package_id == package_id:
                return current
            else:
                current = current.next
        return None


class DeliveryHashTable:
    def __init__(self, length: int):
        if length < 1:
            raise ValueError(
                "The hash table must be initialized with a positive length."
            )
        self.table = [LinkedList() for _ in range(length)]

    def hash_index(self, package_id: int) -> int:
        if package_id < 1:
            raise ValueError("Invalid package id: must be a positive integer.")
        return package_id % len(self.table)

    def insert(self, package_id: int, package: Package):
        index: int = self.hash_index(package_id)
        self.table[index].insert_package(package)

    def lookup(self, package_id: int) -> Package | None:
        index: int = self.hash_index(package_id=package_id)
        # potential weakness: have to use hash index and package id
        node = self.table[index].find_node(package_id)
        if node is not None:
            return node.package
        return None

    def remove(self, package_id: int) -> Package | None:
        index: int = self.hash_index(package_id)
        node = self.table[index].find_node(package_id)
        if node is not None:
            return self.table[index].remove_node(node).package
        return None


def csv_to_packages(filepath: str) -> list[Package]:
    packages: list[Package] = []

    with open(filepath) as package_file:
        package_reader = csv.reader(package_file, delimiter=',')
        next(package_reader) # skip header
        for row in package_reader:
            try:
                package_id = int(row[0])
                delivery_address = row[1]
                delivery_city = row[2]
                delivery_state = row[3]
                delivery_zip_code = row[4]
                delivery_deadline = row[5]
                package_weight = float(row[6])
                special_note = row[7]
                delivery_status = DeliveryStatus.AT_HUB
                package = Package(
                    package_id=package_id,
                    delivery_address=delivery_address,
                    delivery_city=delivery_city,
                    delivery_state=delivery_state,
                    delivery_zip_code=delivery_zip_code,
                    package_weight=package_weight,
                    delivery_deadline=delivery_deadline,
                    delivery_status=delivery_status
                )
                packages.append(package)
            except Exception as e:
                print(f"Error: {e}")
                continue

    return packages

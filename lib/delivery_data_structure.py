import csv
from enum import StrEnum
from typing import Optional
from models.package import Package


class DeliveryStatus(StrEnum):
    AT_HUB = "AT_HUB"
    EN_ROUTE = "EN_ROUTE"
    DELIVERED = "DELIVERED"


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
        # track the package ids that have been added, analagous to dict.keys()
        self.package_ids: list[int] = []
        
        # list of linked lists to act as the hash table itself
        self.table = [LinkedList() for _ in range(length)]

    def __len__(self):
        return len(self.package_ids)

    def hash_index(self, package_id: int) -> int:
        """Hash the package id to use as an index for the linked list."""
        if package_id < 1:
            raise ValueError("Invalid package id: must be a positive integer.")
        return package_id % len(self.table)

    def insert(self, package_id: int, package: Package):
        """Add a package to the hash table"""
        index: int = self.hash_index(package_id)
        self.table[index].insert_package(package)
        self.package_ids.append(package_id)

    def lookup(self, package_id: int) -> Package | None:
        """Search for a package in the hash table.
        If found, returns the node without removing it from the hash table.
        """
        index: int = self.hash_index(package_id=package_id)
        # potential weakness: have to use hash index and package id
        node = self.table[index].find_node(package_id)
        if node is not None:
            return node.package
        return None

    def remove(self, package_id: int) -> Package | None:
        """Removes a package from the hash table."""
        index: int = self.hash_index(package_id)
        node = self.table[index].find_node(package_id)
        if node is not None:
            node = self.table[index].remove_node(node).package
            self.package_ids.remove(package_id)
            return node
        return None

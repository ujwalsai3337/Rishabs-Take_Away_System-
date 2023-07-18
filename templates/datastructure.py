class Order:
    def __init__(self, item_name, quantity, price):
        """
        Represents an individual order item.

        Args:
            item_name (str): The name of the item.
            quantity (int): The quantity of the item.
            price (float): The price of the item.
        """
        self.item_name = item_name
        self.quantity = quantity
        self.price = price
        self.next = None


class Customer:
    def __init__(self, customer_id):
        """
        Represents a customer and their associated orders.

        Args:
            customer_id (str): The ID of the customer.
        """
        self.customer_id = customer_id
        self.order_head = None
        self.next = None


class HashMap:
    def __init__(self):
        self.capacity = 16
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash_key(self, key):
        """
        Hashes the given key using a simple hash function.

        Args:
            key: The key to be hashed.

        Returns:
            int: The hashed value.
        """
        return hash(key) % self.capacity

    def put(self, key, value):
        """
        Inserts a key-value pair into the hash map.

        Args:
            key: The key of the entry.
            value: The value associated with the key.
        """
        index = self.hash_key(key)
        entry = self.buckets[index]

        # If the bucket is empty, create a new entry
        if entry is None:
            self.buckets[index] = [(key, value)]
            self.size += 1
            self.resize()
            return

        # If the key already exists, update its value
        for i, (existing_key, existing_value) in enumerate(entry):
            if existing_key == key:
                entry[i] = (key, value)
                return

        # If the key doesn't exist, append a new entry
        entry.append((key, value))
        self.size += 1
        self.resize()

    def get(self, key):
        """
        Retrieves the value associated with the given key.

        Args:
            key: The key to search for.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        index = self.hash_key(key)
        entry = self.buckets[index]

        if entry is None:
            return None

        for existing_key, value in entry:
            if existing_key == key:
                return value

        return None

    def remove(self, key):
        """
        Removes the key-value pair associated with the given key.

        Args:
            key: The key to be removed.
        """
        index = self.hash_key(key)
        entry = self.buckets[index]

        if entry is None:
            return

        for i, (existing_key, _) in enumerate(entry):
            if existing_key == key:
                del entry[i]
                self.size -= 1
                return

    def contains(self, key):
        """
        Checks if the hash map contains the given key.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        index = self.hash_key(key)
        entry = self.buckets[index]

        if entry is None:
            return False

        for existing_key, _ in entry:
            if existing_key == key:
                return True

        return False

    def is_empty(self):
        """
        Checks if the hash map is empty.

        Returns:
            bool: True if the hash map is empty, False otherwise.
        """
        return self.size == 0

    def resize(self):
        """
        Resizes the hash map if the load factor exceeds 0.75.
        """
        load_factor = self.size / self.capacity

        if load_factor >= 0.75:
            self.capacity *= 2
            new_buckets = [None] * self.capacity

            for entry in self.buckets:
                if entry is not None:
                    for key, value in entry:
                        index = self.hash_key(key)
                        new_entry = new_buckets[index]

                        if new_entry is None:
                            new_buckets[index] = [(key, value)]
                        else:
                            new_entry.append((key, value))

            self.buckets = new_buckets


class Node:
    def __init__(self, customer_id, quantity):
        self.customer_id = customer_id
        self.quantity = quantity
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, customer_id, quantity):
        new_node = Node(customer_id, quantity)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.is_empty():
            return None

        removed_node = self.head
        self.head = self.head.next
        removed_node.next = None

        if self.head is None:
            self.tail = None

        return removed_node


class FoodItem:
    def __init__(self, item_name):
        """
        Represents a food item required for production.

        Args:
            item_name (str): The name of the food item.
        """
        self.item_name = item_name
        self.food_chain = LinkedQueue()

    def add_customer_order(self, customer_id, quantity):
        """
        Adds a customer's order for this food item.

        Args:
            customer_id (str): The ID of the customer.
            quantity (int): The quantity of the item.
        """
        self.food_chain.enqueue(customer_id, quantity)

    def display_customer_orders(self):
        """Displays the customers who ordered this food item."""
        current_node = self.food_chain.head
        while current_node:
            print(f"Customer ID: {current_node.customer_id}, Quantity: {current_node.quantity}")
            current_node = current_node.next


class FoodProductionDepartment:
    def __init__(self):
        """Represents the food production department."""
        self.food_items = HashMap()

    def enqueue_customer_order(self, customer_id, item_name, quantity):
        """
        Enqueues a customer's order for a specific food item in the production department.

        Args:
            customer_id (str): The ID of the customer.
            item_name (str): The name of the food item.
            quantity (int): The quantity of the item.
        """
        item_name_lower = item_name.lower()  # Convert item name to lowercase for case-insensitive comparison

        if self.food_items.get(item_name_lower):
            food_item = self.food_items.get(item_name_lower)
            food_item.add_customer_order(customer_id, quantity)
        else:
            food_item = FoodItem(item_name)
            food_item.add_customer_order(customer_id, quantity)
            self.food_items.put(item_name_lower, food_item)

    def dequeue_customer(self, customer_id):
        """
        Dequeues a customer's orders from the production department.

        Args:
            customer_id (str): The ID of the customer.
        """
        for item_name, food_item in self.food_items.map.items():
            current_node = food_item.food_chain.head
            prev_node = None
            while current_node:
                if current_node.customer_id == customer_id:
                    if prev_node:
                        prev_node.next = current_node.next
                    else:
                        food_item.food_chain.head = current_node.next

                    if current_node == food_item.food_chain.tail:
                        food_item.food_chain.tail = prev_node

                    current_node.next = None
                    break

                prev_node = current_node
                current_node = current_node.next

    def display_food_items(self):
        """Displays all the food items and their associated customer orders."""
        for bucket in self.food_items.buckets:
            if bucket is not None:
                for item_name, food_item in bucket:
                    print(f"{item_name} ->", end="")
                    current_node = food_item.food_chain.head
                    while current_node.next:
                        print(f" ({current_node.customer_id},{current_node.quantity})", end=",")
                        current_node = current_node.next
                    print(f" ({current_node.customer_id},{current_node.quantity})")

class NestedLinkedQueue:
    def __init__(self):
        """Represents a nested linked queue of customers and their orders."""
        self.head = None
        self.tail = None
        self.food_production_department = FoodProductionDepartment()

    def is_empty(self):
        """Checks if the nested linked queue is empty."""
        return self.head is None

    def enqueue_customer(self, customer_id):
        """
        Adds a new customer to the nested linked queue.

        Args:
            customer_id (str): The ID of the customer.
        """
        new_customer = Customer(customer_id)
        if self.is_empty():
            self.head = new_customer
            self.tail = new_customer
        else:
            self.tail.next = new_customer
            self.tail = new_customer

    def dequeue_customer(self):
        """
        Removes and returns the customer at the front of the nested linked queue.
        Automatically enqueues the customer's food items to the food production department.

        Returns:
            Customer: The customer at the front of the queue, or None if the queue is empty.
        """
        if self.is_empty():
            return None

        removed_customer = self.head
        self.head = self.head.next
        removed_customer.next = None

        if self.head is None:
            self.tail = None

        # Automatically enqueue customer's food items to the food production department
        current_order = removed_customer.order_head
        while current_order:
            self.food_production_department.enqueue_customer_order(
                removed_customer.customer_id,
                current_order.item_name,
                current_order.quantity
            )
            current_order = current_order.next

        return removed_customer

    def add_order(self, customer_id, item_name, quantity, price):
        """
        Adds a new order to the customer's order list.

        Args:
            customer_id (str): The ID of the customer.
            item_name (str): The name of the item.
            quantity (int): The quantity of the item.
            price (float): The price of the item.
        """
        current_customer = self.head
        while current_customer:
            if current_customer.customer_id == customer_id:
                if current_customer.order_head is None:
                    current_customer.order_head = Order(item_name, quantity, price)
                    current_customer.order_tail = current_customer.order_head
                else:
                    current_customer.order_tail.next = Order(item_name, quantity, price)
                    current_customer.order_tail = current_customer.order_tail.next
                break
            current_customer = current_customer.next

    def display_customers(self):
        """Displays all the customers and their orders."""
        current_customer = self.head
        while current_customer:
            print("Customer ID:", current_customer.customer_id)
            print("Orders:")
            current_order = current_customer.order_head
            while current_order:
                print("Item Name:", current_order.item_name)
                print("Quantity:", current_order.quantity)
                print("Price:", current_order.price)
                print("--------------------")
                current_order = current_order.next
            current_customer = current_customer.next

# Testing the code

if __name__ == "__main__":
    # Create the bill counter data structure
    queue = NestedLinkedQueue()

    # Create the food production department data structure
    food_department = FoodProductionDepartment()

    # Add customers to the queue
    queue.enqueue_customer("C1")
    queue.enqueue_customer("C2")

    # Add orders for customers
    queue.add_order("C1", "Burger", 2, 500)
    queue.add_order("C1", "Pizza", 1, 80)
    queue.add_order("C2", "Pizza", 3, 60)
    queue.add_order("C2", "Burger", 2, 60)
    queue.add_order("C2", "Ice Cream", 2, 40)

    # Display customers and their orders from the bill counter
    print("Customers and their orders from the bill counter:")
    queue.display_customers()
    print()

    # Dequeue a customer from the bill counter
    removed_customer = queue.dequeue_customer()
    print("Customer removed from the bill counter:", removed_customer.customer_id)
    print()

    removed_customer = queue.dequeue_customer()
    print("Customer removed from the bill counter:", removed_customer.customer_id)
    print()

    # Display food items and associated customer orders after customer removal
    print("Food items and their associated customer orders:")
    queue.food_production_department.display_food_items()



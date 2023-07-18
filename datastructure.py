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
    def __init__(self, customer_id, option = None, payment = None, verification = None):
        """
        Represents a customer and their associated orders.

        Args:
            customer_id (str): The ID of the customer.
        """
        self.customer_id = customer_id
        self.option = option
        self.payment = payment
        self.order_head = None
        self.verification = verification
        self.next = None
    
    def display(self):
        output = ""
        output += f"Customer ID:, {self.customer_id}\n"
        output += "Your Orders:\n"
        current_order = self.order_head
        while current_order:
            output += f"Item Name:, {current_order.item_name}\n"
            output += f"Quantity:, {current_order.quantity}\n"
            output += f"Price:, {int(current_order.price)*int(current_order.quantity)}\n"
            output += "--------------------\n"
            current_order = current_order.next
        return output

        


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
    def get_food_item_head(self, item_name):
        """
        Retrieves the head node of the linked queue associated with the given food item name.

        Args:
            item_name (str): The name of the food item.

        Returns:
            Node: The head node of the linked queue, or None if the food item is not found.
        """
        item_name_lower = item_name.lower()  # Convert item name to lowercase for case-insensitive comparison

        if self.contains(item_name_lower):
            food_item = self.get(item_name_lower)
            return food_item.food_chain.head

        return None


class Node:
    def __init__(self, customer_id, quantity, code):
        self.customer_id = customer_id
        self.quantity = quantity
        self.code = code
        self.next = None

class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, customer_id, quantity, code):
        new_node = Node(customer_id, quantity, code)
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
    def __init__(self):
        """
        Represents a food item required for production.

        Args:
            item_name (str): The name of the food item.
        """
        self.food_chain = LinkedQueue()

    def add_customer_order(self, customer_id, quantity, code):
        """
        Adds a customer's order for this food item.

        Args:
            customer_id (str): The ID of the customer.
            quantity (int): The quantity of the item.
        """
        self.food_chain.enqueue(customer_id, quantity, code)

    def remove_customer_order(self):
        self.food_chain.dequeue()

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


    def decrease_linked_queue(self, item_name):
        """
        Decreases the quantity of the first element in the linked queue associated with the given item name.

        Args:
            item_name (str): The name of the food item.
        """
        item_name_lower = item_name.lower()

        if self.food_items.contains(item_name_lower):
            food_item = self.food_items.get(item_name_lower)
            food_chain = food_item.food_chain

            if not food_chain.is_empty():
                removed_node = food_chain.dequeue()
                # Decrease the quantity of the first element
                removed_node.quantity = str(int(removed_node.quantity) + 1)

                # If the quantity becomes zero, you can remove the node from the linked queue if desired
                if removed_node.quantity == 0:
                    food_item.remove_customer_order()

    def update_quantity(self, item_name, quantity):
        """
        Updates the quantity of a food item in the food production department.

        Args:
            item_name (str): The name of the food item.
            quantity (int): The updated quantity.
        """
        item_name_lower = item_name.lower()  # Convert item name to lowercase for case-insensitive comparison

        if self.food_items.contains(item_name_lower):
            food_item = self.food_items.get(item_name_lower)
            food_item.quantity = quantity
            return food_item.quantity




    def enqueue_customer_order(self, customer_id, item_name, quantity, code):
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
            food_item.add_customer_order(customer_id, quantity, code)
        else:
            food_item = FoodItem()
            food_item.add_customer_order(customer_id, quantity, code)
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
                    
                    current_node = food_item.food_chain.head
                    if current_node:
                        print(f"{item_name} ->", end="")
                    while current_node and current_node.next:
                        print(f" ({current_node.customer_id},{current_node.quantity})", end=",")
                        current_node = current_node.next
                    if current_node:
                        print(f" ({current_node.customer_id},{current_node.quantity})")
    
    def get_food_items(self):
        """
        Retrieves the food items and their associated customer orders from the FoodProductionDepartment.

        Returns:
            list: A list of dictionaries containing the item_name and quantity for each food item.
        """
        food_items = []

        # Access the food_items HashMap in the FoodProductionDepartment
        food_items_map = self.food_items

        # Iterate over each bucket in the HashMap
        for bucket in food_items_map.buckets:
            if bucket is not None:
                for item_name, food_item in bucket:
                    # Create a dictionary for each food item and its associated customer orders
                    food_item_data = {
                        'item_name': item_name,
                        'quantity': 0  # Initialize the quantity
                    }

                    # Access the food_chain LinkedQueue in the FoodItem
                    food_chain = food_item.food_chain

                    # Iterate over each Node in the LinkedQueue
                    current_node = food_chain.head
                    while current_node:
                        # Increment the quantity for each customer order
                        food_item_data['quantity'] = int(food_item_data['quantity']) + int(current_node.quantity)
                        current_node = current_node.next

                    # Append the food item data to the list
                    food_items.append(food_item_data)

        return food_items


class CustomerQueue:
    def __init__(self):
        """Represents a nested linked queue of customers and their orders."""
        self.head = None
        self.tail = None
        self.food_production_department = FoodProductionDepartment()
        self.size = 0
        self.count = 0
        self.pos = None

    def is_empty(self):
        """Checks if the nested linked queue is empty."""
        return self.head is None

    def enqueue_customer(self, customer_id, option, payment, verification):
        """
        Adds a new customer to the nested linked queue.

        Args:
            customer_id (str): The ID of the customer.
        """
        new_customer = Customer(customer_id, option=option, payment=payment, verification=verification)
        if self.is_empty():
            self.head = new_customer
            self.tail = new_customer
        else:
            self.tail.next = new_customer
            self.tail = new_customer
        self.size += 1

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
                current_order.quantity,
                removed_customer.verification
            )
            current_order = current_order.next

        self.size -= 1

        return removed_customer

    def getCustomerNode(self, customer_id):
        cur = self.head
        while cur:
            if cur.customer_id == customer_id:
                return cur
            cur = cur.next
        return None
    
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
                current_order = current_customer.order_head
                while current_order:
                    if current_order.item_name == item_name:
                        # If the food item already exists, increase the quantity
                        current_order.quantity = int(current_order.quantity) + int(quantity)
                        return
                    current_order = current_order.next

                # If the food item doesn't exist, add a new order node
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
        output = ""
        while current_customer:
            output += f"Customer ID:, {current_customer.customer_id}\n"
            output += "Your Orders:\n"
            current_order = current_customer.order_head
            while current_order:
                output += f"Item Name:, {current_order.item_name}\n"
                output += f"Quantity:, {current_order.quantity}\n"
                output += f"Price:, {int(current_order.price)*int(current_order.quantity)}\n"
                output += "--------------------\n"
                current_order = current_order.next
            current_customer = current_customer.next
        return output

# Testing the code

if __name__ == "__main__":
    # Create the customer queue
    queue = CustomerQueue()

    # Add customers to the queue
    queue.enqueue_customer("C1", "Option 1", "Payment 1", "Verification 1")
    queue.enqueue_customer("C2", "Option 2", "Payment 2", "Verification 2")

    # Add orders for customers
    queue.add_order("C1", "Burger", 2, 500)
    queue.add_order("C1", "Burger", 2, 500)
    queue.add_order("C1", "Pizza", 1, 80)
    queue.add_order("C2", "Pizza", 3, 60)
    queue.add_order("C2", "Burger", 2, 60)
    queue.add_order("C2", "Ice Cream", 2, 40)

    # Display customers and their orders from the queue
    print("Customers and their orders from the queue:")
    queue.display_customers()
    print()

    # Dequeue a customer from the queue
    removed_customer = queue.dequeue_customer()
    if removed_customer:
        print("Customer removed from the queue:", removed_customer.customer_id)
    print()

    removed_customer = queue.dequeue_customer()
    if removed_customer:
        print("Customer removed from the queue:", removed_customer.customer_id)
    print()

    # Display food items and associated customer orders after customer removal
    print("Food items and their associated customer orders:")
    food_items = queue.food_production_department.get_food_items()
    for item in food_items:
        print(f"Item Name: {item['item_name']}")
        print(f"Quantity: {item['quantity']}")
        print("--------------------")
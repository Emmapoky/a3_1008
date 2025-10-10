# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from data_structures import List, ArrayR

class Order:
    def __init__(self, hunger: int, location: tuple[float, float]):
        """
            Constructor for Order.
            No analysis required.
        """
        self.hunger = hunger
        self.location = location
        self.distance = None
        
        
    def __str__(self):
        return "Order <???>"
    
    
class OrderDispatch:
    def __init__(self, dispatch_location: tuple[float, float], max_orders: int):
        """
            Constructor for OrderDispatch.
            Complexity Analysis:
            ...
        """
        pass
    
    
    def __len__(self):
        """
            Return the number of pending orders in the dispatch system.
            No analysis required.
        """
        pass
        
    
    def receive_order(self, order: Order):
        """
            Receive a new Food Flight order into the dispatch system.
            Complexity Analysis:
            ...
        """
        pass
        
    
    def deliver_single(self) -> Order:
        """
            Deliver a single pending order with the lowest
            FoodFast (TM) score.
            See specifications for details.
            Complexity Analysis:
            ...
        """
        pass
        
    
    def deliver_multiple(self, max_travel: float) -> List[Order]:
        """
            Deliver as many orders, prioritising orders such that
            lower FoodFast (TM) scores are delivered first.
            See specifications for details.
            Complexity Analysis:
            ...
        """
        pass
        

    def order_surge_1054(self, surge_batch: ArrayR[Order]):
        """
            Add all orders from surge batch, ensuring this is done as
            efficiently as possible to minimise downtime.
            Complexity Analysis:
            ...
        """
        pass


if __name__ == "__main__":
    # Test your code here

    # Let's create a dispatch and a few orders
    dispatch_location = (2, 3)
    dispatch = OrderDispatch(dispatch_location, max_orders=10)
    
    first_orders = [
        Order(3, (5, 6)),
        Order(4, (6, 4)),
        Order(1, (4, 4))
    ]
    
    second_orders = [
        Order(7, (-4, 3)),
        Order(10, dispatch_location), # Someone ordered FROM the dispatch!
        Order(5, (0, 5))
    ]
    
    for order in first_orders:
        dispatch.receive_order(order)
        
    # Dispatch an order
    first_dispatched = dispatch.deliver_single()
    
    print("1st dispatch:", first_dispatched)
    
    # Now we add the second collection
    for order in second_orders:
        dispatch.receive_order(order)
        
    # Let's see what gets delivered now
    second_dispatched = dispatch.deliver_single()
    
    print("2nd dispatch:", second_dispatched)

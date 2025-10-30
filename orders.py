# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Tuple, Optional

from data_structures.array_max_heap import ArrayMaxHeap
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR

class Order:
    def __init__(self, hunger: int, location: Tuple[float, float]) -> None:
        self.hunger = hunger
        self.location = location
        self.distance: Optional[float] = None #added float

    def __str__(self) -> str:
        readable_distance = "?" if self.distance is None else f"{self.distance:.3f}"
        return f"Order(h={self.hunger}, loc={self.location}, d={readable_distance})"
    
class OrderDispatch:
    def __init__(self, dispatch_location: Tuple[float, float], max_orders: int) -> None:
        """
            Constructor for OrderDispatch.
            Complexity Analysis:
            ...
        """
        self._dispatch = dispatch_location
        self._capacity = max_orders
        self._pending: ArrayMaxHeap[tuple[float, int, Order]] = ArrayMaxHeap(max_orders)
        self._tie_counter = 0

    def _distance_from_dispatch(self, point: Tuple[float, float]) -> float:
        return math.hypot(point[0] - self._dispatch[0], point[1] - self._dispatch[1])
    
    def _foodfast(self, distance_value: float, hunger_value: int) -> float:
        return 4.0 * distance_value - 5.0 * hunger_value

    def receive_order(self, order: Order) -> None:
        if len(self._pending) == self._capacity:
            raise Exception("Dispatch at capacity")
        order.distance = self._distance_from_dispatch(order.location)
        score = self._foodfast(order.distance, order.hunger)
        self._pending.add((-score, self._tie_counter, order))
        self._tie_counter += 1
    
    def __len__(self) -> int:
        """
        Number of orders currently waiting.

        Complexity:
        Best and worst: O(1). Heap stores its length.
        """
        return len(self._pending)
    
    def deliver_single(self) -> Order:
        if len(self._pending) == 0:
            raise Exception("No pending orders")
        _, _, next_order = self._pending.extract_root()
        return next_order
        
    
    def deliver_multiple(self, max_travel: float) -> List[Order]:
        """
            Deliver as many orders, prioritising orders such that
            lower FoodFast (TM) scores are delivered first.
            See specifications for details.
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

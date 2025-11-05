# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/

# Context: Feel free to check these for my thought process and implementation notes.
# Github: https://github.com/Emmapoky/a3_1008
# Notes:  https://drive.google.com/file/d/1Tl1zwuZxAvG8mrH47QbRnYfGvCR3fv2B/view?usp=sharing

from functools import total_ordering
import math

from typing import Tuple

from data_structures.array_max_heap import ArrayMaxHeap
from data_structures.array_list import ArrayList

class Order:
    def __init__(self, hunger: int, location: Tuple[float, float]) -> None:
        """
        :complexity: The best case and also worst case is O(1).
        We store hunger and location, set distance to None, and finish 
        without any loops or extra data structure work.
        """
        self.hunger = hunger
        self.location = location
        self.distance = None

    def __str__(self) -> str:
        """
        :complexity: The best case and also worst case is O(1).
        We format a short string from the existing fields, which does not depend 
        on the number of orders.
        """
        readable_distance = "?" if self.distance is None else f"{self.distance:.3f}"
        return f"Order(h={self.hunger}, loc={self.location}, d={readable_distance})"
    
class OrderDispatch:
    def __init__(self, dispatch_location: Tuple[float, float], max_orders: int) -> None:
        """
        :complexity: The best case and also worst case is O(1).
        We record the dispatch point and capacity, create an empty heap, 
        and reset the tie counter, with no work that grows with input size.
        """
        self._dispatch = dispatch_location
        self._capacity = max_orders
        self._pending = ArrayMaxHeap(max_orders)
        self._tie_counter = 0

    def _distance_from_dispatch(self, point: Tuple[float, float]) -> float:
        """
        :complexity: The best case and also worst case is O(1).
        We evaluate one straight‑line distance between two points using a fixed number of arithmetic operations.
        """
        return math.hypot(point[0] - self._dispatch[0], point[1] - self._dispatch[1])
    
    def _foodfast(self, distance_value: float, hunger_value: int) -> float:
        """
        :complexity: The best case and also worst case is O(1).
        We evaluate a single linear formula: 4 * distance − 5 * hunger using constannt work.
        """
        return 4.0 * distance_value - 5.0 * hunger_value

    def receive_order(self, order: Order) -> None:
        """
        :complexity: Best and Worst are both O(log n), where n is the number of waiting orders. 
        We set the order’s distance in O(1), compute its priority in O(1), and add it 
        to the heap, which takes time which is proportional to the heap height O(logn).​
        """
        if len(self._pending) == self._capacity:
            raise Exception("Dispatch at capacity")
        order.distance = self._distance_from_dispatch(order.location)
        score = self._foodfast(order.distance, order.hunger)
        self._pending.add((-score, self._tie_counter, order))
        self._tie_counter += 1
    
    def __len__(self) -> int:
        """
        :complexity: The best case and also worst case is O(1).
        We return the current number of items in the heap, which is stored by the data structure.
        """
        return len(self._pending)
    
    def deliver_single(self) -> Order:
        """
        :complexity: Best and Worst are both O(log n), where n is the number of waiting orders.
        We check for emptiness and remove the top‑priority order from the heap, 
        and one heap extract takes time proportional to the heap height.
        """
        if len(self._pending) == 0:
            raise Exception("No pending orders")
        _, _, next_order = self._pending.extract_root()
        return next_order
        
    
    def deliver_multiple(self, max_travel: float) -> ArrayList[Order]:
        """
        :complexity: Best and Worst are both O(k log n), where n is the number of waiting orders and 
        k is the number of orders delivered in this call. 
        
        We can exit early if the single best order cannot be completed within the travel limit; 
        otherwise, each accepted order does a constant amount of distance and feasibility checks 
        plus one heap extract, so the total is k extracts at O(logn) each.​
        """
        delivered = ArrayList()
        if len(self._pending) == 0:
            return delivered

        _, _, first_best = self._pending.peek()
        if 2.0 * float(first_best.distance) > max_travel:
            return delivered

        current_position = self._dispatch
        path_without_return = 0.0

        while len(self._pending) > 0:
            _, _, candidate = self._pending.peek()
            leg_to_candidate = math.hypot(candidate.location[0] - current_position[0],
                                          candidate.location[1] - current_position[1])
            trip_if_taken = path_without_return + leg_to_candidate + self._distance_from_dispatch(candidate.location)

            if trip_if_taken <= max_travel:
                self._pending.extract_root()
                delivered.append(candidate)
                path_without_return += leg_to_candidate
                current_position = candidate.location
            else:
                break

        return delivered

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

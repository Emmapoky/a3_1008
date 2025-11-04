# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/

# Context: Feel free to check these for my thought process and implementation notes.
# Github: https://github.com/Emmapoky/a3_1008
# Notes:  https://drive.google.com/file/d/1Tl1zwuZxAvG8mrH47QbRnYfGvCR3fv2B/view?usp=sharing

from functools import total_ordering
import math

from typing import Tuple, Optional

from data_structures.array_max_heap import ArrayMaxHeap
from data_structures.array_list import ArrayList

class Order:
    def __init__(self, hunger: int, location: Tuple[float, float]) -> None:
        """
        :complexity: The best case and also worst case is O(1).
        We save the dispatch info and create an empty heap (no elements to rearrange).
        """
        self.hunger = hunger
        self.location = location
        self.distance = None

    def __str__(self) -> str:
        """
        :complexity: The best case and also worst case is O(1).
        We build a small string from existing fields; no loops are involved.
        """
        readable_distance = "?" if self.distance is None else f"{self.distance:.3f}"
        return f"Order(h={self.hunger}, loc={self.location}, d={readable_distance})"
    
class OrderDispatch:
    def __init__(self, dispatch_location: Tuple[float, float], max_orders: int) -> None:
        """
        :complexity: The best case and also worst case is O(1).
        We save the dispatch info and create an empty heap (no elements to rearrange).
        """
        self._dispatch = dispatch_location
        self._capacity = max_orders
        self._pending = ArrayMaxHeap(max_orders)
        self._tie_counter = 0

    def _distance_from_dispatch(self, point: Tuple[float, float]) -> float:
        """
        :complexity: The best case and also worst case is O(1).
        One hypot call (fixed amount of math).
        """
        return math.hypot(point[0] - self._dispatch[0], point[1] - self._dispatch[1])
    
    def _foodfast(self, distance_value: float, hunger_value: int) -> float:
        """
        :complexity: The best case and also worst case is O(1).
        A single formula with a constant number of operations:
        
        FoodFast score is 4*distance - 5*hunger. Smaller scores have higher priority.
        """
        return 4.0 * distance_value - 5.0 * hunger_value

    def receive_order(self, order: Order) -> None:
        """
        :complexity: Best = Worst = O(log n), with n = current waiting orders.
        Reason: set distance (O(1)), compute score (O(1)), and add to the heap.
        Heap add “bubbles up” along the heap’s height, which grows like log n.
        """
        if len(self._pending) == self._capacity:
            raise Exception("Dispatch at capacity")
        order.distance = self._distance_from_dispatch(order.location)
        score = self._foodfast(order.distance, order.hunger)
        self._pending.add((-score, self._tie_counter, order))
        self._tie_counter += 1
    
    def __len__(self) -> int:
        """
        :complexity: The best case and also worst case is 0(1).
        We return a stored count; it doesn’t depend on n beyond reading a number.
        """
        return len(self._pending)
    
    def deliver_single(self) -> Order:
        """
        :complexity: Best = Worst = O(log n), with n = current waiting orders.
        Reason: one heap extract moves elements down the heap by about its height (log n).
        """
        if len(self._pending) == 0:
            raise Exception("No pending orders")
        _, _, next_order = self._pending.extract_root()
        return next_order
        
    
    def deliver_multiple(self, max_travel: float) -> ArrayList[Order]:
        """
        :complexity: Best = Worst = O(k log n), with
        n = current waiting orders and k = delivered now.
        Reason: for each accepted order we do a constant amount of distance checks
        and one heap extract (log n). There are at most k accepts before the trip stops.

        Steps:
        - If the best one alone cannot be delivered and returned, return empty.
        - Otherwise, keep taking the next best as long as the total trip stays within the limit.
        - Stop when the next candidate would make the trip too long or when the heap is empty.
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

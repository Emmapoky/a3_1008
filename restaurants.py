# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Iterator, Optional, Union
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining

from better_bst import BetterBinarySearchTree

from algorithms import mergesort, merge

class MenuItem:
    def __init__(self, name: str, rating: int) -> None:
        """
        :complexity: Best = Worst = O(1).
        We simply store two fields and return; no loops or ADT operations scale with input size.
        """
        self.name = name
        self.rating = rating

    def __eq__(self, other: object) -> bool:
        """
        :complexity: Best = Worst = O(1).
        Equality checks two primitives (int and str references) once; no iteration occurs.
        """
        if not isinstance(other, MenuItem):
            return False
        return self.rating == other.rating and self.name == other.name

    def __lt__(self, other: "MenuItem") -> bool:
        """
        :complexity: Best = Worst = O(1).
        We compare ratings once; on ties we compare names once to impose a total order for sorting/merging.
        """
        if self.rating != other.rating:
            return self.rating > other.rating
        return self.name < other.name

    def __str__(self) -> str:
        """
        :complexity: Best = Worst = O(1).
        String formatting on fixed-size fields is constant-time under assignment assumptions.
        """
        return f"{self.name} ({self.rating})"

class Restaurant:
    def __init__(self, name: str, block: int, initial_menu: ArrayR[MenuItem]) -> None:
        """
        :complexity: Best = Worst = O(n log n) to sort + O(n) to store, where n = len(initial_menu).
        We sort the incoming array once with mergesort, then append each item into an ArrayList once.
        """
        self.name = name
        self.block = block
        sorted_initial = mergesort(initial_menu, key=lambda item: (-item.rating, item.name))
        self._menu = ArrayList()
        for index in range(len(sorted_initial)):
            self._menu.append(sorted_initial[index])
    
    def __str__(self) -> str:
        """
        :complexity: Best = Worst = O(1).
        Constructing a short label string is constant-time in this context.
        """
        return f"Restaurant(name={self.name}, block={self.block})"

    def _merge_sorted_inplace(self, extra_sorted: ArrayList[MenuItem]) -> None:
        """
        :complexity: Best = Worst = O(n + m), where n = current menu size and m = len(extra_sorted).
        We merge two already-sorted lists once; the scaffold merge visits each list exactly once.
        """
        merged_view = merge(self._menu, extra_sorted, key=lambda item: (-item.rating, item.name))

        new_menu = ArrayList()
        for index in range(len(merged_view)):
            new_menu.append(merged_view[index])
        self._menu = new_menu

    def get_menu_ref(self) -> ArrayList[MenuItem]:
        """
        :complexity: Best = Worst = O(1).
        We return a reference to our already-sorted internal list; no copying or traversal occurs.
        """
        return self._menu

class FoodFlight:
    def __init__(self) -> None:
        """
        :complexity: Best = Worst = O(1).
        Construct two empty indexes: a hash table by name and a BST by block; nothing scales here.
        """
        self._name_index = HashTableSeparateChaining()
        self._block_index = BetterBinarySearchTree[int, Restaurant]()

    def add_restaurant(self, restaurant: Restaurant) -> None:
        """
        :complexity: Best = Worst = O(L + log R), where L = len(restaurant.name) and R = current count.
        We compute the string hash once (O(L)) and insert by block into a BST in O(log R) assuming balanced behavior by rubric.
        """
        self._name_index[restaurant.name] = restaurant
        self._block_index[restaurant.block] = restaurant

    def get_menu(self, restaurant_name: str) -> Union[ArrayR[MenuItem], ArrayList[MenuItem]]:
        """
        :complexity: Best = Worst = O(L), where L = len(restaurant_name).
        We hash the string (O(L)) and return the stored menu by reference in O(1); missing names raise KeyError in O(1).
        """
        if restaurant_name not in self._name_index:
            raise KeyError("Restaurant not found")
        return self._name_index[restaurant_name].get_menu_ref()

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]) -> None:
        """
        :complexity: Best = Worst = O(L + m log m + n + m), where
        L = len(restaurant_name), n = current menu size, and m = number of new items.
        Lookup by name costs O(L), sorting the new batch is O(m log m), and a single linear merge is O(n + m).
        """
        if restaurant_name not in self._name_index:
            raise KeyError("Restaurant not found")
        restaurant_ref = self._name_index[restaurant_name]

        buffer_new = ArrayList()
        for index in range(len(new_items)):
            buffer_new.append(new_items[index])

        sorted_new_view = mergesort(buffer_new, key=lambda item: (-item.rating, item.name))

        sorted_new_list = ArrayList()
        for index in range(len(sorted_new_view)):
            sorted_new_list.append(sorted_new_view[index])

        restaurant_ref._merge_sorted_inplace(sorted_new_list)
    
    def meal_suggestions(self, my_block: int, max_walk: int) -> Iterator[MenuItem]:
        """
        :complexity: Total over all yielded items = O(n * R), where
        R = number of restaurants in [my_block - max_walk, my_block + max_walk]
        and n = total items across those restaurants.
        Each next() scans up to R heads to pick the best by MenuItem order, and we do that n times.
        """
        low_block = my_block - max_walk
        high_block = my_block + max_walk
        in_range_restaurants: ArrayList[Restaurant] = self._block_index.range_query(low_block, high_block)

        menus_in_range = ArrayList()
        for restaurant_index in range(len(in_range_restaurants)):
            menus_in_range.append(in_range_restaurants[restaurant_index].get_menu_ref())

        cursors_by_menu = ArrayList()
        for _ in range(len(menus_in_range)):
            cursors_by_menu.append(0)

        class SuggestIter:
            def __init__(self, menus_ref: ArrayList[ArrayList[MenuItem]], cursors_ref: ArrayList[int]) -> None:
                self._menus = menus_ref
                self._cursors = cursors_ref
                self._last_menu = -1
                self._current_rating: Optional[int] = None
                self._served_once = set()  # menus served once at current best rating

            def __iter__(self) -> "SuggestIter":
                return self

            def __next__(self) -> MenuItem:
                # gather heads
                heads = []
                for m in range(len(self._menus)):
                    pos = self._cursors[m]
                    menu_ref = self._menus[m]
                    if pos < len(menu_ref):
                        heads.append((m, menu_ref[pos]))
                if not heads:
                    raise StopIteration

                # best rating among heads
                best_rating = max(item.rating for _, item in heads)

                # new round when rating changes
                if self._current_rating != best_rating:
                    self._current_rating = best_rating
                    self._served_once.clear()

                # heads at best rating
                top = [(i, it) for (i, it) in heads if it.rating == best_rating]

                # prefer menus not yet served once at this rating
                pool = [(i, it) for (i, it) in top if i not in self._served_once]
                if not pool:
                    self._served_once.clear()
                    pool = top

                # avoid immediate repeat if possible
                alt = [(i, it) for (i, it) in pool if i != self._last_menu]
                if alt:
                    pool = alt

                # pick lexicographically smallest name
                chosen_i, chosen_item = min(pool, key=lambda t: t[1].name)

                # advance and mark
                self._cursors[chosen_i] = self._cursors[chosen_i] + 1
                self._served_once.add(chosen_i)
                self._last_menu = chosen_i
                return chosen_item

        return SuggestIter(menus_in_range, cursors_by_menu)

if __name__ == "__main__":
    # Test your code here
    
    # First restaurant with no initial menu items
    first_restaurant = Restaurant("Testaurant", 3, ArrayR(0))
    
    # Add to the FF app
    ff = FoodFlight()

    ff.add_restaurant(first_restaurant)
    
    # Add to Testaurant's menu
    new_items = ArrayR(3)
    new_items[0] = MenuItem("Chips", 2)
    new_items[1] = MenuItem("Pizza", 4)
    new_items[2] = MenuItem("Burger", 3)
    
    ff.add_to_menu("Testaurant", new_items)
    
    # Get the best item from the menu
    print("Best menu item:", ff.get_menu("Testaurant")[0])
    


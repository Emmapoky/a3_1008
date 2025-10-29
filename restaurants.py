# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Iterator, Optional, Union
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR
from data_structures.binary_search_tree import BinarySearchTree, K, V
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from better_bst import BetterBinarySearchTree
from algorithms import mergesort, merge

class MenuItem:
    def __init__(self, name: str, rating: int) -> None:
        self.name = name
        self.rating = rating

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MenuItem):
            return False
        return self.rating == other.rating and self.name == other.name

    def __lt__(self, other: "MenuItem") -> bool:
        if self.rating != other.rating:
            return self.rating > other.rating
        return self.name < other.name

    def __str__(self) -> str:
        return f"{self.name} ({self.rating})"

class Restaurant:
    def __init__(self, name: str, block: int, initial_menu: ArrayR[MenuItem]) -> None:
        """
        Complexity:
        Let n be the number of items in initial_menu.
        Best and worst: O(n log n) due to mergesort.
        """
        self.name = name
        self.block = block
        sorted_initial = mergesort(initial_menu, key=lambda item: (-item.rating, item.name))
        self._menu: ArrayList[MenuItem] = ArrayList()
        for index in range(len(sorted_initial)):
            self._menu.append(sorted_initial[index])
    
    def __str__(self) -> str:
        return f"Restaurant(name={self.name}, block={self.block})"

    def _merge_sorted_inplace(self, extra_sorted: ArrayList[MenuItem]) -> None:
        """
        Merge another already-sorted-by-our-order list into self._menu via scaffold 'merge'.

        Complexity:
        Let n be the current menu length and m be the number of items in extra_sorted.
        Best and worst: O(n + m).
        Reason: both inputs are already sorted by the same rule, so the scaffold merge function walks each list once and builds the result in linear time. 
        """
        merged_view = merge(self._menu, extra_sorted, key=lambda item: (-item.rating, item.name))

        # This keep ArrayList INTERNAL 
        new_menu: ArrayList[MenuItem] = ArrayList()
        for index in range(len(merged_view)):
            new_menu.append(merged_view[index])
        self._menu = new_menu

    def get_menu_ref(self) -> ArrayList[MenuItem]:
        """
        Return the internal, already-sorted menu by reference.

        Complexity:
        Best and worst: O(1).
        Reason: returns a reference to the stored menu without copying. 
        """
        return self._menu

class FoodFlight:
    def __init__(self) -> None:
        self._name_index = HashTableSeparateChaining()
        self._block_index = BetterBinarySearchTree[int, Restaurant]()

    def add_restaurant(self, restaurant: Restaurant) -> None:
        self._name_index[restaurant.name] = restaurant
        self._block_index[restaurant.block] = restaurant

    def get_menu(self, restaurant_name: str) -> Union[ArrayR[MenuItem], ArrayList[MenuItem]]:
        if restaurant_name not in self._name_index:
            raise KeyError("Restaurant not found")
        return self._name_index[restaurant_name].get_menu_ref()

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]) -> None:
        if restaurant_name not in self._name_index:
            raise KeyError("Restaurant not found")
        restaurant_ref = self._name_index[restaurant_name]

        buffer_new: ArrayList[MenuItem] = ArrayList()
        for index in range(len(new_items)):
            buffer_new.append(new_items[index])

        sorted_new_view = mergesort(buffer_new, key=lambda item: (-item.rating, item.name))

        sorted_new_list: ArrayList[MenuItem] = ArrayList()
        for index in range(len(sorted_new_view)):
            sorted_new_list.append(sorted_new_view[index])

        restaurant_ref._merge_sorted_inplace(sorted_new_list)
    
    def meal_suggestions(self, my_block: int, max_walk: int) -> Iterator[MenuItem]:
        """
        Complexity:
        Let R' be in-range restaurants, n' be total items among them.
        Best and worst: O(n' · R') across all yields.
        """
        low_block = my_block - max_walk
        high_block = my_block + max_walk
        in_range_restaurants: ArrayList[Restaurant] = self._block_index.range_query(low_block, high_block)

        menus_in_range: ArrayList[ArrayList[MenuItem]] = ArrayList()
        for restaurant_index in range(len(in_range_restaurants)):
            menus_in_range.append(in_range_restaurants[restaurant_index].get_menu_ref())

        cursors_by_menu: ArrayList[int] = ArrayList()
        for _ in range(len(menus_in_range)):
            cursors_by_menu.append(0)

        class SuggestIter:
            def __init__(self, menus_ref: ArrayList[ArrayList[MenuItem]], cursors_ref: ArrayList[int]) -> None:
                self._menus = menus_ref
                self._cursors = cursors_ref

            def __iter__(self) -> "SuggestIter":
                return self

            def __next__(self) -> MenuItem:
                best_menu_index = -1
                best_candidate: Optional[MenuItem] = None
                for menu_index in range(len(self._menus)):
                    cursor_position = self._cursors[menu_index]
                    menu_ref = self._menus[menu_index]
                    if cursor_position < len(menu_ref):
                        candidate_item = menu_ref[cursor_position]
                        if best_candidate is None or candidate_item < best_candidate:
                            best_candidate = candidate_item
                            best_menu_index = menu_index
                if best_menu_index == -1:
                    raise StopIteration
                self._cursors[best_menu_index] = self._cursors[best_menu_index] + 1
                return best_candidate  # type: ignore

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
    

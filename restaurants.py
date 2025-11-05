# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/

# Context: Feel free to check these for my thought process and implementation notes.
# Notes:  https://drive.google.com/file/d/1Tl1zwuZxAvG8mrH47QbRnYfGvCR3fv2B/view?usp=sharing

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
        :complexity: The best case and also worst case is O(1).
        We store the name and rating in fields and return, with no loops or calls that grow with input size.
        """
        self.name = name
        self.rating = rating

    def __eq__(self, other: object) -> bool:
        """
        :complexity: The best case and also worst case is O(1).
        We check the type once and compare the rating and name once, with no iteration over data structures.
        """
        if not isinstance(other, MenuItem):
            return False
        return self.rating == other.rating and self.name == other.name

    def __lt__(self, other: "MenuItem") -> bool:
        """
        :complexity: The best case and also worst case is O(1).
        We compare ratings once, and only if they are equal we compare names once to break ties, 
        which is constant under the assignment’s assumptions.
        """
        if self.rating != other.rating:
            return self.rating > other.rating
        return self.name < other.name

    def __str__(self) -> str:
        """
        :complexity: The best case and also worst case is O(1).
        We build a short string from fixed fields without any loops.
        """
        return f"{self.name} ({self.rating})"

class Restaurant:
    def __init__(self, name: str, block: int, initial_menu: ArrayR[MenuItem]) -> None:
        """
        :complexity: Best and Worst are both O(n log n) to sort + O(n) to store, where 
        n is the number of initial items.
        We sort the given menu once using mergesort and then copy the sorted items 
        into our ArrayList in one pass.
        """
        self.name = name
        self.block = block
        sorted_initial = mergesort(initial_menu, key=lambda item: (-item.rating, item.name))
        self._menu = ArrayList()
        for index in range(len(sorted_initial)):
            self._menu.append(sorted_initial[index])
    
    def __str__(self) -> str:
        """
        :complexity: The best case and also worst case is O(1).
        Constructing a short label string is constant-time.
        """
        return f"Restaurant(name={self.name}, block={self.block})"

    def _merge_sorted_inplace(self, extra_sorted: ArrayList[MenuItem]) -> None:
        """
        :complexity: Best and Worst are both O(n + m), where n is the current menu size and 
        m is the size of the new sorted list.
        We do a single linear merge of two already‑sorted sequences, then copy the merged 
        view into a new ArrayList in one pass.
        """
        merged_view = merge(self._menu, extra_sorted, key=lambda item: (-item.rating, item.name))

        new_menu = ArrayList()
        for index in range(len(merged_view)):
            new_menu.append(merged_view[index])
        self._menu = new_menu

    def get_menu_ref(self) -> ArrayList[MenuItem]:
        """
        :complexity: The best case and also worst case is O(1).
        We return a reference to the internal sorted menu without copying or scanning it.
        """
        return self._menu

class FoodFlight:
    def __init__(self) -> None:
        """
        :complexity: The best case and also worst case is O(1).
        We create an empty hash table for names and an empty BST for blocks, with no work that 
        scales with input size.
        """
        self._name_index = HashTableSeparateChaining()
        self._block_index = BetterBinarySearchTree[int, Restaurant]()

    def add_restaurant(self, restaurant: Restaurant) -> None:
        """
        :complexity: Best & Worst are both O(L + log R), where L is the length of the restaurant name 
        and R is the number of restaurants stored.
        We hash the name once (cost depends on L and insert the restaurant into the BST by block; 
        in a well‑shaped tree this is O(logR), while in a very skewed tree it can be O(R).
        """
        self._name_index[restaurant.name] = restaurant
        self._block_index[restaurant.block] = restaurant

    def get_menu(self, restaurant_name: str) -> ArrayList[MenuItem]:
        """
        :complexity: Best and Worst are both O(L), where L is the length of the name.
        We hash the name to find the restaurant and then return the menu reference in constant time; 
        missing names raise a KeyError after the same hash cost.
        """
        if restaurant_name not in self._name_index:
            raise KeyError("Restaurant not found")
        return self._name_index[restaurant_name].get_menu_ref()

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]) -> None:
        """
        :complexity: Best & Worst are O(L + m log m + n + m), where L is the length of the name, 
        n is the current menu size, and m is the number of new items. 
        We hash the name once, sort the new items with mergesort in O(mlogm), and perform one 
        linear merge of sizesn n & m.
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
        :complexity: Total over all yielded items is O(n * R), where R is the number of restaurants 
        with blocks in [my_block − max_walk, my_block + max_walk] and n is the total number of items across 
        those restaurants. 
        Each call to next() scans up to R heads to find the best rating and pick the next item by 
        name tie‑break, and this repeats until all n items have been yielded.​
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
                """
                :complexity: Best is O(R) and worst is O(R), where R is the number of in‑range restaurants. 
                We allocate one boolean flag per menu to track whether it has been served in the current rating round.​
                """ 
                self._menus = menus_ref
                self._cursors = cursors_ref
                self._last_menu = -1
                self._current_rating: Optional[int] = None
                self._served_once = ArrayList()
                for _ in range(len(self._menus)):
                    self._served_once.append(False)

            def __iter__(self) -> "SuggestIter":
                return self

            def __next__(self) -> MenuItem:
                """
                :complexity: Best is O(R) per yielded item and worst is O(R) per yielded item, where 
                R is the number of in‑range restaurants. 
                
                We scan menu heads to find the best rating, reset a round when the rating changes, 
                filter menus not yet served at that rating, dodging/avoiding immediate repeats when possible, 
                and pick the smallest name among the remaining choices, all these steps touch at 
                most R indices once per yield.​
                """
                # find best rating among available heads 
                any_head = False
                best_rating: Optional[int] = None
                for m in range(len(self._menus)):
                    pos = self._cursors[m]
                    menu_ref = self._menus[m]
                    if pos < len(menu_ref):
                        any_head = True
                        r = menu_ref[pos].rating
                        if best_rating is None or r > best_rating:
                            best_rating = r
                if not any_head:
                    raise StopIteration

                # reset per-rating round
                if self._current_rating != best_rating:
                    self._current_rating = best_rating
                    for i in range(len(self._served_once)):
                        self._served_once[i] = False

                # collect indices at best rating
                top_idx = ArrayList()
                for m in range(len(self._menus)):
                    pos = self._cursors[m]
                    menu_ref = self._menus[m]
                    if pos < len(menu_ref) and menu_ref[pos].rating == best_rating:
                        top_idx.append(m)

                # prefer indices not served in this round
                pool_idx = ArrayList()
                for j in range(len(top_idx)):
                    i = top_idx[j]
                    if not self._served_once[i]:
                        pool_idx.append(i)
                if len(pool_idx) == 0:
                    for i in range(len(self._served_once)):
                        self._served_once[i] = False
                    pool_idx = top_idx  # reuse the same ArrayList reference

                # avoid immediate repeat if possible
                candidate_idx = ArrayList()
                for j in range(len(pool_idx)):
                    i = pool_idx[j]
                    if i != self._last_menu:
                        candidate_idx.append(i)
                if len(candidate_idx) > 0:
                    pool_idx = candidate_idx

                # pick the smallest name among pool_idx
                chosen_i = pool_idx[0]
                chosen_name = self._menus[chosen_i][self._cursors[chosen_i]].name
                for j in range(1, len(pool_idx)):
                    i = pool_idx[j]
                    name_i = self._menus[i][self._cursors[i]].name
                    if name_i < chosen_name:
                        chosen_i = i
                        chosen_name = name_i

                # move forward and mark
                chosen_item = self._menus[chosen_i][self._cursors[chosen_i]]
                self._cursors[chosen_i] = self._cursors[chosen_i] + 1
                self._served_once[chosen_i] = True
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
    


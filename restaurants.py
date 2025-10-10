# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Iterator
from data_structures import ArrayR

class MenuItem:
    def __init__(self, name: str, rating: float):
        """
            Constructor for Restaurant.
            No analysis required.
        """
        self.name = name
        self.rating = rating
        
        
    def __str__(self):
        """
            String representation method for MenuItem class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"MenuItem <???>"
        


class Restaurant:
    def __init__(self, name: str, block_number: int, initial_menu: ArrayR[MenuItem]):
        """
            Constructor for Restaurant.
            Complexity Analysis:
            ...
        """
        self.name = name
        self.block_number = block_number
    
    
    def __str__(self):
        """
            String representation method for Restaurant class.
            Implementation optional - perhaps useful for debugging.
            No analysis required.
        """
        return f"Restaurant <???>"
        

class FoodFlight:
    def __init__(self):
        """
            Constructor for FoodFlight.
            Complexity Analysis:
            ...
        """
        pass
        
    
    def add_restaurant(self, restaurant: Restaurant):
        """
            Register a `restaurant` in the FoodFlight app.
            Complexity Analysis:
            ...
        """
        pass
        
    
    def get_menu(self, restaurant_name: str):
        """
            Return all menu items for a restaurant in decreasing order of their ratings.
            Complexity Analysis:
            ...
        """
        pass
        

    def add_to_menu(self, restaurant_name: str, new_items: ArrayR[MenuItem]):
        """
            Add an ArrayR of MenuItems to a Restaurant's menu.
            Complexity Analysis:
            ...
        """
        pass
    
    
    def meal_suggestions(self, user_block_number: int, max_walk: int) -> Iterator[MenuItem]:
        """
            Yield all menu items within max_walk blocks of the user's current block.
            Complexity Analysis (across all __next__ calls):
            ...
        """
        pass


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
    

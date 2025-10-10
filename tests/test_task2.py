from unittest import TestCase
import ast
import inspect
from data_structures.abstract_list import List
from data_structures.binary_search_tree import BinarySearchTree
from data_structures.hash_table_double_hashing import DoubleHashingTable
from data_structures.hash_table_linear_probing import LinearProbeTable
from data_structures.hash_table_quadratic_probing import QuadraticProbeTable
from data_structures.hash_table_separate_chaining import HashTableSeparateChaining
from data_structures.referential_array import ArrayR
from tests.helper import CollectionsFinder

from restaurants import FoodFlight, MenuItem, Restaurant

TEST_RESTAURANT_NAME = "Testaurant"

class TestTask2Setup(TestCase):
    pass

class TestTask2(TestTask2Setup):
    def test_foodflight_initial_menu(self):
        """
        #name(Test FoodFlight initial menu is retrievable)
        #hurdle
        """
        ff = FoodFlight()
        
        test_menu = ArrayR.from_list([
            MenuItem("Breakfast Muffin", 1),
            MenuItem("Pancakes", 3),
            MenuItem("French Toast", 2)
        ])
        
        # Add a restaurant with a test menu
        
        ff.add_restaurant(Restaurant(TEST_RESTAURANT_NAME, 3, test_menu))
        
        # Should be able to retrieve from FF object
        res_menu = ff.get_menu(TEST_RESTAURANT_NAME)
        
        self.assertIsNot(res_menu, None, "Got None when attempting to retrieve menu from FoodFlight app")
        self.assertEqual(len(res_menu), len(test_menu), "Length mismatch between initial menu and retrieved menu")
        
        
        
    def test_foodflight_menu_type(self):
        """
        #name(Test FoodFlight menu type)
        #hurdle
        """
        test_restaurant = Restaurant(
            "giraffis", 
            3,
            ArrayR(0)
        )
        
        ff = FoodFlight()
        
        ff.add_restaurant(test_restaurant)
        
        ff.add_to_menu('giraffis', ArrayR.from_list([
            MenuItem("Breakfast Muffin", 1),
            MenuItem("Vegetarian Focaccia", 4)
        ]))
        
        giraffis_menu = ff.get_menu('giraffis')
        
        self.assertTrue(isinstance(giraffis_menu, ArrayR) or isinstance(giraffis_menu, List), f"Restaurant's menu should be an ArrayR or List derivative (got {type(giraffis_menu)})")
        self.assertNotEqual(len(giraffis_menu), 0, "Restaurant's menu is empty, despite starting with 2 items")
        self.assertIsInstance(giraffis_menu[0], MenuItem, f"Restaurant's menu doesn't contain MenuItems (got {type(giraffis_menu[0])})")
    
    
    def test_foodflight_suggestion_type(self):
        """
        #name(Test FoodFlight suggestion type)
        #hurdle
        """
        ff = FoodFlight()
        
        suggestions_obj = ff.meal_suggestions(0, 1)
        
        self.assertTrue(hasattr(suggestions_obj, "__next__"), f"Suggestions method should always return an Iterator, but the returned object of type '{type(suggestions_obj)}' didn't have a __next__ method defined.")
    
    
            

class TestTask2Approach(TestTask2Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        #approach
        """
        import restaurants
        modules = [restaurants]

        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__
            
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            
            # Report any failures
            for failure in visitor.failures:
                self.fail(failure[3])
        
    
    @staticmethod
    def do_restaurant_inserts(n_rests: int):
        test_restaurants = [
            Restaurant(
                TestTask2.gen_restaurant_name(i),
                i,
                ArrayR(0)
            ) for i in range(n_rests)
        ]
        
        ff = FoodFlight()
        for rest in test_restaurants:
            ff.add_restaurant(rest)

        

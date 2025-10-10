from unittest import TestCase
import ast
import inspect
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR
from tests.helper import CollectionsFinder

from better_bst import BetterBinarySearchTree

class TestTask1Setup(TestCase):
    pass

class TestTask1(TestTask1Setup):
    def test_bst_range_query_type(self):
        """
        #name(Test BetterBST range query type)
        #hurdle
        """
        better_bst = BetterBinarySearchTree()
        
        # Add 10 keys
        test_keys = list(range(1, 10))
        for k in test_keys:
            better_bst[k] = k
            
        query_result = better_bst.range_query(min(test_keys), max(test_keys))
        
        self.assertTrue(
            isinstance(query_result, ArrayList) or isinstance(query_result, ArrayR),
            f"The object returned from range_query should be an ArrayList or an ArrayR (got '{type(query_result)}')"
        )

    def test_bst_balance_score_numeric(self):
        """
        #name(Test BetterBST balance score is numeric)
        #hurdle
        """
        tree = BetterBinarySearchTree()
        for k in [2, 1, 3]:
            tree[k] = k
            
        score_result = tree.balance_score()
        
        self.assertTrue(isinstance(score_result, int) or isinstance(score_result, float), f"Balance score should be a numeric value, but got {score_result} ({type(score_result)})")
    
    
    def test_bst_rebalance_basics(self):
        """
        #name(Test BetterBST root changed after rebalance)
        #hurdle
        """
        stick_tree = BetterBinarySearchTree()
        for k in range(10):
            stick_tree[k] = k
            
        og_order = list(stick_tree.pre_iter())
        
        stick_tree.rebalance()
        
        new_order = list(stick_tree.pre_iter())
        
        self.assertNotEqual(og_order, new_order, "Rebalancing a maximally unbalanced tree should change the iteration order")


class TestTask1Approach(TestTask1Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        #approach
        """
        import better_bst
        modules = [better_bst]

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
                

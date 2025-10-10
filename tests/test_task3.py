from unittest import TestCase
import ast
import inspect
from data_structures.abstract_list import List
from data_structures.referential_array import ArrayR
from data_structures.array_max_heap import ArrayMaxHeap
from tests.helper import CollectionsFinder

from orders import Order, OrderDispatch

class TestTask3Setup(TestCase):
    pass

class TestTask3(TestTask3Setup):
    def test_order_dispatch_distance_basics(self):
        """
        #name(Test order and dispatch distance basics)
        #hurdle
        """
        order = Order(5, (3, 4))

        dispatch = OrderDispatch((0, 0), 1)
        
        dispatch.receive_order(order)
        
        self.assertTrue(hasattr(order, 'distance') and order.distance is not None, "Order.distance attribute should be set once order is received by the Dispatch")
        self.assertEqual(order.distance, 5)
        
        
    def test_order_dispatch_multiple_type(self):
        """
        #name(Test dispatching multiple - types)
        #hurdle
        """
        dispatch = OrderDispatch((0, 0), 10)
        
        self.assertIsInstance(dispatch.deliver_multiple(max_travel=1000), List, "Deliver multiple should return an object derived from (abstract) List - even when empty")
        
        order1 = Order(5, (3, 4))
        order2 = Order(5, (6, 8))
        self.assertIsInstance(dispatch.deliver_multiple(max_travel=1000), List, "Deliver multiple should return an object derived from (abstract) List")

    def test_1054_only_order_surge_length(self):
        """
        #name(Test [FIT1054 ONLY] order surge - correct length)
        """
        n_expected = 50
        dispatch = OrderDispatch((0, 0), n_expected)
        dispatch.order_surge_1054(ArrayR.from_list([Order((5), (0, 0)) for _ in range(n_expected)]))
        
        try:
            n_actual = len(dispatch)
            
        except TypeError:
            self.fail("Dispatch __len__ didn't return an integer")
            
        self.assertIsInstance(n_actual, int, "Dispatch __len__ didn't return an integer")
        
        self.assertEqual(len(dispatch), n_expected, f"[IGNORE IF NOT FIT1054] - after a surge with n orders, dispatch should have length of n (expected {n_expected}, got {len(dispatch)})")

            

class TestTask3Approach(TestTask3Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        #approach
        """
        import orders
        modules = [orders]

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
        

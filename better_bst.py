# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Union
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR
from data_structures.binary_search_tree import BinarySearchTree, K, V

class BetterBinarySearchTree(BinarySearchTree[K, V]):
    def range_query(self, low: K, high: K) -> Union[ArrayR[V], ArrayList[V]]:
        """
            Return all items from the BST with keys,
            in the (inclusive) range of [low, high].
            Return the result in either an ArrayR or an ArrayList.
            Complexity Analysis:
            Let N be the number of nodes, h the tree height, and k the number of returned items.
            Best: O(h) by pruning off-range subtrees via the BST property (e.g., all keys < low or > high).
            Worst: O(N) when the range covers all keys so every node is visited (and k = N).     
        """
        out: ArrayList[V] = ArrayList()
        self._range_query_aux(self._BinarySearchTree__root, low, high, out)
        return out

    def _range_query_aux(self, node, low: K, high: K, out: ArrayList[V]) -> None:
        if node is None:
            return
        if node.key > high:
            self._range_query_aux(node.left, low, high, out)
        elif node.key < low:
            self._range_query_aux(node.right, low, high, out)
        else:
            self._range_query_aux(node.left, low, high, out)
            out.append(node.item)
            self._range_query_aux(node.right, low, high, out)
        
    def balance_score(self):
        """
            Returns the balance score of the BST, which we define as the
            difference between the ideal (balanced) height of the tree (achievable with a complete tree),
            and the actual height of the tree.
            Complexity Analysis:
            ...
        """
        pass
    def balance_score(self) -> int:
        """
        Returns the balance score of the BST, which we define as the
        difference between the ideal (balanced) height of the tree (achievable with a complete tree),
        and the actual height of the tree.
           
        Return balance score = actual_height - ideal_height, where height(empty) = -1.

        Ideal height: the height of a complete binary tree with the same number of nodes,
        given by ideal = ceil(log2(n + 1)) - 1 for n >= 1, and -1 when n = 0.

        Complexity analysis:
        Count and height are each computed once by recursion: time O(N), extra space O(h).
        """
        n = self._count_nodes(self._BinarySearchTree__root)
        actual = self._height(self._BinarySearchTree__root)
        ideal = -1 if n == 0 else math.ceil(math.log2(n + 1)) - 1
        return actual - ideal

    def _count_nodes(self, node) -> int:
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _height(self, node) -> int:
        if node is None:
            return -1
        lh = self._height(node.left)
        rh = self._height(node.right)
        return 1 + (lh if lh >= rh else rh)
    
    def rebalance(self):
        """
            Restructure the BST such that it is balanced.
            
            Do *not* return a new instance; rather, this method
            should modify the tree it is called on.
            Complexity Analysis:
            ...
        """
        pass
        
if __name__ == "__main__":
    # Test your code here.
    
    # Create a Better BST
    bbst = BetterBinarySearchTree()
    
    # Add all integers as key-value pairs to the tree
    for i in range(10):
        bbst[i] = i
        
    # Try a range query
    # Should give us the values between 4 and 7
    print("Range query:", bbst.range_query(4, 7))
    
    # Check the balance score before balancing
    print("Before balancing:", bbst.balance_score())
    
    # Try a rebalance
    bbst.rebalance()
    
    # How about after?
    print("After balancing:", bbst.balance_score())

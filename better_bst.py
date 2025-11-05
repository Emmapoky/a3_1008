# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/

# Context: Feel free to check these for my thought process and implementation notes.
# Notes:  https://drive.google.com/file/d/1Tl1zwuZxAvG8mrH47QbRnYfGvCR3fv2B/view?usp=sharing

from functools import total_ordering
import math

from typing import Tuple
from data_structures.array_list import ArrayList
from data_structures.binary_search_tree import BinarySearchTree, K, V

class BetterBinarySearchTree(BinarySearchTree[K, V]):
    def range_query(self, low: K, high: K) -> ArrayList[V]:
        """
        Return all values whose keys lie in the inclusive range [low, high], in ascending key order.

        :complexity: Best is O(h + k), Worst is O(N).

        The best case happens when key comparisons let the search prune most subtrees, so the traversal follows 
        one path of length h and visits only the k in‑range nodes to collect their values.​
        The worst case happens when the requested range covers most keys or the tree is very unbalanced, so the 
        traversal touches almost all N nodes.​

        This all works beacuse, in‑order traversal visits keys in ascending order, as such, the returned values are 
        already in ascending key order without extra work.​
        The BST property allows pruning during the traversal: if node.key < low, the left subtree is skipped, 
        and if node.key > high, the right subtree is skipped.
        """
        out = ArrayList()
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
        
    def balance_score(self) -> int:
        """
        Return balance score equates to actual_height minus ideal_height, with height(empty) being -1.

        :complexity: Best and Worst are both is O(N), where N is the number of nodes & h is the tree height.
        Both cases run in linear time because we traverse the tree once to count nodes and once to compute 
        height, visiting each node a constant number of times.​
        
        Moreover, the ideal height is computed from the node count using [ log (base 2) (n+1) - 1 ] 
        (or −1 when n=0).
        """
        n = self._count_nodes(self._BinarySearchTree__root)
        actual = self._height(self._BinarySearchTree__root)
        ideal = -1 if n == 0 else math.ceil(math.log2(n + 1)) - 1
        return actual - ideal

    def _count_nodes(self, node) -> int:
        """
        Count the number of nodes in the subtree rooted at node.

        :complexity: Best and Worst are both is O(N), where N is the number of nodes in the subtree.
        Here, the recursion visits each node exactly one time and combines the counts from the left 
        and right subtrees using a constant amount of work per node.
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _height(self, node) -> int:
        """
        Compute the height of the subtree rooted at node, with height(empty) = −1.

        :complexity: The best case and also worst case is O(N), where N is the number of nodes in the subtree.
        Here, the recursion touches each node once to take 1+max(left height,right height), 
        so the work is linear in the size of the subtree.
        """
        if node is None:
            return -1
        lh = self._height(node.left)
        rh = self._height(node.right)
        return 1 + (lh if lh >= rh else rh)
    
    def rebalance(self) -> None:
        """
        Rebuild the current tree into a balanced shape in place by collecting items and 
        reinserting in midpoint order.

        :complexity: Collect is O(N); Rebuild is O(N log N), where N is the number of nodes.​
        The collect step performs one in‑order traversal to gather all (key, value) pairs into 
        a list, touching each node once.​
        The rebuild step inserts midpoints via the tree’s insertion method; each insert costs 
        O(log N) as the shape becomes balanced, so across N inserts the total is O(N log N).
        """
        sorted_pairs = ArrayList()
        self._collect_inorder(self._BinarySearchTree__root, sorted_pairs)
        self._BinarySearchTree__root = None
        self._rebuild_from_sorted(sorted_pairs, 0, len(sorted_pairs) - 1)

    def _collect_inorder(self, node, out: ArrayList[Tuple[K, V]]) -> None:
        """
        Collect all (key, value) pairs from the subtree in ascending key order using in‑order traversal.

        :complexity: The best case and also worst case is O(N), where N is the number of nodes in the subtree.​
        In‑order traversal visits each node exactly once and appends its (key, value) to the output, 
        so the total work is linear.
        """
        if node is None:
            return
        self._collect_inorder(node.left, out)
        out.append((node.key, node.item))
        self._collect_inorder(node.right, out)

    def _rebuild_from_sorted(self, arr: ArrayList[Tuple[K, V]], lo: int, hi: int) -> None:
        """
        Insert items back into the tree from a sorted array by choosing midpoints first to form a balanced shape.

        :complexity: Over the entire rebuild it is O(N log N), where N is the number of items.
        Each recursion picks a midpoint in constant time and performs a single BST insertion; as the tree becomes 
        balanced, each insertion costs O(log N), so the N insertions add up to O(N log N).
        """
        if lo > hi:
            return
        mid = (lo + hi) // 2
        k, v = arr[mid]
        # herere I use BST’s recursive insertion
        self[k] = v
        self._rebuild_from_sorted(arr, lo, mid - 1)
        self._rebuild_from_sorted(arr, mid + 1, hi)
        
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

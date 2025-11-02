# You're welcome to use this decorator
# See: https://www.geeksforgeeks.org/python/python-functools-total_ordering/
from functools import total_ordering
import math

from typing import Union, Tuple
from data_structures.array_list import ArrayList
from data_structures.referential_array import ArrayR
from data_structures.binary_search_tree import BinarySearchTree, K, V

class BetterBinarySearchTree(BinarySearchTree[K, V]):
    def range_query(self, low: K, high: K) -> Union[ArrayR[V], ArrayList[V]]:
        """
        Return all values whose keys lie in the inclusive range [low, high], in ascending key order.

        :complexity: Best = O(h + k), Worst = O(N).
        Best happens when pruning skips most subtrees and we only walk down one path (height h)
        and collect k in-range items; Worst is when the range covers most keys (or the tree is
        very unbalanced), so we touch all N nodes once.

        Why this works:
        - In-order traversal of a BST visits keys in ascending order, so values come out sorted
          without any extra sorting.
        - The BST property lets us prune: if node.key < low, skip its left; if node.key > high,
          skip its right.
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
        
    def balance_score(self) -> int:
        """
        Return balance score = actual_height - ideal_height, with height(empty) = -1.

        :complexity: Best = Worst = O(N) time and O(h) recursion space.
        We compute the node count and the height once each by recursion; both visit every node once.

        Notes:
        - ideal_height for n nodes uses the complete-tree baseline: ceil(log2(n + 1)) - 1
          (and −1 when n = 0).
        """
        n = self._count_nodes(self._BinarySearchTree__root)
        actual = self._height(self._BinarySearchTree__root)
        ideal = -1 if n == 0 else math.ceil(math.log2(n + 1)) - 1
        return actual - ideal

    def _count_nodes(self, node) -> int:
        """
        :complexity: Best = Worst = O(N).
        Standard post-order count: 1 + left + right, touching each node exactly once.
        """
        if node is None:
            return 0
        return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    def _height(self, node) -> int:
        """
        :complexity: Best = Worst = O(N).
        Height(empty) = -1 so a leaf has height 0; result is 1 + max(left_height, right_height).
        """
        if node is None:
            return -1
        lh = self._height(node.left)
        rh = self._height(node.right)
        return 1 + (lh if lh >= rh else rh)
    
    def rebalance(self) -> None:
        """
        Rebuild the current tree into a balanced shape in place.

        :complexity: Collect = O(N); Rebuild = O(N log N).
        We first collect the in-order (key, value) sequence in O(N), then insert midpoints first
        using the tree’s own insertion, which is O(log N) per insert overall once the shape becomes
        balanced.

        Method:
        1) In-order collect to get (key, value) pairs in ascending key order.
        2) Clear the root and insert midpoints first (divide-and-conquer) for a near-complete shape.
        """
        sorted_pairs: ArrayList[Tuple[K, V]] = ArrayList()
        self._collect_inorder(self._BinarySearchTree__root, sorted_pairs)
        self._BinarySearchTree__root = None
        self._rebuild_from_sorted(sorted_pairs, 0, len(sorted_pairs) - 1)

    def _collect_inorder(self, node, out: ArrayList[Tuple[K, V]]) -> None:
        """
        :complexity: Best = Worst = O(N).
        In-order traversal (left -> visit -> right) yields ascending keys in a BST.
        """
        if node is None:
            return
        self._collect_inorder(node.left, out)
        out.append((node.key, node.item))
        self._collect_inorder(node.right, out)

    def _rebuild_from_sorted(self, arr: ArrayList[Tuple[K, V]], lo: int, hi: int) -> None:
        """
        :complexity: Over the entire rebuild: O(N log N).
        Each recursion chooses a midpoint (O(1)) and inserts via the tree API; across all N inserts,
        the cost amortizes to O(N log N) as the tree becomes balanced.

        Strategy:
        - Pick mid = (lo+hi)//2, insert (key, value), then recurse on left and right halves.
        """
        if lo > hi:
            return
        mid = (lo + hi) // 2
        k, v = arr[mid]
        # Use the BST’s recursive insertion; do not construct nodes directly to KEEP within the scaffold
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

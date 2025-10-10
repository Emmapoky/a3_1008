from __future__ import annotations
import sys

"""
Helper class to help extract data from your ADTS
for testing purposes.

You cannot use methods in this file or you will recieve
a 0 for approach and test case marks.

"""
from typing import Iterable, TypeVar, Union

import ast

T = TypeVar('T')

class CollectionsFinder(ast.NodeVisitor):
    def __init__(self, filename, forbidden_types=None):
        self.filename = filename

        # These will keep track of which class and function we are in
        # so we can ignore certain functions if needed
        self.current_class = None
        self.current_function = None
        self.in_testing = False

        # Holds 4-tuples of (class, function, used type, error message)
        self.failures = []
        self.forbidden_types = forbidden_types or {"list", "set", "dict", "reversed", "sorted"}
        
    def add_failure(self, used_type, message):
        """
        Add a failure to the list of failures.
        """
        if self.in_testing:
            return
        self.failures.append(
            (
                self.current_class,
                self.current_function,
                used_type,
                message,
            )
        )

    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        
        # Visit children
        self.generic_visit(node)
        
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        old_function = self.current_function
        self.current_function = node.name
        
        # Visit children
        self.generic_visit(node)
        
        self.current_function = old_function
        
    def visit_Assign(self, node: ast.Assign):
        if self.current_function in ("__str__", "__repr__"):
            return
        elif isinstance(node.value, (ast.List, ast.Set, ast.Dict)):
            self.add_failure(
                {
                    ast.List: list,
                    ast.Set: set,
                    ast.Dict: dict,
                }[type(node.value)],
                f"{self.filename} should not use built-in collections, but found usage at line {node.lineno}."
            )

        self.generic_visit(node)
        
    def visit_Call(self, node):
        if self.current_function in ("__str__", "__repr__"):
            return

        # Ignore print function calls
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            return
            
        if isinstance(node.func, ast.Name) and node.func.id in self.forbidden_types:
            self.add_failure(
                {
                    "list": list,
                    "set": set,
                    "dict": dict,
                    "reversed": reversed,
                    "sorted": sorted,
                }[node.func.id],
                f"{self.filename} should not use Python built-ins, but found '{node.func.id}()' at line {node.lineno}.",
            )

        self.generic_visit(node)
    
    def visit_ListComp(self, node: ast.ListComp):
        if "list" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            list,
            f"{self.filename} should not use built-in collections, but found a list comprehension at line {node.lineno}."
        )
        self.generic_visit(node)

    def visit_SetComp(self, node: ast.SetComp):
        if "set" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            set,
            f"{self.filename} should not use built-in collections, but found a set comprehension at line {node.lineno}."
        )
        self.generic_visit(node)
    
    def visit_DictComp(self, node: ast.DictComp):
        if "dict" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            dict,
            f"{self.filename} should not use built-in collections, but found a dict comprehension at line {node.lineno}."
        )
        self.generic_visit(node)
    
    def visit_List(self, node: ast.List):
        if "list" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            list,
            f"{self.filename} should not use built-in collections, but found a list at line {node.lineno}."
        )
        self.generic_visit(node)
    
    def visit_Set(self, node: ast.Set):
        if "set" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            set,
            f"{self.filename} should not use built-in collections, but found a set at line {node.lineno}."
        )
        self.generic_visit(node)
    
    def visit_Dict(self, node: ast.Dict):
        if "dict" not in self.forbidden_types or self.current_function in ("__str__", "__repr__"):
            return
        self.add_failure(
            dict,
            f"{self.filename} should not use built-in collections, but found a dict at line {node.lineno}."
        )
        self.generic_visit(node)
    
    def visit_If(self, node):
        try:
            if node.test.comparators[0].value == "__main__":
                self.in_testing = True
                self.generic_visit(node)
                self.in_testing = False
            else:
                self.generic_visit(node)
        except (AttributeError, IndexError):
            self.generic_visit(node)


import ast, inspect



#!/usr/bin/env python3
"""Utility functions for working with nested maps."""

def access_nested_map(nested_map, path):
    """Access a value in a nested dictionary using a tuple path.

    Args:
        nested_map (dict): The dictionary to navigate.
        path (tuple): Keys specifying the path to the desired value.

    Returns:
        The value at the end of the path.
    """
    for key in path:
        nested_map = nested_map[key]
    return nested_map

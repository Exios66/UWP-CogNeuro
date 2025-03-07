"""
Visualization tools for neuroscience data.

This module provides functions and classes for visualizing neuroscience data,
including brain maps, connectivity matrices, and statistical results.
"""

from .brain_maps import plot_brain_map, plot_roi

__all__ = ["plot_brain_map", "plot_roi"]

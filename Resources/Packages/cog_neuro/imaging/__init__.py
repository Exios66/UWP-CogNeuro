"""
Neuroimaging data processing and analysis tools.

This module provides functions and classes for processing and analyzing
neuroimaging data, including fMRI, EEG, and other modalities.
"""

from .preprocess import load_dataset, standard_pipeline

__all__ = ["load_dataset", "standard_pipeline"]

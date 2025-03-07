"""
Unit tests for the preprocessing module.
"""

import os
import numpy as np
import pytest
from cog_neuro.imaging import preprocess


def test_load_dataset():
    """Test that load_dataset raises FileNotFoundError for non-existent files."""
    with pytest.raises(FileNotFoundError):
        preprocess.load_dataset("non_existent_file.nii.gz")


def test_standard_pipeline():
    """Test that standard_pipeline applies the correct preprocessing steps."""
    # Create a random dataset
    data = np.random.randn(64, 64, 30, 100)
    
    # Apply standard pipeline with all steps
    preprocessed_data = preprocess.standard_pipeline(
        data,
        motion_correction=True,
        spatial_smoothing=True,
        temporal_filtering=True
    )
    
    # Check that the output has the same shape as the input
    assert preprocessed_data.shape == data.shape
    
    # Apply standard pipeline with no steps
    preprocessed_data = preprocess.standard_pipeline(
        data,
        motion_correction=False,
        spatial_smoothing=False,
        temporal_filtering=False
    )
    
    # Check that the output is the same as the input (no preprocessing applied)
    np.testing.assert_array_equal(preprocessed_data, data)


def test_motion_correction():
    """Test that _apply_motion_correction returns data with the same shape."""
    data = np.random.randn(64, 64, 30, 100)
    corrected_data = preprocess._apply_motion_correction(data, method="rigid")
    assert corrected_data.shape == data.shape


def test_spatial_smoothing():
    """Test that _apply_spatial_smoothing returns data with the same shape."""
    data = np.random.randn(64, 64, 30, 100)
    smoothed_data = preprocess._apply_spatial_smoothing(data, fwhm=6.0)
    assert smoothed_data.shape == data.shape


def test_temporal_filtering():
    """Test that _apply_temporal_filtering returns data with the same shape."""
    data = np.random.randn(64, 64, 30, 100)
    filtered_data = preprocess._apply_temporal_filtering(
        data, high_pass=0.01, low_pass=0.1
    )
    assert filtered_data.shape == data.shape 
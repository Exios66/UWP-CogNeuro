# Imaging Module API Reference

The `cog_neuro.imaging` module provides functions and classes for processing and analyzing neuroimaging data.

## Preprocessing

### `load_dataset(filepath)`

Load a neuroimaging dataset from a file.

**Parameters:**

- `filepath` (str): Path to the neuroimaging data file.

**Returns:**

- `np.ndarray`: The loaded neuroimaging data.

**Raises:**

- `FileNotFoundError`: If the file does not exist.
- `ValueError`: If the file format is not supported.

**Example:**

```python
from cog_neuro.imaging import load_dataset

# Load a dataset
data = load_dataset('data/sub-01_task-rest_bold.nii.gz')
```

### `standard_pipeline(data, motion_correction=True, spatial_smoothing=True, temporal_filtering=True, **kwargs)`

Apply a standard preprocessing pipeline to neuroimaging data.

**Parameters:**

- `data` (np.ndarray): The input neuroimaging data.
- `motion_correction` (bool, optional): Whether to apply motion correction. Default is True.
- `spatial_smoothing` (bool, optional): Whether to apply spatial smoothing. Default is True.
- `temporal_filtering` (bool, optional): Whether to apply temporal filtering. Default is True.
- `**kwargs`: Additional parameters for specific preprocessing steps.

**Additional Parameters:**

- `method` (str, optional): The motion correction method to use. Default is "rigid".
- `fwhm` (float, optional): The full width at half maximum of the Gaussian kernel for spatial smoothing. Default is 6.0.
- `high_pass` (float, optional): The high-pass filter cutoff frequency in Hz for temporal filtering. Default is 0.01.
- `low_pass` (float, optional): The low-pass filter cutoff frequency in Hz for temporal filtering. Default is None.

**Returns:**

- `np.ndarray`: The preprocessed neuroimaging data.

**Example:**

```python
from cog_neuro.imaging import load_dataset, standard_pipeline

# Load a dataset
data = load_dataset('data/sub-01_task-rest_bold.nii.gz')

# Apply standard preprocessing
preprocessed_data = standard_pipeline(
    data,
    motion_correction=True,
    spatial_smoothing=True,
    temporal_filtering=True,
    fwhm=6.0,
    high_pass=0.01,
    low_pass=0.1
)
```

## Internal Functions

These functions are used internally by the `standard_pipeline` function and are not typically called directly.

### `_apply_motion_correction(data, method="rigid", **kwargs)`

Apply motion correction to neuroimaging data.

### `_apply_spatial_smoothing(data, fwhm=6.0, **kwargs)`

Apply spatial smoothing to neuroimaging data.

### `_apply_temporal_filtering(data, high_pass=0.01, low_pass=None, **kwargs)`

Apply temporal filtering to neuroimaging data.

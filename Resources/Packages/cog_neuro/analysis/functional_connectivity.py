"""
Functional connectivity analysis for neuroimaging data.

This module provides functions for computing and visualizing functional
connectivity in the brain, including correlation matrices and network analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Optional, Union, Dict, Any, List, Tuple


def compute_correlation_matrix(
    data: np.ndarray, 
    atlas: str = "harvard_oxford", 
    method: str = "pearson",
    **kwargs: Any
) -> np.ndarray:
    """
    Compute a functional connectivity matrix from neuroimaging data.

    Parameters
    ----------
    data : np.ndarray
        The input neuroimaging data, with shape (x, y, z, time) or (roi, time).
    atlas : str, optional
        The brain atlas to use for defining regions of interest, by default "harvard_oxford".
    method : str, optional
        The correlation method to use, by default "pearson".
    **kwargs : Any
        Additional parameters for the correlation method.

    Returns
    -------
    np.ndarray
        The functional connectivity matrix, with shape (roi, roi).
    """
    # This is a placeholder. In a real implementation, we would use
    # libraries like nilearn to compute functional connectivity.
    print(f"Computing functional connectivity with atlas: {atlas}, method: {method}")
    
    # If data is already in ROI format
    if len(data.shape) == 2:
        roi_data = data
    else:
        # Placeholder: extract ROI time series using the specified atlas
        # In a real implementation, we would use nilearn.input_data.NiftiLabelsMasker
        print(f"Extracting ROI time series using atlas: {atlas}")
        n_rois = 100  # Placeholder
        n_timepoints = data.shape[-1]
        roi_data = np.random.randn(n_rois, n_timepoints)
    
    # Compute correlation matrix
    fc_matrix = np.corrcoef(roi_data)
    
    return fc_matrix


def plot_matrix(
    matrix: np.ndarray,
    roi_labels: Optional[List[str]] = None,
    cmap: str = "coolwarm",
    vmin: float = -1.0,
    vmax: float = 1.0,
    title: str = "Functional Connectivity Matrix",
    figsize: Tuple[int, int] = (10, 8),
    **kwargs: Any
) -> plt.Figure:
    """
    Plot a functional connectivity matrix.

    Parameters
    ----------
    matrix : np.ndarray
        The functional connectivity matrix to plot.
    roi_labels : Optional[List[str]], optional
        Labels for the regions of interest, by default None.
    cmap : str, optional
        The colormap to use, by default "coolwarm".
    vmin : float, optional
        The minimum value for the colormap, by default -1.0.
    vmax : float, optional
        The maximum value for the colormap, by default 1.0.
    title : str, optional
        The title of the plot, by default "Functional Connectivity Matrix".
    figsize : Tuple[int, int], optional
        The size of the figure, by default (10, 8).
    **kwargs : Any
        Additional parameters for matplotlib.pyplot.imshow.

    Returns
    -------
    plt.Figure
        The matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    im = ax.imshow(matrix, cmap=cmap, vmin=vmin, vmax=vmax, **kwargs)
    
    # Add colorbar
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Correlation")
    
    # Add labels if provided
    if roi_labels is not None:
        n_rois = len(roi_labels)
        ax.set_xticks(np.arange(n_rois))
        ax.set_yticks(np.arange(n_rois))
        ax.set_xticklabels(roi_labels, rotation=90)
        ax.set_yticklabels(roi_labels)
    
    ax.set_title(title)
    
    # Add grid lines
    ax.set_xticks(np.arange(-0.5, matrix.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0], 1), minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=0.5)
    
    fig.tight_layout()
    
    return fig 
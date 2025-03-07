# Neuroimaging Visualization Tools

This directory contains resources for visualization tools used in cognitive neuroscience, with a focus on brain imaging data visualization, interactive exploration, and data presentation techniques.

## Brain Visualization Software

### Comparison of Popular Brain Visualization Tools

| Tool | Primary Use Cases | Data Formats | Platform | Interface | Key Features | Learning Curve |
|------|------------------|--------------|----------|-----------|--------------|----------------|
| FSLeyes | FSL data visualization | NIfTI, GIFTI, CIFTI | Cross-platform | GUI | Multi-modal display, ROI analysis | Moderate |
| MRIcroGL | Quick visualization, rendering | NIfTI | Cross-platform | GUI | 3D rendering, multiple overlays | Gentle |
| FreeSurfer Freeview | Surface & volume visualization | MGZ, NIfTI, surface files | Cross-platform | GUI | Surface/volume integration | Moderate |
| BrainNet Viewer | Network visualization | Surface meshes, matrices | MATLAB | GUI | Connectome visualization | Gentle |
| Nilearn | Programmatic visualization | NIfTI, GIFTI | Python | Script-based | Integration with sklearn, customizable | Moderate |
| Brainstorm | MEG/EEG/fMRI visualization | MEG/EEG/fMRI | MATLAB | GUI | Source reconstruction, time series | Steep |
| 3D Slicer | Multi-purpose medical imaging | DICOM, NIfTI | Cross-platform | GUI | Segmentation, registration, extensible | Steep |
| MNE-Python | MEG/EEG visualization | MEG/EEG/fMRI | Python | Script-based | Complete analysis pipeline | Moderate |
| AFNI | Full fMRI pipeline & viewing | BRIK/HEAD, NIfTI | Cross-platform | GUI/Script | Real-time display, many plugins | Steep |
| BrainVoyager | Commercial neuroimage analysis | Native format, NIfTI | Cross-platform | GUI | High-quality rendering, MVPA | Steep |

## Installation and Basic Usage

### FSLeyes

FSLeyes is the FSL image viewer, used for viewing 3D and 4D neuroimaging data.

#### Installation

```bash
# Via conda
conda install -c conda-forge fsleyes

# Via pip
pip install fsleyes

# It's also included with FSL installation
```

#### Basic Usage Example

```python
# Python scripting with FSLeyes
import fsleyes

# Start fsleyes with specific files
fsleyes.main(['path/to/structural.nii.gz', 'path/to/functional.nii.gz'])

# Programmatic control
overlayList = fsleyes.getCurrentOverlayList()
displayCtx = fsleyes.getCurrentDisplayContext()

# Add an overlay
overlay = fsleyes.loadOverlay('path/to/image.nii.gz')
overlayList.append(overlay)

# Set display properties
display = displayCtx.getDisplay(overlay)
display.brightness = 50
display.contrast = 40
```

### Nilearn

A Python package that provides statistical and machine learning tools for neuroimaging data analysis and visualization.

#### Installation

```bash
# Via pip
pip install nilearn

# Via conda
conda install -c conda-forge nilearn
```

#### Basic Visualization Examples

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, image

# Fetch example dataset
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]

# Basic plot - Single cuts
plotting.plot_stat_map(
    stat_img, 
    display_mode='ortho',
    cut_coords=(0, 0, 0),
    title='Motor activation'
)

# Surface plot
fsaverage = datasets.fetch_surf_fsaverage()
texture = surface.vol_to_surf(stat_img, fsaverage.pial_right)
plotting.plot_surf_stat_map(
    fsaverage.infl_right, 
    texture, 
    hemi='right',
    title='Surface right hemisphere',
    threshold=1., 
    bg_map=fsaverage.sulc_right
)

# Multiple slices
plotting.plot_stat_map(
    stat_img,
    display_mode='z',
    cut_coords=5,
    title='Motor activation (axial slices)'
)

# Glass brain view
plotting.plot_glass_brain(
    stat_img,
    threshold=3,
    title='Glass brain view',
    display_mode='lzry',
    colorbar=True
)

# Region highlighting
plotting.plot_roi(
    datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm'),
    title='Harvard-Oxford Atlas'
)

# Interactive view (in Jupyter notebooks)
view = plotting.view_img(
    stat_img, 
    threshold=3.0,
    title='Interactive Viewer'
)
view.open_in_browser()

# Connectome visualization
matrix = np.random.rand(10, 10)
coords = np.random.rand(10, 3) * 100
plotting.plot_connectome(
    matrix, coords,
    edge_threshold='80%',
    title='Connectome'
)

plt.show()
```

## Brain Atlases and Parcellations

### Common Atlases for Visualization

| Atlas | Resolution | Regions | Anatomical/Functional | Format | Access Tools |
|-------|------------|---------|---------------|--------|-------------|
| AAL | 1mm, 2mm | 116 | Anatomical | NIfTI | FSL, SPM, Nilearn |
| Harvard-Oxford | 1mm, 2mm | 48/96 | Anatomical | NIfTI | FSL, Nilearn |
| Brainnetome | 1mm, 2mm | 246 | Anatomical/Functional | NIfTI | [Website](http://atlas.brainnetome.org) |
| Yeo-7/17 | Surface | 7/17 networks | Functional | GIFTI, CIFTI | FreeSurfer, Nilearn |
| Schaefer | Surface | 100-1000 | Functional | GIFTI, CIFTI, NIfTI | Nilearn |
| Destrieux | Surface | 148 | Anatomical | Surface | FreeSurfer |
| Power 264 | Coordinates | 264 ROIs | Functional | Coordinates | Custom |
| Glasser (HCP) | Surface | 360 | Multimodal | GIFTI, CIFTI | Connectome Workbench |
| JuBrain (Jülich) | 1mm, 2mm | Various | Cytoarchitectonic | NIfTI | SPM Anatomy Toolbox |
| Talairach | 1mm | Various | Anatomical | Specialized | Talairach Daemon |

### Accessing and Visualizing Atlases with Nilearn

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, image, regions

# Fetch different atlases
harvard_oxford = datasets.fetch_atlas_harvard_oxford('cort-maxprob-thr25-2mm')
aal = datasets.fetch_atlas_aal()
msdl = datasets.fetch_atlas_msdl()
basc = datasets.fetch_atlas_basc_multiscale_2015(version='sym', resolution=64)
yeo = datasets.fetch_atlas_yeo_2011()
difumo = datasets.fetch_atlas_difumo(dimension=64)

# Plot different atlases
plt.figure(figsize=(15, 10))

# Harvard-Oxford cortical atlas
plt.subplot(231)
plotting.plot_roi(
    harvard_oxford.maps, 
    title="Harvard-Oxford Atlas",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

# AAL atlas
plt.subplot(232)
plotting.plot_roi(
    aal.maps, 
    title="AAL Atlas",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

# MSDL atlas
plt.subplot(233)
plotting.plot_roi(
    msdl.maps, 
    title="MSDL Atlas",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

# BASC atlas
plt.subplot(234)
plotting.plot_roi(
    basc.scale064, 
    title="BASC Atlas (64 regions)",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

# Yeo atlas
plt.subplot(235)
plotting.plot_roi(
    yeo.thick_7, 
    title="Yeo 7-Network Atlas",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

# DiFuMo atlas
plt.subplot(236)
plotting.plot_roi(
    difumo.maps, 
    title="DiFuMo Atlas (64 dimensions)",
    cut_coords=(0, 0, 0),
    display_mode='ortho',
    colorbar=False,
    cmap='Paired'
)

plt.tight_layout()
plt.show()
```

## Advanced Visualization Techniques

### Time Series and Dynamic Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from nilearn import datasets, plotting

# Fetch example 4D dataset (fMRI)
fmri_data = datasets.fetch_development_fmri(n_subjects=1)
fmri_img = fmri_data.func[0]

# Extract data
from nilearn.image import load_img
fmri_array = load_img(fmri_img).get_fdata()
n_volumes = fmri_array.shape[3]

# Create a figure for animation
fig, ax = plt.subplots(figsize=(10, 6))

# Create initial empty display
display = plotting.plot_epi(
    fmri_img, 
    display_mode='z', 
    cut_coords=1, 
    title=f"Volume: 0/{n_volumes-1}",
    figure=fig,
    axes=ax
)

# Update function for animation
def update(frame):
    ax.clear()
    display = plotting.plot_epi(
        fmri_img, 
        display_mode='z', 
        cut_coords=1, 
        title=f"Volume: {frame}/{n_volumes-1}",
        figure=fig,
        axes=ax
    )
    return display.axes

# Create animation
ani = FuncAnimation(fig, update, frames=range(0, n_volumes, 5), blit=False)

# Save animation (optional)
# ani.save('fmri_animation.gif', writer='pillow', fps=5)

plt.tight_layout()
plt.show()
```

### 3D Surface Visualization

```python
import numpy as np
from nilearn import datasets, surface, plotting

# Load fsaverage surface
fsaverage = datasets.fetch_surf_fsaverage()

# Example: Visualize a random activation pattern
# Generate random data for the right hemisphere
n_vertices = len(surface.load_surf_data(fsaverage.sulc_right))
random_data = np.random.randn(n_vertices)
# Smooth it for a more realistic appearance
from scipy.ndimage import gaussian_filter1d
smooth_data = gaussian_filter1d(random_data, sigma=5)

# Create an interactive 3D visualization
view = plotting.view_surf(
    fsaverage.infl_right, 
    smooth_data, 
    threshold=0.5,
    cmap='cold_hot',
    symmetric_cmap=True,
    bg_map=fsaverage.sulc_right
)

# Open in browser (for Jupyter: view to display inline)
view.open_in_browser()
```

### Connectome Visualization

```python
import numpy as np
from nilearn import datasets, plotting

# Fetch coordinates in MNI space
power_dataset = datasets.fetch_coords_power_2011()
power_coords = np.vstack((
    power_dataset.rois['x'],
    power_dataset.rois['y'],
    power_dataset.rois['z']
)).T

# Number of nodes
n_nodes = power_coords.shape[0]

# Create a random connectivity matrix
np.random.seed(42)
connectivity = np.random.rand(n_nodes, n_nodes)
# Make it symmetric
connectivity = (connectivity + connectivity.T) / 2
# Set diagonal to zero (no self-connections)
np.fill_diagonal(connectivity, 0)

# Create basic connectome visualization
plotting.plot_connectome(
    connectivity, 
    power_coords,
    edge_threshold="95%",  # Keep only the 5% strongest connections
    node_color='k',
    node_size=10,
    title="Brain Connectome Visualization"
)

# More advanced, with node colors by network
node_networks = power_dataset.networks
network_names = np.unique(node_networks)
network_colors = plotting.cm.nipy_spectral(np.linspace(0, 1, len(network_names)))

# Map network names to colors
node_colors = np.zeros((n_nodes, 4))
for i, network in enumerate(network_names):
    node_colors[node_networks == network] = network_colors[i]

# Plot with colored nodes by network
plotting.plot_connectome(
    connectivity, 
    power_coords,
    edge_threshold="95%",
    node_color=node_colors,
    node_size=20,
    title="Connectome with Networks"
)

# Interactive 3D connectome visualization
view = plotting.view_connectome(
    connectivity, 
    power_coords,
    edge_threshold="95%"
)
view.open_in_browser()

plt.show()
```

## Specialized Visualization Types

### Statistical Maps

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting

# Fetch example statistical map
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]

# Basic stat map with proper thresholding
plotting.plot_stat_map(
    stat_img,
    threshold=3.0,  # Thresholding at z=3.0
    colorbar=True,
    title='Thresholded Statistical Map'
)

# With different colormaps
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

colormaps = ['cold_hot', 'red_yellow', 'blue_red', 'cyan_copper']
for i, cmap in enumerate(colormaps):
    ax = axes[i // 2, i % 2]
    plotting.plot_stat_map(
        stat_img,
        threshold=3.0,
        cmap=cmap,
        colorbar=True,
        title=f'Colormap: {cmap}',
        axes=ax
    )

plt.tight_layout()
plt.show()
```

### Multi-modal Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, image

# Fetch data
mni_template = datasets.load_mni152_template()
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]

# 1. Overlay statistical map on anatomical image
plotting.plot_stat_map(
    stat_img,
    bg_img=mni_template,
    threshold=3.0,
    title='Statistical Map on Anatomical'
)

# 2. Multi-modal visualization: anatomical + statistical + contours
# First create a mask from thresholded statistical map
from nilearn.image import threshold_img
thresh_stat_img = threshold_img(stat_img, threshold=3.0)

# Plot
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
display = plotting.plot_anat(
    mni_template,
    title='Multi-modal: Anatomy + Stats + Contours',
    figure=fig,
    axes=ax
)
display.add_overlay(stat_img, cmap='cold_hot', threshold=3.0)
display.add_contours(thresh_stat_img, colors='r', linewidths=0.5)

plt.show()
```

## Data Export and Publication-Ready Figures

### Creating Publication Quality Figures

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting, image
from matplotlib.gridspec import GridSpec

# Fetch example data
mni_template = datasets.load_mni152_template()
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]
fsaverage = datasets.fetch_surf_fsaverage()

# Create a publication-quality figure
plt.figure(figsize=(12, 10), dpi=300)  # High resolution
gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

# Plot 1: Axial slices
ax1 = plt.subplot(gs[0, 0])
display1 = plotting.plot_stat_map(
    stat_img,
    display_mode='z',
    cut_coords=5,
    threshold=3.0,
    colorbar=True,
    cmap='cold_hot',
    black_bg=False,
    title='A. Axial Slices',
    axes=ax1
)

# Plot 2: 3D Glass brain
ax2 = plt.subplot(gs[0, 1])
display2 = plotting.plot_glass_brain(
    stat_img,
    threshold=3.0,
    colorbar=True,
    title='B. Glass Brain View',
    axes=ax2
)

# Plot 3: Surface view left
ax3 = plt.subplot(gs[1, 0])
texture = surface.vol_to_surf(stat_img, fsaverage.pial_left)
display3 = plotting.plot_surf_stat_map(
    fsaverage.infl_left,
    texture,
    hemi='left',
    threshold=1.0,
    bg_map=fsaverage.sulc_left,
    colorbar=True,
    title='C. Left Surface',
    axes=ax3
)

# Plot 4: Surface view right
ax4 = plt.subplot(gs[1, 1])
texture = surface.vol_to_surf(stat_img, fsaverage.pial_right)
display4 = plotting.plot_surf_stat_map(
    fsaverage.infl_right,
    texture,
    hemi='right',
    threshold=1.0,
    bg_map=fsaverage.sulc_right,
    colorbar=True,
    title='D. Right Surface',
    axes=ax4
)

plt.tight_layout()
plt.savefig('publication_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('publication_figure.svg', format='svg', bbox_inches='tight')
plt.show()
```

### Video Creation Tools

```python
import numpy as np
import matplotlib.pyplot as plt
from nilearn import datasets, plotting
from matplotlib.animation import FuncAnimation
import os

# Fetch example data
fsaverage = datasets.fetch_surf_fsaverage()
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]

# Create a surface texture
texture = surface.vol_to_surf(stat_img, fsaverage.pial_right)

# Prepare a figure for animation
fig = plt.figure(figsize=(10, 8))

# Function to create a frame with a specific camera view
def create_frame(elevation, azimuth):
    fig.clear()
    
    # Plot surface with 3D data
    display = plotting.plot_surf_stat_map(
        fsaverage.infl_right,
        texture,
        hemi='right',
        threshold=1.0,
        bg_map=fsaverage.sulc_right,
        cmap='cold_hot',
        colorbar=True,
        title=f'View: Elevation={elevation}°, Azimuth={azimuth}°',
        figure=fig
    )
    
    # Set camera position
    display.axes3d.view_init(elev=elevation, azim=azimuth)
    
    return fig

# Define animation parameters
elevations = 20  # Fixed elevation
azimuths = np.linspace(0, 360, 36)  # Full rotation

# Function to update frame
def update(frame):
    return create_frame(elevations, azimuths[frame])

# Create animation
ani = FuncAnimation(fig, update, frames=len(azimuths), blit=False)

# Save animation
ani.save('brain_rotation.gif', writer='pillow', fps=8, dpi=150)

# For video formats (requires ffmpeg)
# ani.save('brain_rotation.mp4', writer='ffmpeg', fps=15, dpi=200, bitrate=1800)

plt.close()
print("Animation saved to brain_rotation.gif")
```

## Interactive Web-Based Visualization

### Using Nilearn's HTML Viewer

```python
from nilearn import datasets, plotting

# Fetch data
motor_images = datasets.fetch_neurovault_motor_task()
stat_img = motor_images.images[0]

# Create interactive HTML visualization
view = plotting.view_img(
    stat_img, 
    threshold=3.0,
    colorbar=True,
    title='Interactive Statistical Map'
)

# Save HTML file
view.save_as_html('interactive_brain.html')

# Open in browser
view.open_in_browser()
```

### Using Plotly for Web-Compatible Visualizations

```python
import numpy as np
import nibabel as nib
import plotly.graph_objects as go
from nilearn import datasets

# Fetch example data
mni = datasets.load_mni152_template()
img = nib.load(mni)
data = img.get_fdata()

# Extract a slice
slice_data = data[:, :, 40].T  # Get axial slice and transpose for correct orientation

# Create plotly figure
fig = go.Figure(data=go.Heatmap(
    z=slice_data,
    colorscale='Gray',
    showscale=False
))

fig.update_layout(
    title='Interactive MRI Slice',
    width=600,
    height=600,
    xaxis=dict(title='X axis'),
    yaxis=dict(title='Y axis')
)

# Add interactive tools
fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(
                    args=[{"colorscale": "Gray"}],
                    label="Grayscale",
                    method="restyle"
                ),
                dict(
                    args=[{"colorscale": "Hot"}],
                    label="Hot",
                    method="restyle"
                ),
                dict(
                    args=[{"colorscale": "Jet"}],
                    label="Jet",
                    method="restyle"
                )
            ],
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        )
    ]
)

# Show figure
fig.show()

# Save to HTML (for sharing)
fig.write_html("interactive_slice.html")
```

## Learning Resources and Tutorials

### Recommended Courses and Tutorials

1. **Nilearn Tutorials**
   - [Official Nilearn Examples](https://nilearn.github.io/stable/auto_examples/index.html)
   - [Nilearn Documentation](https://nilearn.github.io/stable/index.html)

2. **Online Courses**
   - [Neuromatch Academy](https://compneuro.neuromatch.io/) - Computational Neuroscience
   - [OHBM Educational Courses](https://www.humanbrainmapping.org/)

3. **Workshops**
   - [BrainHack](https://brainhack.org/) - Global collaboration workshops
   - [INCF Training](https://training.incf.org/) - Neuroinformatics training resources

4. **YouTube Channels**
   - [Andy's Brain Book](https://www.youtube.com/channel/UCPiCUNIskanIZvTOXG-jMlw)
   - [fMRIPrep YouTube](https://www.youtube.com/channel/UC_BIby85hZmcItMrkAlc8wg)

### Books and Papers

1. **Books**
   - "Principles of Brain Dynamics" by Mikhail I. Rabinovich et al.
   - "Brain Mapping: The Methods" by Arthur W. Toga and John C. Mazziotta
   - "Visualization in Medicine" by Bernhard Preim and Dirk Bartz

2. **Key Papers**
   - Margulies, D.S., et al. (2013). "Visualizing the human connectome"
   - Madan, C.R. (2015). "Creating 3D visualizations of MRI data"
   - Heuer, K. et al. (2016). "Open Neuroimaging Laboratory"

### Conferences and Communities

1. **Conferences**
   - Organization for Human Brain Mapping (OHBM)
   - Society for Neuroscience (SfN)
   - IEEE Visualization
   - BioVis

2. **Online Communities**
   - [NeuroStars](https://neurostars.org/) - Q&A forum for neuroscience
   - [Nilearn Discourse](https://nilearn.discourse.group/)
   - [BrainHack Mattermost](https://mattermost.brainhack.org/)

## Best Practices for Scientific Visualization

### Color Scheme Recommendations

| Purpose | Recommended Schemes | Accessibility Considerations |
|---------|---------------------|------------------------------|
| Anatomical | Gray, Bone | High contrast for structures |
| Statistical (pos/neg) | RdBu, cold_hot | Diverging, color-blind safe |
| Statistical (pos only) | YlOrRd, hot | Sequential, color-blind safe |
| Overlays | YlOrRd, Reds, plasma | Contrast with background |
| ROIs/Atlases | Set3, tab20, Paired | Distinguishable categorical colors |
| Surface meshes | gray, bone | Subtle to highlight data |
| DTI/Tractography | hsv, twilight | Angular data representation |

### Visualization Ethics Guidelines

1. **Truthful Representation**
   - Use appropriate thresholds (no "cherry-picking")
   - Show full data range when relevant
   - Maintain anatomical proportions

2. **Reproducibility**
   - Document visualization parameters
   - Include colorbar scales
   - Report software versions and methods

3. **Accessibility**
   - Use colorblind-friendly palettes
   - Provide multiple views (different planes)
   - Include appropriate labels and legends

4. **Data Privacy**
   - Ensure de-identification for shared visualizations
   - Consider facial features in surface renderings
   - Check metadata in shared files

### Effective Communication Tips

1. **For Scientific Papers**
   - Use consistent views across figures
   - Include appropriate anatomical reference
   - Label regions clearly with anatomical terms
   - Use composite figures to show multiple aspects

2. **For Presentations**
   - Simplify visualizations for slides
   - Use animations sparingly and purposefully
   - Consider 3D for engagement, 2D for precision
   - Highlight key findings visually

3. **For Public Communication**
   - Simplify terminology and visualization
   - Provide clear anatomical context
   - Use familiar metaphors and comparisons
   - Consider interactive formats when possible

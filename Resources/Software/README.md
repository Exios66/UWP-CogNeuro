# Cognitive Neuroscience Software Resources

This directory contains a curated collection of software resources for cognitive neuroscience research, organized by category. Each subdirectory contains detailed information about specific tools, frameworks, and best practices for different aspects of neuroscience research.

## Directory Structure

| Subdirectory | Description |
|--------------|-------------|
| [Neuroimaging](./Neuroimaging/) | Software for MRI, fMRI, PET, and other neuroimaging modalities |
| [DataAnalysis](./DataAnalysis/) | Statistical and machine learning tools for neuroscience data analysis |
| [Visualization](./Visualization/) | Tools for visualizing brain data, networks, and research findings |
| [ComputationalNeuroscience](./ComputationalNeuroscience/) | Neural simulators and computational modeling frameworks |
| [DataManagement](./DataManagement/) | Standards, tools, and best practices for neuroscience data management |

## Quick Reference Guide

### General Purpose Neuroscience Packages

| Package | Programming Language | Primary Focus | URL |
|---------|---------------------|---------------|-----|
| Nilearn | Python | Statistical learning for neuroimaging | [nilearn.github.io](https://nilearn.github.io/) |
| MNE-Python | Python | MEG/EEG analysis and visualization | [mne.tools](https://mne.tools/stable/index.html) |
| FreeSurfer | C, C++ | Structural MRI processing | [freesurfer.net](https://surfer.nmr.mgh.harvard.edu/) |
| FSL | C++, Python | Comprehensive MRI analysis | [fmrib.ox.ac.uk/fsl](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki) |
| SPM | MATLAB | Statistical Parametric Mapping | [fil.ion.ucl.ac.uk/spm](https://www.fil.ion.ucl.ac.uk/spm/) |
| AFNI | C, Python | Functional MRI analysis | [afni.nimh.nih.gov](https://afni.nimh.nih.gov/) |
| NeuroDebian | N/A | Neuroscience software platform | [neuro.debian.net](https://neuro.debian.net/) |
| NiBabel | Python | Neuroimaging file format access | [nipy.org/nibabel](https://nipy.org/nibabel/) |
| Psychtoolbox | MATLAB | Visual and auditory stimulus presentation | [psychtoolbox.org](http://psychtoolbox.org/) |
| PsychoPy | Python | Stimulus presentation and experimental control | [psychopy.org](https://www.psychopy.org/) |

### Computational Neuroscience Tools

| Tool | Level of Detail | Primary Use | URL |
|------|----------------|-------------|-----|
| NEURON | Detailed compartmental | Single neurons to networks | [neuron.yale.edu](https://neuron.yale.edu/neuron/) |
| Brian2 | Flexible | Spiking neural networks | [briansimulator.org](https://briansimulator.org/) |
| NEST | Point neuron | Large-scale networks | [nest-simulator.org](https://www.nest-simulator.org/) |
| The Virtual Brain | Whole-brain | Large-scale brain dynamics | [thevirtualbrain.org](https://www.thevirtualbrain.org/tvb/zwei) |
| NetPyNE | Network-level | Complex networks with NEURON | [netpyne.org](http://netpyne.org/) |
| NeuroML | Model description | Standardized model descriptions | [neuroml.org](https://neuroml.org/) |

### Neuroimaging Analysis Suites

| Suite | Interface | Specialties | Open Source | URL |
|-------|-----------|-------------|------------|-----|
| fMRIPrep | Command-line, BIDS | fMRI preprocessing | Yes | [fmriprep.org](https://fmriprep.org/) |
| DPARSF/DPABI | GUI (MATLAB) | Resting-state fMRI processing | Yes | [rfmri.org/DPABI](http://rfmri.org/DPABI) |
| QSIPrep | Command-line, BIDS | Diffusion MRI preprocessing | Yes | [qsiprep.readthedocs.io](https://qsiprep.readthedocs.io/) |
| ANTs | Command-line | Registration, segmentation | Yes | [stnava.github.io/ANTs](https://stnava.github.io/ANTs/) |
| MRtrix3 | Command-line | Diffusion MRI analysis | Yes | [mrtrix.org](https://www.mrtrix.org/) |
| Freesurfer | Command-line | Structural MRI analysis | Yes | [freesurfer.net](https://surfer.nmr.mgh.harvard.edu/) |
| BrainSuite | GUI | Structural/functional MRI analysis | Yes | [brainsuite.org](https://brainsuite.org/) |
| CONN | GUI (MATLAB) | Functional connectivity | Yes | [conn-toolbox.org](https://web.conn-toolbox.org/) |
| Nipype | Python | Pipeline construction | Yes | [nipype.readthedocs.io](https://nipype.readthedocs.io/) |
| BrainVoyager | GUI | Comprehensive MRI analysis | No | [brainvoyager.com](https://www.brainvoyager.com/) |

### Data Management and Sharing

| Tool | Primary Purpose | URL |
|------|----------------|-----|
| BIDS | Data organization standard | [bids-standard.github.io](https://bids-standard.github.io/) |
| OpenNeuro | Data sharing platform | [openneuro.org](https://openneuro.org/) |
| Datalad | Dataset version control | [datalad.org](https://www.datalad.org/) |
| XNAT | Imaging data management | [xnat.org](https://www.xnat.org/) |
| LORIS | Web-based data management | [loris.ca](https://loris.ca/) |
| MRIQC | MRI quality control | [mriqc.readthedocs.io](https://mriqc.readthedocs.io/) |
| PyBIDS | Python library for BIDS datasets | [github.com/bids-standard/pybids](https://github.com/bids-standard/pybids) |

### Visualization Tools

| Tool | Data Types | Interface | URL |
|------|------------|-----------|-----|
| FSLeyes | MRI | GUI | [fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FSLeyes) |
| MRIcroGL | MRI | GUI | [nitrc.org/projects/mricrogl](https://www.nitrc.org/projects/mricrogl) |
| Nilearn plotting | MRI | Python API | [nilearn.github.io/stable/plotting](https://nilearn.github.io/stable/plotting/index.html) |
| BrainNet Viewer | Network data | MATLAB | [nitrc.org/projects/bnv](https://www.nitrc.org/projects/bnv/) |
| Connectome Workbench | Surface data | GUI | [humanconnectome.org/software/connectome-workbench](https://www.humanconnectome.org/software/connectome-workbench) |
| BrainVisa | MRI | GUI | [brainvisa.info](https://brainvisa.info/) |
| 3D Slicer | Multi-modality | GUI | [slicer.org](https://www.slicer.org/) |

## Practical Examples

For hands-on demonstration of these tools, visit our [Examples directory](../Examples/):

- **Comprehensive Neuroscience Workflow**: A complete workflow demonstrating data organization, preprocessing, analysis, visualization, and computational modeling
- **BIDS Organization**: Examples of organizing neuroimaging data according to BIDS standards
- **Neuroimaging Analysis**: Practical demonstrations of fMRI data preprocessing and analysis
- **MVPA Implementation**: Examples of machine learning applied to brain data
- **Computational Modeling**: Working implementations of neural models

These examples integrate the various tools and techniques documented in the Software subdirectories, providing practical context for their application in neuroscience research.

## Installation Guides

### Python Environment Setup

Setting up a comprehensive Python environment for neuroimaging:

```bash
# Create conda environment for neuroimaging
conda create -n neuro python=3.9
conda activate neuro

# Install core neuroimaging packages
conda install -c conda-forge nibabel nilearn numpy scipy matplotlib pandas jupyterlab ipywidgets scikit-learn

# Install MNE for MEG/EEG analysis
pip install mne mne-bids

# BIDS tools
pip install pybids bids-validator

# Workflow tools
pip install nipype

# Quality control
pip install mriqc

# Advanced visualization
pip install plotly pyvista vtk

# For preprocessing pipelines (requires more setup)
pip install fmriprep-docker
```

### Docker-based Installation

Using containerized neuroimaging tools:

```bash
# Pull fMRIPrep container
docker pull nipreps/fmriprep:latest

# Pull MRIQC container
docker pull nipreps/mriqc:latest

# Pull FreeSurfer container
docker pull freesurfer/freesurfer:7.3.2

# Pull FSL container
docker pull brainlife/fsl:6.0.4

# Create a command alias for easier use
echo 'alias fmriprep="docker run -ti --rm \
    -v /path/to/data:/data:ro \
    -v /path/to/output:/out \
    -v /path/to/freesurfer/license.txt:/opt/freesurfer/license.txt:ro \
    nipreps/fmriprep:latest \
    /data /out \
    participant"' >> ~/.bashrc

source ~/.bashrc
```

## Getting Started Guides

### Quick Start with Neuroimaging Analysis

1. **Organize your data in BIDS format**
   - Use the [BIDS Starter Kit](https://github.com/bids-standard/bids-starter-kit)
   - Convert your DICOM files using [dcm2niix](https://github.com/rordenlab/dcm2niix)

2. **Perform quality control**
   - Run MRIQC on your dataset
   - Inspect the reports and exclude problematic data

3. **Preprocess your data**
   - Use fMRIPrep for functional MRI
   - Use QSIPrep for diffusion MRI

4. **Analyze your data**
   - Use Nilearn for statistical learning on neuroimaging data
   - Use FSL or AFNI for traditional GLM analyses
   - Use MNE-Python for MEG/EEG analyses

5. **Create visualizations**
   - Use Nilearn plotting functions for brain maps
   - Use FSLeyes or MRIcroGL for interactive visualization
   - Use BrainNet Viewer for connectome visualization

### Quick Start with Computational Modeling

1. **Choose the appropriate level of detail**
   - Detailed compartmental models → NEURON
   - Spiking neural networks → Brian2, NEST
   - Neural mass models → The Virtual Brain

2. **Install the software**
   - Many simulators can be installed via pip or conda
   - Some may require compilation from source

3. **Start with tutorials and examples**
   - Each simulator provides examples showcasing key features
   - Work through tutorials to understand model construction

4. **Develop your model incrementally**
   - Start simple and gradually add complexity
   - Validate each step against known results or expectations

5. **Document and share your models**
   - Use standardized formats like NeuroML when possible
   - Share code and documentation on GitHub or ModelDB

## Community Resources

### Major Neuroscience Software Communities

- [Neuro Debian](https://neuro.debian.net/): Comprehensive platform for neuroscience software
- [NiPy](https://nipy.org/): Neuroimaging in Python ecosystem
- [NeuroStars](https://neurostars.org/): Q&A forum for neuroscience
- [Brainhack](https://brainhack.org/): Global collaborative community
- [INCF](https://www.incf.org/): International Neuroinformatics Coordinating Facility
- [OHBM](https://www.humanbrainmapping.org/): Organization for Human Brain Mapping

### Mailing Lists and Discussion Forums

- [FSL](https://www.jiscmail.ac.uk/cgi-bin/webadmin?A0=FSL)
- [SPM](https://www.fil.ion.ucl.ac.uk/spm/support/)
- [AFNI](https://afni.nimh.nih.gov/afni/community/board/list.php?1)
- [FreeSurfer](https://www.mail-archive.com/freesurfer@nmr.mgh.harvard.edu/)
- [MNE](https://mail.nmr.mgh.harvard.edu/mailman/listinfo/mne_analysis)
- [Nipype](https://mail.python.org/mailman/listinfo/neuroimaging)
- [BIDS](https://groups.google.com/g/bids-discussion)

### Conferences and Workshops

- **OHBM Annual Meeting**: Largest neuroimaging conference
- **SfN Annual Meeting**: Society for Neuroscience
- **CNS Meeting**: Computational Neuroscience
- **INCF Assembly**: Neuroinformatics
- **Neurohackademy**: Summer institute for neuroimaging and data science
- **BrainHack**: Collaborative workshops worldwide

## Contributing to This Resource

We welcome contributions to improve these software resources! Please follow these guidelines:

1. **Adding new software**: Include name, purpose, URL, and a brief description
2. **Updating information**: Ensure information is accurate and up-to-date
3. **Examples and tutorials**: Practical examples are highly valuable
4. **Installation guides**: Clear installation instructions help new users

To contribute:

1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description of your additions or changes

## License and Usage

These resources are compiled for educational and research purposes. Please respect the licenses of individual software packages when using them.

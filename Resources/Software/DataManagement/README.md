# Neuroimaging Data Management Tools

This directory contains resources related to data management in cognitive neuroscience, including tools for organizing neuroimaging data, standardized formats, quality control, and data sharing platforms.

## Brain Imaging Data Structure (BIDS)

BIDS is a standardized way to organize neuroimaging data and metadata that simplifies data sharing, analysis pipeline development, and collaboration.

### BIDS Overview and Benefits

| Aspect | Description |
|--------|-------------|
| Purpose | Standardized organization of neuroimaging data and metadata |
| Key Benefits | Facilitates sharing, reduces pipeline setup time, improves reproducibility |
| Modalities Supported | MRI, MEG, EEG, iEEG, PET, NIRS, microscopy, and more |
| Adoption | Standard in large initiatives (HCP, ABCD, UK Biobank), required by many journals |
| Validation | Automated validation tools to ensure compliance |
| Extensions | Growing ecosystem of modality-specific extensions |

### BIDS Converter Tools

| Tool | Primary Use | Interface | Key Features | Platform |
|------|-------------|-----------|--------------|----------|
| dcm2bids | DICOM to BIDS conversion | CLI | Simple config file, handles most use cases | Cross-platform |
| HeuDiConv | DICOM to BIDS with flexible heuristics | CLI | Python-based heuristics for complex datasets | Linux, Mac |
| BIDScoin | DICOM/PAR/REC to BIDS | GUI/CLI | User-friendly interface, interactive mode | Cross-platform |
| bidskit | DICOM to BIDS | CLI | Automated pipeline, two-pass process | Cross-platform |
| MNE-BIDS | EEG/MEG to BIDS | Python API | Integration with MNE-Python | Cross-platform |
| BIDS-starter-kit | Teaching and examples | Documentation | Tutorials, templates, and guides | N/A |

### BIDS Directory Structure Example

```
my_study/
├── dataset_description.json
├── participants.tsv
├── participants.json
├── README
├── CHANGES
├── code/
├── derivatives/
├── sub-01/
│   ├── anat/
│   │   ├── sub-01_T1w.nii.gz
│   │   └── sub-01_T1w.json
│   ├── func/
│   │   ├── sub-01_task-rest_bold.nii.gz
│   │   ├── sub-01_task-rest_bold.json
│   │   ├── sub-01_task-rest_events.tsv
│   │   ├── sub-01_task-rest_physio.tsv.gz
│   │   └── sub-01_task-rest_physio.json
│   └── dwi/
│       ├── sub-01_dwi.nii.gz
│       ├── sub-01_dwi.bval
│       ├── sub-01_dwi.bvec
│       └── sub-01_dwi.json
└── ...
```

### Basic BIDS Conversion Example with dcm2bids

```bash
# Install dcm2bids
pip install dcm2bids

# Create a configuration file config.json
cat > config.json << 'EOL'
{
  "descriptions": [
    {
      "dataType": "anat",
      "modalityLabel": "T1w",
      "criteria": {
        "SeriesDescription": "*T1*"
      }
    },
    {
      "dataType": "func",
      "modalityLabel": "bold",
      "customLabels": "task-rest",
      "criteria": {
        "SeriesDescription": "*BOLD*resting*"
      }
    },
    {
      "dataType": "dwi",
      "modalityLabel": "dwi",
      "criteria": {
        "SeriesDescription": "*DWI*"
      }
    }
  ]
}
EOL

# Run the conversion
dcm2bids -d /path/to/dicom/folder -p 01 -c config.json
```

### BIDS Validation

```bash
# Install the BIDS validator
npm install -g bids-validator

# Validate a BIDS dataset
bids-validator /path/to/bids/dataset

# Python implementation
pip install bids-validator
python -c "from bids_validator import BIDSValidator; validator = BIDSValidator(); print(validator.is_bids('/path/to/bids/dataset'))"
```

## Data Quality Control Tools

### QC Software Comparison

| Tool | Modalities | Integration | Automation | Visualization | Output |
|------|------------|-------------|------------|---------------|--------|
| MRIQC | T1w, T2w, BOLD | BIDS | Full pipeline | Interactive reports | JSON metrics, HTML reports |
| fMRIPrep QC | BOLD | BIDS | Via fMRIPrep | HTML reports | Integrated in processing |
| VisualQC | T1w, fMRI, DTI | Custom | Semi-automated | GUI review | QC ratings, outlier detection |
| QSIPrep QC | DTI, DWI | BIDS | Via QSIPrep | HTML reports | Integrated in processing |
| EEG-BIDS QC | EEG | BIDS | Semi-automated | Interactive plots | Report generation |
| PETPrep QC | PET | BIDS | Via PETPrep | HTML reports | Integrated in processing |

### Running MRIQC

```bash
# Install MRIQC
pip install mriqc

# Basic usage
mriqc /path/to/bids/dataset /path/to/output/folder participant

# Run on specific subjects with multiple threads
mriqc /path/to/bids/dataset /path/to/output/folder participant \
    --participant-label 01 02 03 \
    --nprocs 8 \
    --mem_gb 16

# Generate group reports after individual processing
mriqc /path/to/bids/dataset /path/to/output/folder group
```

### Custom QC Metrics with Python

```python
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from nilearn import plotting

def calculate_snr(image_file):
    """Calculate Signal-to-Noise Ratio from a NIfTI file."""
    img = nib.load(image_file)
    data = img.get_fdata()
    
    # Simple SNR calculation (signal mean / signal std)
    # For anatomical images, mask out background first
    mask = data > np.percentile(data, 10)  # Simple threshold-based mask
    signal_mean = np.mean(data[mask])
    signal_std = np.std(data[mask])
    snr = signal_mean / signal_std
    
    return snr

def check_motion(motion_params_file):
    """Analyze motion parameters from fMRI preprocessing."""
    # Load motion parameters (assuming 6 columns: 3 rotation, 3 translation)
    motion = np.loadtxt(motion_params_file)
    
    # Calculate Framewise Displacement
    fd = np.zeros(motion.shape[0])
    for i in range(1, motion.shape[0]):
        # Convert rotational displacements from radians to mm
        # Assumes rotational parameters are in radians and a brain radius of 50 mm
        rot_displacement = motion[i, :3] - motion[i-1, :3]
        rot_displacement = np.abs(rot_displacement) * 50
        
        # Translation displacement in mm
        trans_displacement = np.abs(motion[i, 3:] - motion[i-1, 3:])
        
        # Sum of absolute displacements
        fd[i] = np.sum(rot_displacement) + np.sum(trans_displacement)
    
    return {
        'mean_fd': np.mean(fd),
        'max_fd': np.max(fd),
        'num_fd_above_threshold': np.sum(fd > 0.5),  # Common threshold is 0.5mm
        'percent_fd_above_threshold': np.mean(fd > 0.5) * 100
    }

def plot_qc_report(image_file, output_file, motion_params=None):
    """Create a QC visualization for a neuroimaging file."""
    img = nib.load(image_file)
    
    fig = plt.figure(figsize=(16, 8))
    
    # Plot brain slices
    plt.subplot(2, 3, 1)
    plotting.plot_anat(img, display_mode='ortho', figure=fig, axes=plt.gca())
    plt.title('Orthogonal View')
    
    # Plot histogram of intensities
    plt.subplot(2, 3, 2)
    data = img.get_fdata()
    plt.hist(data.ravel(), bins=100)
    plt.title('Intensity Histogram')
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    
    # Calculate and display SNR
    snr = calculate_snr(image_file)
    plt.subplot(2, 3, 3)
    plt.text(0.5, 0.5, f'SNR: {snr:.2f}', ha='center', va='center', fontsize=20)
    plt.axis('off')
    plt.title('Quality Metrics')
    
    # If motion parameters are provided, plot them
    if motion_params is not None:
        motion = np.loadtxt(motion_params)
        
        # Plot translation parameters
        plt.subplot(2, 3, 4)
        plt.plot(motion[:, 3:])
        plt.title('Translation Parameters')
        plt.xlabel('Timepoint')
        plt.ylabel('mm')
        plt.legend(['x', 'y', 'z'])
        
        # Plot rotation parameters
        plt.subplot(2, 3, 5)
        plt.plot(motion[:, :3])
        plt.title('Rotation Parameters')
        plt.xlabel('Timepoint')
        plt.ylabel('radians')
        plt.legend(['pitch', 'roll', 'yaw'])
        
        # Plot framewise displacement
        motion_metrics = check_motion(motion_params)
        plt.subplot(2, 3, 6)
        fd = motion_metrics['mean_fd']
        plt.text(0.5, 0.5, 
                 f"Mean FD: {fd:.3f} mm\n"
                 f"Max FD: {motion_metrics['max_fd']:.3f} mm\n"
                 f"% High Motion: {motion_metrics['percent_fd_above_threshold']:.1f}%",
                 ha='center', va='center', fontsize=12)
        plt.axis('off')
        plt.title('Motion Metrics')
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
    
    return {
        'snr': snr,
        'motion_metrics': motion_metrics if motion_params is not None else None
    }
```

## Data Storage and Sharing Platforms

### Platform Comparison

| Platform | Cost | Storage Capacity | Privacy Features | Collaboration | Special Features |
|----------|------|------------------|-----------------|---------------|------------------|
| OpenNeuro | Free | Unlimited for open data | Defacing tools, ethics compliance | Version control, DOI | BIDS required, preprocessing pipelines |
| NITRC | Free | Limited | Private/public options | Forums, wikis | Integration with analysis tools |
| XNAT | Self-hosted/Commercial | Scalable | Fine-grained permissions | Project-based | Clinical integration |
| Datalad | Free | Git-based, scalable | Local/remote | Versioning | Provenance tracking |
| Brainlife.io | Free for researchers | Limited | IRB compliance | Open publishing | Online computing |
| Flywheel | Commercial | Enterprise-scale | HIPAA compliant | Workflow integration | Automation, clinical tools |
| LORIS | Free, self-hosted | Scalable | Access control | Multi-site management | Longitudinal studies |
| OSF | Free/paid tiers | 50GB free | Private/public | Collaborative | Integration with other services |

### Setting Up Datalad for Version-Controlled Datasets

```bash
# Install Datalad
pip install datalad

# Create a new dataset
datalad create -d ~/datasets/my_neuroimaging_study

# Navigate to the dataset
cd ~/datasets/my_neuroimaging_study

# Add some files or subdatasets
datalad download-url https://openneuro.org/some_data_example.zip

# Add remote storage (e.g., on GIN - similar to GitHub for data)
datalad siblings add --name gin --url https://gin.g-node.org/username/my_neuroimaging_study.git

# Save the current state
datalad save -m "Add initial data"

# Push to the remote
datalad push --to gin

# Tracking changes
# Make some changes to your files...
datalad save -m "Update preprocessing parameters"

# See the history
datalad diff
```

### Accessing Data from OpenNeuro

```bash
# Using Datalad
datalad install https://github.com/OpenNeuroDatasets/ds000001.git

# Using AWS CLI
aws s3 sync --no-sign-request s3://openneuro.org/ds000001 ds000001-download/

# Using Python
import requests
import os

def download_file(url, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

# Example: download a specific file
download_file(
    'https://openneuro.org/crn/datasets/ds000001/snapshots/1.0.0/files/sub-01/anat/sub-01_T1w.nii.gz',
    'downloads/sub-01_T1w.nii.gz'
)
```

## Data Anonymization and Privacy Tools

### Comparison of Anonymization Tools

| Tool | Modalities | Methods | Customizability | Integration |
|------|------------|---------|-----------------|------------|
| PyDeface | T1-weighted MRI | Face removal | Limited | Command-line, Python |
| mri_deface (FreeSurfer) | T1-weighted MRI | Face removal | Limited | FreeSurfer suite |
| DICOM Confidential | DICOM | Header & pixel data | Configurable | Java application |
| dcm2niix | DICOM to NIfTI | Header cleaning | Basic | Command-line |
| BIDSonym | BIDS datasets | Multiple defacing tools | Configurable | BIDS apps |
| MRI Defacer | T1, T2, FLAIR | Face blurring/removal | Limited | Python library |

### Example: Using PyDeface

```bash
# Install PyDeface
pip install pydeface

# Basic usage
pydeface /path/to/input/T1w.nii.gz

# Specify output file
pydeface /path/to/input/T1w.nii.gz --outfile /path/to/output/T1w_defaced.nii.gz

# Batch processing with a script
cat > deface_all.sh << 'EOL'
#!/bin/bash
# Deface all T1w images in a BIDS dataset

BIDS_DIR=$1
OUTPUT_DIR=$2

mkdir -p "$OUTPUT_DIR"

for t1_file in $(find "$BIDS_DIR" -name "*T1w.nii.gz"); do
    sub_dir=$(dirname $(dirname "$t1_file"))
    sub_id=$(basename "$sub_dir")
    anat_dir="$OUTPUT_DIR/$sub_id/anat"
    mkdir -p "$anat_dir"
    out_file="$anat_dir/$(basename "$t1_file" .nii.gz)_defaced.nii.gz"
    echo "Defacing $t1_file -> $out_file"
    pydeface "$t1_file" --outfile "$out_file"
done
EOL

chmod +x deface_all.sh
./deface_all.sh /path/to/bids/dataset /path/to/output/dataset
```

### DICOM Header Cleaning Example

```python
import pydicom
import os
import glob

# Tags that should be removed or modified for anonymization
# Based on DICOM standard PS3.15 Annex E (Basic Profile)
TAGS_TO_REMOVE = [
    (0x0008, 0x0014),  # Instance Creator UID
    (0x0008, 0x0018),  # SOP Instance UID (replace)
    (0x0008, 0x0050),  # Accession Number
    (0x0008, 0x0080),  # Institution Name
    (0x0008, 0x0081),  # Institution Address
    (0x0008, 0x0090),  # Referring Physician's Name
    (0x0008, 0x0092),  # Referring Physician's Address
    (0x0008, 0x0094),  # Referring Physician's Telephone
    (0x0008, 0x1010),  # Station Name
    (0x0008, 0x1030),  # Study Description
    (0x0008, 0x103E),  # Series Description
    (0x0008, 0x1040),  # Institutional Department Name
    (0x0008, 0x1048),  # Physician(s) of Record
    (0x0008, 0x1050),  # Performing Physician's Name
    (0x0008, 0x1060),  # Name of Physician(s) Reading Study
    (0x0008, 0x1070),  # Operators' Name
    (0x0008, 0x1080),  # Admitting Diagnoses Description
    (0x0010, 0x0010),  # Patient's Name
    (0x0010, 0x0020),  # Patient ID
    (0x0010, 0x0030),  # Patient's Birth Date
    (0x0010, 0x0032),  # Patient's Birth Time
    (0x0010, 0x0040),  # Patient's Sex
    (0x0010, 0x0050),  # Patient's Insurance Plan Code Sequence
    (0x0010, 0x0101),  # Patient's Primary Language Code Sequence
    (0x0010, 0x1000),  # Other Patient IDs
    (0x0010, 0x1001),  # Other Patient Names
    (0x0010, 0x1010),  # Patient's Age
    (0x0010, 0x1020),  # Patient's Size
    (0x0010, 0x1030),  # Patient's Weight
    (0x0010, 0x1090),  # Medical Record Locator
    (0x0010, 0x2160),  # Ethnic Group
    (0x0010, 0x2180),  # Occupation
    (0x0010, 0x21B0),  # Additional Patient's History
    (0x0010, 0x4000),  # Patient Comments
    (0x0020, 0x000D),  # Study Instance UID (replace)
    (0x0020, 0x000E),  # Series Instance UID (replace)
    (0x0020, 0x0010),  # Study ID
    (0x0020, 0x0052),  # Frame of Reference UID (replace)
    (0x0020, 0x0200),  # Synchronization Frame of Reference UID (replace)
    (0x0020, 0x4000),  # Image Comments
    (0x0040, 0x0275),  # Request Attributes Sequence
]

def anonymize_dicom(dicom_file, output_dir):
    """Anonymize a DICOM file by removing patient identifiers."""
    # Read the DICOM file
    ds = pydicom.dcmread(dicom_file)
    
    # Replace patient name and ID with anonymous values
    ds.PatientName = "ANONYMOUS"
    ds.PatientID = "SUBJ_" + os.path.basename(dicom_file)[:8]
    
    # Remove birth date
    if hasattr(ds, 'PatientBirthDate'):
        delattr(ds, 'PatientBirthDate')
    
    # Process all other tags
    for tag in TAGS_TO_REMOVE:
        if tag in ds:
            # Special handling for UIDs - replace instead of remove
            if tag in [(0x0008, 0x0018), (0x0020, 0x000D), (0x0020, 0x000E), (0x0020, 0x0052)]:
                ds[tag].value = pydicom.uid.generate_uid()
            else:
                # For other tags, simply delete them
                del ds[tag]
    
    # Save the anonymized file
    output_file = os.path.join(output_dir, os.path.basename(dicom_file))
    ds.save_as(output_file)
    return output_file

def batch_anonymize(input_dir, output_dir):
    """Anonymize all DICOM files in a directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all DCM files
    dicom_files = glob.glob(os.path.join(input_dir, "**/*.dcm"), recursive=True)
    
    # Process each file
    for file in dicom_files:
        relative_path = os.path.relpath(file, input_dir)
        output_subdir = os.path.join(output_dir, os.path.dirname(relative_path))
        os.makedirs(output_subdir, exist_ok=True)
        
        output_file = os.path.join(output_subdir, os.path.basename(file))
        try:
            anonymize_dicom(file, output_subdir)
            print(f"Processed: {file} -> {output_file}")
        except Exception as e:
            print(f"Error processing {file}: {e}")

# Example usage
batch_anonymize("/path/to/dicom/files", "/path/to/anonymized/output")
```

## Data Provenance and Reproducibility

### Tools for Tracking Data Provenance

| Tool | Primary Use | Integration | Special Features |
|------|-------------|-------------|-----------------|
| Git-Annex | Version control for large files | Git, Datalad | Distributed storage |
| Datalad | Dataset versioning and distribution | Git-Annex | Nested datasets, provenance |
| Nipype | Workflow management | Many neuroimaging tools | Pipeline provenance |
| BIDS Apps | Standardized processing | BIDS | Containerized workflows |
| ReproNim | Computational environment | Various | Reproducible neuroimaging |
| DataLad Containers | Environment tracking | Datalad | Container versioning |
| Reprozip | Computational environment capture | Linux | Trace dependencies |

### Example: Nipype Workflow with Provenance Tracking

```python
import os
from nipype import Workflow, Node, MapNode, Function
from nipype.interfaces.fsl import BET, FAST
from nipype.interfaces.utility import IdentityInterface
from nipype.interfaces.io import DataSink

# Set up directories
experiment_dir = '/path/to/experiment'
output_dir = os.path.join(experiment_dir, 'output')
working_dir = os.path.join(experiment_dir, 'workingdir')

# Create workflow
wf = Workflow(name='structural_preprocessing')
wf.base_dir = working_dir

# Input node
inputnode = Node(IdentityInterface(fields=['T1']), name='inputnode')
inputnode.inputs.T1 = ['/path/to/subject1/T1.nii.gz', '/path/to/subject2/T1.nii.gz']

# Skull stripping
bet = MapNode(BET(), name='bet', iterfield=['in_file'])
bet.inputs.frac = 0.5
bet.inputs.mask = True
bet.inputs.robust = True

# Tissue segmentation
segment = MapNode(FAST(), name='segment', iterfield=['in_files'])
segment.inputs.number_classes = 3

# DataSink for saving outputs
datasink = Node(DataSink(), name='datasink')
datasink.inputs.base_directory = output_dir
datasink.inputs.container = 'structural_preprocessing'

# Connect nodes
wf.connect([
    (inputnode, bet, [('T1', 'in_file')]),
    (bet, segment, [('out_file', 'in_files')]),
    (bet, datasink, [('out_file', 'bet.@out_file'),
                     ('mask_file', 'bet.@mask_file')]),
    (segment, datasink, [('segmentation_file', 'segment.@segmentation_file'),
                         ('tissue_class_files', 'segment.@tissue_files')])
])

# Run workflow with provenance tracking
wf.config['execution'] = {'hash_method': 'content',  # Track content, not just filenames
                          'stop_on_first_crash': True,
                          'remove_unnecessary_outputs': False,  # Keep all outputs for provenance
                          'use_relative_paths': True,  # More portable
                          'keep_inputs': True}  # Store inputs for complete provenance

wf.write_graph(graph2use='flat', format='png')  # Save workflow graph
wf.write_graph(graph2use='colored', format='svg')

# Run workflow
result = wf.run()

# After running, the provenance information is stored in working_dir
# You can package it for sharing:
import tarfile
with tarfile.open(os.path.join(experiment_dir, 'provenance.tar.gz'), 'w:gz') as tar:
    tar.add(working_dir, arcname=os.path.basename(working_dir))
    # Include scripts and configuration
    tar.add(__file__, arcname=os.path.basename(__file__))
```

## Best Practices for Data Management

### Data Organization

1. **Consistency is Key**
   - Use consistent naming conventions
   - Organize similar data together
   - Document your organization scheme

2. **Follow Standards When Possible**
   - Use BIDS for neuroimaging data
   - Consider EEG-BIDS for EEG data
   - Adopt the FAIR principles

3. **Hierarchical Structure**
   - Group by project, then participant, then session, then data type
   - Clear separation between raw data and derivatives
   - Dedicated space for code and documentation

### Data Collection

1. **Plan Before You Start**
   - Design data management plan before data collection
   - Create templates for collection forms/protocols
   - Test procedures before full data collection

2. **Quality Control During Collection**
   - Real-time QC when possible
   - Regular checks of collected data
   - Document any issues or deviations

3. **Metadata Collection**
   - Collect rich metadata during acquisition
   - Use standardized forms when possible
   - Create a data dictionary

### Data Preservation

1. **Backup Strategy**
   - 3-2-1 rule: 3 copies, 2 different media, 1 off-site
   - Automated, regular backups
   - Test restoration procedures periodically

2. **File Formats**
   - Use open, non-proprietary formats when possible
   - Convert proprietary formats to open ones for long-term storage
   - Include format documentation

3. **Version Control**
   - Track changes to data and code
   - Document processing steps and parameters
   - Use tools like Git, DataLad, or OSF

### Data Sharing

1. **Ethical and Legal Considerations**
   - Get appropriate consent for sharing
   - De-identify data properly
   - Understand institutional requirements

2. **Choose Appropriate Repositories**
   - Domain-specific repositories when possible
   - Consider visibility, longevity, and accessibility
   - Ensure repository has DOI capability

3. **Documentation for Reuse**
   - Include detailed README files
   - Provide processing scripts and parameters
   - Document limitations and known issues

### Template Data Management Plan

```markdown
# Data Management Plan for [Project Name]

## 1. Data Collection and Organization
* **Data types:** [List all data types: MRI, EEG, behavioral, etc.]
* **Organization structure:** BIDS-compliant organization
* **Naming conventions:** [Describe naming conventions]
* **Quality control procedures:** [Describe QC procedures]

## 2. Data Storage and Security
* **Storage locations:** [Primary storage, backup locations]
* **Backup schedule:** [Frequency of backups]
* **Access controls:** [Who has access and how]
* **Security measures:** [Encryption, authentication, etc.]

## 3. Data Processing and Analysis
* **Software tools:** [List key software]
* **Workflow management:** [Describe workflow tools]
* **Version control:** [Git repository details]
* **Computational environment:** [Containers, virtual environments]

## 4. Data Sharing and Publication
* **Sharing platform:** [OpenNeuro, OSF, etc.]
* **Timeline for sharing:** [When data will be shared]
* **Access restrictions:** [Any restrictions on shared data]
* **Citation information:** [How to cite the dataset]

## 5. Roles and Responsibilities
* **Data manager:** [Name, contact]
* **Data collection team:** [Names or roles]
* **Data analysis team:** [Names or roles]
* **IT support:** [Contact information]

## 6. Budget
* **Storage costs:** [Estimated costs]
* **Personnel time:** [Estimated time allocation]
* **Software licenses:** [If applicable]
* **Repository fees:** [If applicable]

## 7. Timeline
* **Data collection period:** [Start and end dates]
* **Processing milestones:** [Key processing dates]
* **Quality control reviews:** [QC review schedule]
* **Sharing deadlines:** [When data will be published]
```

## Learning Resources

### Books and Guides

1. **Handbooks and Guides**
   - "The BIDS Starter Kit" - [GitHub Repository](https://github.com/bids-standard/bids-starter-kit)
   - "The Practice of Reproducible Research" by Kitzes, Turek, & Deniz
   - "Principles of Data Management and Presentation" by John P. Hoffmann

2. **Online Resources**
   - [ReproNim Training](https://www.repronim.org/training.html)
   - [INCF Training](https://training.incf.org/)
   - [OpenNeuro Documentation](https://openneuro.org/documentation)
   - [Scientific Data Management Guide](https://www.nature.com/articles/sdata201618)

### Courses and Workshops

1. **Online Courses**
   - [Neurohackademy](https://neurohackademy.org/) - Summer institute
   - [OHBM Educational Course on Data Management](https://www.humanbrainmapping.org/)
   - [Research Data Management on Coursera](https://www.coursera.org/learn/data-management)

2. **Workshops**
   - BrainHack - Regular events worldwide
   - INCF workshops on neuroinformatics
   - ReproNim webinars and training events

### Communities and Forums

1. **Online Communities**
   - [NeuroStars](https://neurostars.org/) - Q&A forum
   - [BIDS Google Group](https://groups.google.com/g/bids-discussion)
   - [ReproNim Discussion Forum](https://community.repronim.org/)
   - [Research Data Alliance](https://www.rd-alliance.org/)

2. **Conferences with Data Management Focus**
   - Organization for Human Brain Mapping (OHBM)
   - International Conference on Biomedical and Health Informatics
   - Research Data Alliance (RDA) Plenaries

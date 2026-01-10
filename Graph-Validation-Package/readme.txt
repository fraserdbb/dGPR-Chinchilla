dGPR Monte Carlo Graph Validation

Authored and Developed by Daniel B. B. Fraser

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Important End-User Information:

It is recommended that this package is run from the C drive of your
workstation, due to path handling issues encountered during development.
It is possible to run on separate drives, but may take manual
configuration.

Expected user inputs for each validation can be found in the
documentation of the respective sub-folders.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validated Workstation Specifications:

CPU: Intel Core i7 13700kf
GPU: nVidia RTX 4090
RAM: 64GB 5200MHz DDR5

This package can be computationally intensive due to the subdivision
method used for voxelization, as such, I cannot confirm whether it would
function on a workstation with lower compute or memory capacity than the
above validated specifications.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dependencies (verified with the pipreqs package):

Numpy 2.4.0

Trimesh[easy] 4.10.0

Matplotlib 3.10.8


These can be installed via the pip installer with the following
command line argument:

pip install [package name]==[version number]


For reference, Trimesh[easy] is listed for sub-dependencies.


Additionally, the Monte Carlo eXtreme - CUDA edition package version 2.8 
(v2025.10, Kilo-Kelvin), which can be found at https://mcx.space/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package represents mathematical proof for the MCX graphs provided in
the Appendix section of the paper "Novel Application of Stereotaxically
Guided Dental Germinative Photodynamic Regulation in Chinchilla lanigera
with Refractory Malocclusion".

The contained files are intentionally hard-coded structures, to ensure
reproducibility in results, for validation purposes.
 
No parameter tuning or interactive input is required or expected for 
operation. This allows for the graphs to be validated with relative ease.

This package is not intended or designed for general-purpose MCX
experimentation or clinical planning.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Optical parameters for rabbit tissue and human pulp (considered best
available match due to lack of optical properties of Chinchilla lanigera
tissues) were sourced from the following papers:

Fu, Y & Jacques, S. L. (2011). Monte Carlo Simulation for Light Propagation
	in 3D tooth model. Optical Interactions with Tissues and Cells XXII,
	SPIE: Bellingham, WA, USA. https://doi.org/10.1117/12.873603

Shanshool, A. S. et al. (2022). Optical Properties and Fluence Distribution
	in Rabbit Head Tissues at Selected Laser Wavelengths. Materials,
	15(16), 5696. https://doi.org/10.3390/ma15165696

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The MCX software was established in the following paper, as such, it 
covers the foundational concepts necessary for these simulations.

Fang, Q. & Boas, D. A. (2009). Monte Carlo Simulation of Photon Migration 
in 3D Turbid Media Accelerated by Graphics Processing Units. Optics 
Express, 17(22), 20178-20190. https://doi.org/10.1364/oe.17.020178

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Segment models of the Chinchilla lanigera maxilla used were derived from 
CT data sourced from the Natural History Museum of Los Angeles County 
via Morphosource:

Natural History Museum of Los Angeles County (2020). Chinchilla lanigera 
	Skull DICOM [Data Set]. MorphoSource. 
	https://www.morphosource.org/concern/media/000114253

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

License & Copyright

This project is dual-licensed due to scope:

Software code (Python Scripts) are licenced under the GNU General Public
License v3.0 (GPLv3). You may copy, distribute, and modify the software as
long as you track the changes and release modifications under the same 
license.

Documentation and Papers (PDFs, Protocol Text, and Guide Specifications) 
are licensed under Creative Commons Attribution-ShareAlike 4.0
International (CC BY-SA 4.0). To view a copy of this license, visit 
https://creativecommons.org/licenses/by-sa/4.0/

dGPR Monte Carlo Simulation - Maxillary Incisor

Dependencies:
Numpy 2.4.0
Trimesh[easy] 4.10.0
Matplotlib 3.10.8

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
Filepaths may have to be adjusted for user system, original code used 
full length file paths. For ease of use, it is recommended to run from 
the C drive, as issues were encountered when running MCX using other 
drives. Programs should be run in the following order, using the 
commands provided:

cd (current working directory)

python STLtoVoxel.py

mcx --input MCXincisor.json -F mc2

python ApoptosisVisualizer

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Explanation of MCXincisor.json:

{
  "Session": {
    "ID": "Chinchilla_25um",
    "Photons": 500000000,	#500 million photons for fluid results
    "RNGSeed": 4982598		#fixed seed for reproducibility
  },
  "Forward": {
    "T0": 0.0,			#starting position, 0 time passage
    "T1": 5e-10,		#ending position, 0.5 nanoseconds past start
    "Dt": 1e-10			#intervals, 0.1 nanoseconds per interval
  },
  "Optode": {
    "Source": {
      "Type": "isotropic",	#Isotropic source to simulate cylindrical diffuser
      "Pos": [399, 137, 101],	#center of fiber tip
      "Dir": [1.0, 0.0, 0.0],
      "Param1": [1, 1, 1, 1],
      "Param2": [0, 0, 0, 0]
    },
    "Detector": [
      { "Pos": [399, 137, 101], "R": 10.0 }	#placeholder detector
    ]
  },
  "Domain": {
    "VolumeFile": "tooth_25um_FINAL.bin",		#filepath may need user adjustment, the original code used full file paths
    "Dim": [781, 504, 366],				#grid dimensions
    "LengthUnit": 0.025,				#Voxel size
    "VolumeFormat": "C",
    "Media": [
      {"mua": 0.12,  "mus": 6.2,  "g": 0.83, "n": 1.368}, #Rabbit Neural Tissue (Shanshool et al., 2022)
      {"mua": 0.12,  "mus": 6.2,  "g": 0.83, "n": 1.368}, #Rabbit Neural Tissue (Shanshool et al., 2022)
      {"mua": 0.30,  "mus": 7.8,  "g": 0.81, "n": 1.370}, #Rabbit Cranial Bone (Shanshool et al., 2022)
      {"mua": 0.035,  "mus": 10.0,  "g": 0.97, "n": 1.370}, #Human Pulp, using n value from Rabbit tissue (Fu & Jacques, 2011; Shanshool et al., 2022)
      {"mua": 1000.0,  "mus": 100.0,  "g": 0.01, "n": 1.000}, #Resin, generic opaque
      {"mua": 1000.0,  "mus": 100.0,  "g": 0.01, "n": 1.000}, #Steel, generic opaque
      {"mua": 1000.0,  "mus": 100.0,  "g": 0.01, "n": 1.000}, #Fiber coating, generic opaque
      {"mua": 0.01,  "mus": 0.1,  "g": 0.99, "n": 1.460} #Fiber core, generic near-transparent
      {"mua": 1000.0,  "mus": 100.0,  "g": 0.01, "n": 1.000} #Fiber cap, generic opaque
    ]
  }
}
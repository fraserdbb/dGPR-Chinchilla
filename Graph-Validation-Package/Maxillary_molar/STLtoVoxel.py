"""
STL to Voxel Converter for Maxillary Molar Fluence Simulation
Developed by Daniel B. B. Fraser

Description:
    This script loads multiple different STL meshes, which represent different tissues and materials.
    The script then voxelizes the loaded meshes at the specified resolution (labeled 'pitch'), and
    merges them into a labeled, 3D, binary volume.

    It uses an algorithm to label a set of meshes in 3D space in a set order, 
    overwriting previous labels. Thus ensuring that overlapping regions are assigned to
    the highest priority material.

Dependencies:
    > Numpy 2.4.0
    > Trimesh[easy] 4.10.0

Usage:
    Ensure the STL files listed in Mesh Loading are present in the same folder.
    Run: python STLtoVoxel.py
"""

import numpy as np # for data processing (like minimum and maximum functions)
import trimesh # for 3D mesh handling

# ~~~Output Configuration~~~
pitch = 0.025 # resolution setter; currently 25um voxels
output_filename = "tooth_25um_FINAL.bin"

BACKGROUND_LABEL = 1   # label background; allows it to be set as tissue

# ~~~Mesh Loading~~~
print("Loading STL files...")
meshes = {
    2: trimesh.load('maxilla_fixed.stl'),
    3: trimesh.load('pulp.stl'),
    4: trimesh.load('resin.stl'),
    5: trimesh.load('steel.stl'),
    6: trimesh.load('fiberCoated.stl'),
    7: trimesh.load('fiberUncoated.stl'),
}

# ~~~Mesh Labeling~~~
labeling_order = [3, 2, 4, 5, 6, 7] # processes label order, later labels override prior labels

def voxel_origin(vox): # determine the origin point for the mesh
    return vox.points.min(axis=0) - pitch / 2

# create grid based on Maxilla
mesh_bone = meshes[2]
print("Creating master grid from Maxilla...")
master_vox = mesh_bone.voxelized(pitch=pitch, method='subdivide', max_iter=20)
grid_shape = master_vox.matrix.shape
origin = voxel_origin(master_vox)

# provide the grid shape for later parameters
print("Master grid origin:", origin)
print(f"Master grid shape (raw): {grid_shape}")

vol_data = np.zeros(grid_shape, dtype=np.uint8) # start with vacuum grid

bounds = meshes[2].bounds  # set grid boundaries based on Maxilla bounds

# calculate points relative to the origin
vmin = np.floor((bounds[0] - origin) / pitch).astype(int)
vmax = np.ceil((bounds[1] - origin) / pitch).astype(int)

# ensure points stay within the maxilla grid
vmin = np.maximum(vmin, 0)
vmax = np.minimum(vmax, grid_shape)

# set the region within the bounds
region = vol_data[
    vmin[0]:vmax[0],
    vmin[1]:vmax[1],
    vmin[2]:vmax[2]
]

# Label the background to allow tissue parameter assignment
region[region == 0] = BACKGROUND_LABEL

# ~~~Voxelization~~~
def voxelize(mesh):
    # voxelize the current mesh with subdivision
    v = mesh.voxelized(pitch=pitch, method='subdivide', max_iter=20)
    try:
        v = v.fill() # attempt to fill internal voids
    except:
        print("~~~~~~~~ voxel filling failed, data may be compromised ~~~~~~~~")
        pass # keep surface if fill fails
    return v

# ~~~Voxel Labeling~~~
def label(mesh, label_id):
    vox = voxelize(mesh)
    vox_origin = voxel_origin(vox)

    # convert world coordinates to index coordinates
    offset = np.round((vox_origin - origin) / pitch).astype(int)
    d0, d1, d2 = offset

    # Dimensions of the local mesh
    s0, s1, s2 = vox.shape

    # Calculate start and end for the local mesh
    start0, end0 = d0, d0 + s0
    start1, end1 = d1, d1 + s1
    start2, end2 = d2, d2 + s2

    # Clip to master volume boundaries
    m_s0, m_e0 = max(start0, 0), min(end0, grid_shape[0])
    m_s1, m_e1 = max(start1, 0), min(end1, grid_shape[1])
    m_s2, m_e2 = max(start2, 0), min(end2, grid_shape[2])

    # Slice ranges for the local array
    l_s0 = m_s0 - start0
    l_s1 = m_s1 - start1
    l_s2 = m_s2 - start2

    l_e0 = l_s0 + (m_e0 - m_s0)
    l_e1 = l_s1 + (m_e1 - m_s1)
    l_e2 = l_s2 + (m_e2 - m_s2)

    # Get the mask from the local voxel grid
    mask = vox.matrix[l_s0:l_e0, l_s1:l_e1, l_s2:l_e2]

    # label the mask onto the master volume
    region = vol_data[m_s0:m_e0, m_s1:m_e1, m_s2:m_e2]
    region[mask] = label_id
    vol_data[m_s0:m_e0, m_s1:m_e1, m_s2:m_e2] = region

# ~~~Labeling Logic~~~
for label_id in labeling_order:
    if label_id in meshes:
        print(f"labeling label {label_id}...")
        label(meshes[label_id], label_id)
    else:
        print(f"Warning: Label {label_id} not found in meshes.")

print("Voxel labeling complete.")

# ~~~Generate Output File~~~
vol_mcx = np.transpose(vol_data, (2, 1, 0))
vol_mcx.tofile(output_filename)

# ~~~Output Diagnostics~~~
print("~" * 30)
print(f"Saved {output_filename}")
print(f"Final Shape (X, Y, Z): {vol_mcx.shape}")
print("~" * 30)
print("UPDATE YOUR JSON WITH THESE VALUES:")
print(f' "Dim": {list(vol_mcx.shape)}')
print("~" * 30)

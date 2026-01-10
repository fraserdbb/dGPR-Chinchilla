"""
Apoptosis Visualizer for Maxillary Molar Fluence Simulation
Developed by Daniel B. B. Fraser

Description:
    This script loads the volumes from STLtoVoxel.py alongside fluence results from MCX in order to
    make a colour-coded, safety-tiered slice diagram of the dGPR procedure. 

Dependencies:
    > Numpy 2.4.0
    > Matplotlib 3.10.8

Usage:
    Ensure the volume bin file (from STLtoVoxel.py) and the fluence mc2 file from MCX are both present.
    Run: python ApoptosisVisualizer.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# ~~~ Configuration ~~~
nx, ny, nz = 196, 584, 305
vol_path = "tooth_25um_FINAL.bin"
flux_path = "chinchilla_25um.mc2"

# ~~~ Calibration ~~~
# this value can be adjusted for different J/cm^2 values (multiply by photons from MCX json)
CALIBRATION_SCALAR = 4e-8 

# ~~~ Thresholds (J/cm^2) ~~~
# these are based on Porphysome literature (Kato et al., 2017; Sahovaler et al., 2024)
KILL_THRESHOLD = 100.0   # near-complete ablation threshold
SAFE_THRESHOLD = 10.0   # partial-ablation threshold

def load_and_plot_zones():
    # load geometry from the volume file
    try:
        vol = np.fromfile(vol_path, dtype=np.uint8)
        vol = vol.reshape((nz, ny, nx))
        vol = np.transpose(vol, (2, 1, 0)) # [X, Y, Z]
    except Exception as e:
        print(f"Error loading geometry: {e}"); return

    # load fluence from the MCX simulation output
    try:
        flux_raw = np.fromfile(flux_path, dtype=np.float32)
        nt = flux_raw.size // (nx*ny*nz)
        flux_cw = flux_raw.reshape((nt, nz, ny, nx)).sum(axis=0)
        flux_cw = np.transpose(flux_cw, (2, 1, 0))
    except Exception as e:
        print(f"Error loading fluence: {e}"); return

    # apply calibration to get fluence in J/cm^2
    real_fluence = flux_cw * CALIBRATION_SCALAR
    
    # slice at center of fiber tip
    slice_idx = 332
    if slice_idx >= ny: slice_idx = ny // 2
    
    geo_slice = vol[:, slice_idx, :]
    flux_slice = real_fluence[:, slice_idx, :]

    # create discrete masks
    # apoptosis mask
    mask_kill = np.ma.masked_where(flux_slice < KILL_THRESHOLD, flux_slice)
    
    # partial apoptosis mask (desired outcome)
    mask_warn = np.ma.masked_where((flux_slice >= KILL_THRESHOLD) | (flux_slice < SAFE_THRESHOLD), flux_slice)
    
    # 'safe' mask (minimal clinical effect)
    mask_safe = np.ma.masked_where(flux_slice >= SAFE_THRESHOLD, flux_slice)

    # display maximal fluence in any voxel
    print(f"Peak Fluence at Tip (with Scalar {CALIBRATION_SCALAR:.0e}): {np.max(flux_slice):.1f} J/cm2")

    # ~~~ Plotting ~~~
    plt.figure(figsize=(10, 8))
    
    # background anatomy (grey)
    plt.imshow(np.rot90(geo_slice), cmap='gray', aspect='auto', alpha=1.0)
    
    # partial apoptosis overlay (yellow/orange)
    cmap_warn = ListedColormap(['yellow'])
    plt.imshow(np.rot90(mask_warn > 0), cmap=cmap_warn, aspect='auto', alpha=0.4, interpolation='none')
    
    # near-complete apoptosis overlay (red)
    cmap_kill = ListedColormap(['red'])
    plt.imshow(np.rot90(mask_kill > 0), cmap=cmap_kill, aspect='auto', alpha=0.6, interpolation='none')

    # colour-coded legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.6, label=f'Apoptosis Zone (> {KILL_THRESHOLD} J/cm²)'),
        Patch(facecolor='yellow', alpha=0.4, label=f'Risk/Warning ({SAFE_THRESHOLD}-{KILL_THRESHOLD} J/cm²)'),
        Patch(facecolor='black', alpha=0.1, label=f'Safe Zone (< {SAFE_THRESHOLD} J/cm²)')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title(f"Safety Threshold Map\nCalibrated Peak: {np.max(flux_slice):.0f} J/cm²")
    plt.show()

if __name__ == "__main__":
    load_and_plot_zones()
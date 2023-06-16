# SO3_analysis

# Jupyter notebooks and shell scripts for computing and analyzing EKE in FESOM simulations on the SO3 mesh.

'eke_calcs_sample_1950s' demonstrates how eke is calculated from the model output data using cdo (see https://code.mpimet.mpg.de/projects/cdo). This method can be applied to other datasets, including from AWI-CM in CMIP6 and from geostrophic velocities from Altimetry observations. For code used to calculate geostrophic velocities from sea surface height data from AWI-CM-1-1-MR in CMIP6, see https://doi.org/10.5281/zenodo.7050573.

'so3_eke_interp.py' and 'c6_eke_interp.py' interpolate EKE data from the native FESOM grids to regular grids. 

Data is visualized in the figure_notebooks folder. Many visualizations are based on pyfesom2 (see https://github.com/FESOM/pyfesom2).

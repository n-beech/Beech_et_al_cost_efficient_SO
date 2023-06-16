import xarray as xr
import numpy as np
import datetime as dt
import pyfesom2 as pf
import matplotlib.tri as mtri
from joblib import Parallel, delayed

datapath='/PATH/TO/DATA/'
mesh_path='/PATH/TO/MESH/DATA/'
mesh=pf.load_mesh(mesh_path)
model_lons=mesh.x2
model_lats=mesh.y2
elements=mesh.elem.astype('int32')

d = model_lons[elements].max(axis=1) - model_lons[elements].min(axis=1)
no_cyclic_elem = np.argwhere(d < 100).ravel()

#regular grid for interpolation
dx=0.25
dy=0.25
left,right=-179.875,180
bottom,top=-89.875,90
nx2=left-right #just to make sure the grid isn't square (makes it easier to keep track of dimensions)
ny2=top-bottom
lon_eq = np.arange(left, right, dx) 
lat_eq = np.arange(bottom, top, dy)
nx=lon_eq.shape[0]
ny=lat_eq.shape[0]

xx_eq, yy_eq = np.meshgrid(lon_eq, lat_eq)
xx_eq=xx_eq.T;
yy_eq=yy_eq.T;

triang = mtri.Triangulation(model_lons, model_lats, elements[no_cyclic_elem])
tri = triang.get_trifinder()

def convert_to_reg(i):
    return mtri.LinearTriInterpolator(triang, data.uo[i,:].data,trifinder=tri)(xx_eq, yy_eq)

for year in ['2091-2095']:
    for run in ['r1','r2','r3','r4','r5']:

        data=xr.open_dataset(datapath+'c6_eke_5d_nol_'+run+'_'+year+'.nc')
        regout=Parallel(n_jobs=-1,batch_size=1,verbose=10,backend='threading')(delayed(convert_to_reg)(i) for i in np.arange(len(data.time)))

        data_interp=xr.DataArray(data=regout,dims=['time','lon','lat'],name='eke',
                                coords={'time':data.time.values,'lon':lon_eq,'lat':lat_eq},
                                attrs=dict(description='eke computed from geostrophic velocities from cmip6 data, coarsened to 5day means w/o leap years, and interpolated to a regular grid',
                                       units='m^2/s^2'))

        data_ds=data_interp.to_dataset(name='eke')
        data_ds.to_netcdf(datapath+'c6_eke_5d_nol_'+run+'_reg_'+year+'.nc')

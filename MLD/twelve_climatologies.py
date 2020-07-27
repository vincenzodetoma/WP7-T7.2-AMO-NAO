import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys

variable='somxl010'

surf_path='/home/Vincenzo.DeToma/wp7/MLD'

ds = xr.open_dataset(surf_path+'/somxl010_ORCA-0.25x0.25_regular_1979_2017.nc')
var = ds[variable].copy()

twelve_climatologies = var.groupby('time.month').mean('time').rename(r'$MLD~[m]$')
twelve_climatologies = twelve_climatologies.assign_coords({'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']})

p = twelve_climatologies.plot.contourf(transform=ccrs.PlateCarree(), 
                                       col='month',
                                       col_wrap=2,
                                       sharex=True, sharey=True,
                                       extend='both', #figsize=(5,6),
                                       levels=[10,20,30,40,50,60,70,80,90,100,125,150,200,300,500],
                                       cmap='jet',
                                       cbar_kwargs={'spacing':'uniform', 'shrink' : 0.80, 
                                                    'orientation' : 'horizontal', 'pad':0.05},
                                       infer_intervals=True,
                                       subplot_kws={"projection": ccrs.Robinson()})

for ax in p.axes.flat:
  ax.coastlines()
  #ax.set_aspect("equal")

p.fig.savefig(surf_path+'/'+variable+'_twelve_clim_ORCA-0.25x0.25_regular_1979_2017.png', dpi=300, transparent=True, bbox_inches='tight')
  
#plt.show()
ds.close()

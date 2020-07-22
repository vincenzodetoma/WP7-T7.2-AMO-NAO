import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import sys

data_path='/DataArchive/C3S/subsurf_temp/Results'
name_file='thetao_1m_ORCA-0.25x0.25_regular_1979_2018.nc'
name_var='thetao1'

ds = xr.open_dataset(data_path+'/'+name_file)
var=ds[name_var]

#bounds for calculation
lat_s = 0.
lat_n = 60.
lon_w = 285.
lon_e = 352.5
weights=np.cos(ds.lat*np.pi/180.).sel(lat=slice(lat_s, lat_n))
amo_index = var.sel(lat=slice(lat_s, lat_n), lon=slice(lon_w, lon_e)).weighted(weights).mean(dim=['lat', 'lon'])


climatology_mean = amo_index.groupby("time.month").mean('time')
anomalies = xr.apply_ufunc(
    lambda x, m: (x - m),
    amo_index.groupby("time.month"),
    climatology_mean,
)

fig=plt.figure(1, figsize=(9,4))
ax=fig.add_subplot(111)
ax.plot(np.linspace(1979, 2018, 480), anomalies, lw=1, color='k')
ax.axhline(0., color='k')
ax.fill_between(np.linspace(1979, 2018, 480), anomalies, where=anomalies > 0., facecolor='red', alpha=0.7)
ax.fill_between(np.linspace(1979, 2018, 480), anomalies, where=anomalies < 0., facecolor='blue', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'AMO index')
ax.set_xlabel(r'time')
ax.set_title(r'Anomalies of SST'+'\n'+
              'averaged over ('+str(lat_s)+','+str(lat_n)+')$^o$N'+'\n'+
              '('+str(360. - lon_w)+','+str(360. - lon_e)+')$^o$W - ORAS5')
fig.tight_layout()
fig.savefig('amo_anomalies_1979_2018_1m_oras5.png', dpi=300)
plt.show()

climatology_mean = amo_index.groupby("time.year").mean('time').mean('year')
anomalies = xr.apply_ufunc(
    lambda x, m: (x - m),
    amo_index.groupby("time.year").mean('time'),
    climatology_mean,
)

fig=plt.figure(1, figsize=(9,4))
ax=fig.add_subplot(111)
ax.axhline(0., color='k')
ax.bar(np.linspace(1979, 2018, 40), anomalies.where(anomalies>0.), width=1, color='red', edgecolor='k', alpha=0.7)
ax.bar(np.linspace(1979, 2018, 40), anomalies.where(anomalies<0.), width=1, color='blue', edgecolor='k', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'AMO index')
ax.set_xlabel(r'time')
ax.set_title(r'Yearly Anomalies of SST'+'\n'+
              'averaged over ('+str(lat_s)+','+str(lat_n)+')$^o$N'+'\n'+
              '('+str(360. - lon_w)+','+str(360. - lon_e)+')$^o$W - ORAS5')
fig.tight_layout()
fig.savefig('amo_anomalies_1979_2018_1y_oras5.png', dpi=300)
plt.show()


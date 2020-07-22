import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import sys

name_file='ESACCI_sst_1982-2018.nc'
name_var='analysed_sst'

ds = xr.open_dataset(name_file)
var=ds[name_var]

#bounds for calculation
lat_s = 60.
lat_n = 0.
lon_w = -75
lon_e = -7.5
weights=np.cos(ds.latitude*np.pi/180.).sel(latitude=slice(lat_s, lat_n))
amo_index = var.sel(latitude=slice(lat_s, lat_n), longitude=slice(lon_w, lon_e)).weighted(weights).mean(dim=['latitude', 'longitude'])


climatology_mean = amo_index.groupby("time.month").mean('time')
anomalies = xr.apply_ufunc(
    lambda x, m: (x - m),
    amo_index.groupby("time.month"),
    climatology_mean,
)

fig=plt.figure(1, figsize=(9,4))
ax=fig.add_subplot(111)
ax.plot(np.linspace(1982, 2018, 444), anomalies, lw=1, color='k')
ax.axhline(0., color='k')
ax.fill_between(np.linspace(1982, 2018, 444), anomalies, where=anomalies > 0., facecolor='red', alpha=0.7)
ax.fill_between(np.linspace(1982, 2018, 444), anomalies, where=anomalies < 0., facecolor='blue', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'AMO index')
ax.set_xlabel(r'time')
ax.set_xlim(1977., 2020.)
ax.set_title(r'Anomalies of SST'+'\n'+
              'averaged over ('+str(lat_s)+','+str(lat_n)+')$^o$N'+'\n'+
              '('+str(lon_w)+','+str(lon_e)+')$^o$W - ESACCI')
fig.tight_layout()
fig.savefig('amo_anomalies_1982_2018_1m_esacci.png', dpi=300)
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
ax.bar(np.linspace(1982, 2018, 37), anomalies.where(anomalies>0.), width=1, color='red', edgecolor='k', alpha=0.7)
ax.bar(np.linspace(1982, 2018, 37), anomalies.where(anomalies<0.), width=1, color='blue', edgecolor='k', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'AMO index')
ax.set_xlabel(r'time')
ax.set_xlim(1976.5, 2020.5)
ax.set_title(r'Yearly Anomalies of SST'+'\n'+
              'averaged over ('+str(lat_s)+','+str(lat_n)+')$^o$N'+'\n'+
              '('+str(lon_w)+','+str(lon_e)+')$^o$W - ESACCI')
fig.tight_layout()
fig.savefig('amo_anomalies_1982_2018_1y_esacci.png', dpi=300)
plt.show()


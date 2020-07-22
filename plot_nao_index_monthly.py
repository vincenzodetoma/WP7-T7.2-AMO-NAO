import pandas as pd
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import sys

filename = 'nao_station_monthly.txt'
data = pd.read_csv(filename, skiprows=1, sep='\s+')
data = data.replace(-999.0,np.NaN)
nao_series_data = data.stack()
nao_ts = np.array(nao_series_data.values)[1368:]
time=np.linspace(1979, 2020, len(nao_ts))

fig=plt.figure(1, figsize=(9,4))
ax=fig.add_subplot(111)
ax.plot(time, nao_ts, lw=1, color='k')
ax.axhline(0., color='k')
ax.fill_between(time, nao_ts, where=nao_ts > 0., facecolor='red', alpha=0.7)
ax.fill_between(time, nao_ts, where=nao_ts < 0., facecolor='blue', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'NAO index')
ax.set_xlabel(r'time')
ax.set_title(r' Hurrell Station-Based Monthly NAO Index')
fig.tight_layout()
fig.savefig('nao_index_1979_2020_Hurrell_1m.png', dpi=300)
plt.show()

time_idx=pd.date_range('1979-01-01', '2020-01-01', freq='M')
xr_nao = xr.DataArray(nao_ts[:-2], dims='time', coords={'time': ('time', time_idx)})
yearly_nao = xr_nao.groupby('time.year').mean(dim='time')

fig=plt.figure(1, figsize=(9,4))
ax=fig.add_subplot(111)
ax.axhline(0., color='k')
ax.bar(np.linspace(1979, 2019, 41), yearly_nao.where(yearly_nao>0.), width=1, color='red', edgecolor='k', alpha=0.7)
ax.bar(np.linspace(1979, 2019, 41), yearly_nao.where(yearly_nao<0.), width=1, color='blue', edgecolor='k', alpha=0.7)
ax.grid(True)
ax.set_ylabel(r'NAO index')
ax.set_xlabel(r'time')
ax.set_title(r' Hurrell Station-Based Annual NAO Index')
fig.tight_layout()
fig.savefig('NAO_Hurrell_1979_2019_1y.png', dpi=300)
plt.show()




import xarray as xr
import dask
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from ds_wrapper import my_ds_wrapper

# Splitting large chunks leads to long calculation times...
dask.config.set(**{'array.slicing.split_large_chunks': False})

def seas5_clim(lat_range = None, lon_range = None, day_range = None, year_range = None,
               lon_shift = False):
    '''Compute climatologies for u field in SEAS5 for NDJFM initialisation dates'''
    
    u_seas5_av = []
    # Split latitude chunks in two (latitude size = 256) as SH not required.
    seas5_chunks = {"latitude":128, "time":30, "longitude":-1}
    
    for init_date in ['0111', '0112', '0101', '0102', '0103']:
        fname = f'../data/raw/SEAS5/{init_date}/*nc'
        ds_all = xr.open_mfdataset(fname, combine = 'by_coords', parallel = True,
                                   chunks = seas5_chunks)
        u = ds_all['u']
        u_seas5 = my_ds_wrapper(u)
        u_seas5_av.append(u_seas5.compute_time_av(lats = lat_range, lons = lon_range,
                                                  days = day_range, years = year_range,
                                                  shift = lon_shift))
    return u_seas5_av

def era5_clim(lat_range = None, lon_range = None, day_range = None, year_range = None, 
              lon_shift = False):
    '''Compute climatology for u field in ERA5'''
    
    # Datasets are stored in monthly files, hence maximum time chunk is 31.
    # Split latitude chunks in two (latitude size = 721) as SH not required.
    era5_chunks = {"latitude":361, "time":-1, "longitude":-1}
    
    fname = f'../data/raw/ERA5/u_v/*nc'
    ds_all=xr.open_mfdataset(fname, combine='by_coords', parallel=True, chunks = era5_chunks)
    u = ds_all['u']
    u_era = my_ds_wrapper(u)
    u_era_av = u_era.compute_time_av(lats = lat_range, lons = lon_range, days = day_range,
                                     years = year_range, shift = lon_shift)
    
    return u_era_av

def clim_plot_panel(climate, early = False):
    '''Save a panel plot of climatological jet biases over NW Europe'''
    
    proj = ccrs.Orthographic(central_longitude = -20, central_latitude = 60)
    fig, axes = plt.subplots(figsize = (13,13),nrows = 2, ncols = 2, 
                             subplot_kw = {'projection': proj})
    clevs = np.linspace(-12, 12, 13)
    month = ['November 1', 'December 1', 'January 1', 'February 1']

    for i, ax in enumerate(axes.flat):
        ax.set_global()
        ax.coastlines()
        ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth=1,
                     color = 'gray', alpha = 0.6, linestyle = '--')
        cs = ax.contourf(climate[i].longitude, climate[i].latitude, climate[i].squeeze(),
                         levels = clevs, cmap = plt.cm.RdBu_r, transform = ccrs.PlateCarree())
        # Fill values between +/-2 m/s contours white
        ax.contourf(climate[i].longitude, climate[i].latitude, climate[i].squeeze(),
                    levels = [-2,2], colors = 'w', transform = ccrs.PlateCarree())
        ax.set_title(f'{month[i]} forecast initialisation date', fontsize = 15)

    fig.colorbar(cs, ax = axes.ravel().tolist(), orientation = 'horizontal',
                 fraction = .03, pad = 0.05)

    if early:
        plt.suptitle('u 500hPa March Climatology Bias (1982 - 1997, ERA5 - SEAS5)', 
                     fontsize = 20)
        plt.savefig('../images/pplot_early.png', bbox_inches = 'tight')
    else:
        plt.suptitle('u 500hPa March Climatology Bias (2002 - 2017, ERA5 - SEAS5)', 
                     fontsize = 20)
        plt.savefig('../images/pplot_late.png', bbox_inches = 'tight')
        
def clim_plot_single(climate, early = False):
    '''Save a single plot of climatological jet biases over NW Europe'''
    
    fig = plt.figure(figsize=(7,7))

    clevs = np.linspace(-12, 12, 13)
    proj = ccrs.Orthographic(central_longitude = -20, central_latitude = 60)
    ax = plt.axes(projection = proj)
    ax.set_global()
    ax.coastlines()
    ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1,
                 color = 'gray', alpha = 0.6, linestyle = '--')
    cs = ax.contourf(climate.longitude, climate.latitude, climate.squeeze(),
                     levels = clevs, cmap = plt.cm.RdBu_r, transform = ccrs.PlateCarree())
    ax.contourf(climate.longitude, climate.latitude, climate.squeeze(),
                levels = [-2,2], colors = 'w', transform = ccrs.PlateCarree())
    fig.colorbar(cs, orientation = 'horizontal', fraction = .05, pad = 0.05)    
    
    if early:
        plt.title('u 500hPa March Climatology Bias (1982 - 1997, ERA5 - SEAS5),' +
                  '\n' + 'March 1 initialisation', fontsize = 20)
        plt.savefig('../images/splot_early.png', bbox_inches = 'tight')
    else:
        plt.title('u 500hPa March Climatology Bias (2002 - 2017, ERA5 - SEAS5),' +
                  '\n' + 'March 1 initialisation', fontsize = 20)
        plt.savefig('../images/splot_late.png', bbox_inches = 'tight')
        
def h168_clim(lat_range = None, lon_range = None, day_range = None, year_range = None,
               lon_shift = False):
    '''Compute climatologies for u field in h168 experiment for November initialisation date'''
    
    u_h168_av = []
    # Split latitude chunks in two (latitude size = 256) as SH not required.
    h168_chunks = {"latitude":128, "time":30, "longitude":-1}
    
    fname = f'../data/raw/h168/*nc'
    ds_all = xr.open_mfdataset(fname, combine = 'by_coords', parallel = True, 
                               chunks = h168_chunks)
    u = ds_all['u']
    u_h168 = my_ds_wrapper(u)
    u_h168_av.append(u_h168.compute_time_av(lats = lat_range, lons = lon_range,
                                             days = day_range, years = year_range,
                                             shift = lon_shift))
    return u_h168_av

def main():
    
    # Compute early and late climatologies
    seas5_early = seas5_clim(lat_range = [25, 85], lon_range = [-80, 40], day_range = [60, 91], 
                             year_range = [1981, 1998], lon_shift = True)
    seas5_late = seas5_clim(lat_range = [25, 85], lon_range = [-80, 40], day_range = [60, 91], 
                            year_range = [2001, 2018], lon_shift = True)    
    era5_early = era5_clim(lat_range = [25, 85], lon_range = [-80, 40], day_range = [60, 91], 
                           year_range = [1981, 1998], lon_shift = True)
    era5_late = era5_clim(lat_range = [25, 85], lon_range = [-80, 40], day_range = [60, 91], 
                          year_range = [2001, 2018], lon_shift = True) 
    
    # Coarsen ERA5 to SEAS5 grid
    era5_early_coarse = era5_early.interp(longitude = seas5_early[0].longitude, 
                                          latitude = seas5_early[0].latitude)
    era5_late_coarse = era5_late.interp(longitude = seas5_late[0].longitude, 
                                        latitude = seas5_late[0].latitude)
    
    # Compute bias for all forecast initialisation dates
    bias_early = [(era5_early_coarse - i).compute() for i in seas5_early]
    bias_late = [(era5_late_coarse - i).compute() for i in seas5_late]

    # Save results for NDJF
    clim_plot_panel(bias_early, early = True)
    clim_plot_panel(bias_late, early = False)
    
    # Save results for March
    clim_plot_single(bias_early[4], early = True)
    clim_plot_single(bias_late[4], early = False)

if __name__ == "__main__":
    main()





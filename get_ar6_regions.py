import argparse
import xarray as xr
import regionmask
import numpy as np
from matplotlib import pyplot as plt

def get_args():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="./get_ar6_regions.py <variable> <file>")

    # Add positional arguments
    parser.add_argument("variable", type=str, help="The variable name as it appears in your dataset")
    parser.add_argument("file", type=str, help="The NetCDF file")

    # Parse the command line arguments
    args = parser.parse_args()

    # Check if the user provided enough arguments
    if len(vars(args)) < 2:
        parser.error("You must provide at least four arguments.")

    # Access and use the arguments
    var = args.variable
    file = args.file

    return var, file


def clean_dims(ds):
    """
    Clean dimensions, format in standardized format
    """
    # Drop bnds coords if exist
    try:
        ds = ds.drop(['lat_bnds', 'lon_bnds', 'time_bnds'])
    except:
        None
    
    # Ensure lon/lat have consistent labeling
    if "longitude" in ds.dims:
        ds = ds.rename({"longitude": "lon"})
    if "latitude" in ds.dims:
        ds = ds.rename({"latitude": "lat"})
    
    return ds


def lon2180(ds):
    # Allows for easier plotting and compatibility with certain packages
    lon = 'lon'
    ds['_longitude_adjusted'] = xr.where(
        ds[lon] > 180,
        ds[lon] - 360,
        ds[lon])

    # reassign the new coords to as the main lon coords
    # and sort DataArray using new coordinate values
    ds = (
        ds
        .swap_dims({lon: '_longitude_adjusted'})
        .sel(**{'_longitude_adjusted': sorted(ds._longitude_adjusted)})
        .drop(lon))

    ds = ds.rename({'_longitude_adjusted': lon})
    
    return ds


def regional_means(ds, var):
    
    # Get AR6 region masks and calculate regional weighted means
    mask_3D = regionmask.defined_regions.ar6.land.mask_3D(ds[var])
    weights = np.cos(np.deg2rad(ds.lat))

    ds_mean = xr.Dataset()
    ds_mean = ds_mean.assign({var: ds[var].weighted(mask_3D * weights).mean(('lat', 'lon'))})

    return ds_mean

def save_nc(ds_out, file):
    """
    Auto-generate netcdf name using file input
    Save to work directory
    """
    # Based output name off input file
    if "/" in file:
        outds_name = file.split("/")[-1].split(".nc")[0] + "_REGIONAL_MEANS_AR6.nc"
    else:
        outds_name = file.split(".nc")[0] + "_REGIONAL_MEANS_AR6.nc"
    
    # Save netcdf
    ds_out.to_netcdf(outds_name)
    print(f"Output saved as {outds_name}")


def main():
    """
    Run all with wrappings
    """

    # Arguments
    var, file = get_args()

    # Open dataset
    ds = xr.open_dataset(file)

    # Clean dimensions
    ds = clean_dims(ds)

    # Set lon to -180,180
    ds = lon2180(ds)

    # Get regional means
    ds_out = regional_means(ds, var)

    # Save netcdf
    save_nc(ds_out, file)

if __name__ == "__main__":
    main()

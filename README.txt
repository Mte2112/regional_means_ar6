To import: git clone https://github.com/Mte2112/regional_means_ar6

————Environment setup (only have to do this once)————
1. Load latest Python module
	1.A. module load python/GEOSpyD/Min23.3.1-0_py3.10
2. Create conda environment using environment file 
	2.A. conda env create -f /discover/nobackup/melling/4larissa/regional_means/environment.yml

————Running the script————
Prep
1. Load latest Python module
        1.A. module load python/GEOSpyD/Min23.3.1-0_py3.10
2. Activate your conda environment
        2.A. conda activate extremes

Running script
Run the script from one of your directories, where you have write permission. This is because the output data file is written to the work directory
Format ./get_ar6_regions.py <variable> <file>
Example:       python ./get_ar6_regions.py txxETCCDI sample_data/txxETCCDI_mon_GISS-E2-1-G_historical_r1i1p1f2_185001-194912.nc
* You may remind yourself of how to run the script by running the script with the help argument i.e. python ./get_ar6_regions.py -h

Command line inputs:
- Data file: This file should contain dimensions lon/lat/time and your variable
- Variable: The relevant variable name in the dataset
- Type: Either “p” ( for precipitation) or “t” (for temperature) This is to determine the colormap being used for the plot


Outputs
- A png file of the regional averages, broken up by SREX regions, for the entire time period in the file
- A NetCDF file consistent with the data in the plot


Sample output ncdump 
dimensions:
	time = 1200 ;
	region = 46 ;
variables:
	double time(time) ;
		time:_FillValue = NaN ;
		time:units = "days since 1850-01-01" ;
		time:calendar = "365_day" ;
	int64 region(region) ;
	string abbrevs(region) ;
	string names(region) ;
	double txxETCCDI(time, region) ;
		txxETCCDI:_FillValue = NaN ;
		txxETCCDI:coordinates = "abbrevs names" ;
}


Relevant links
https://www.ipcc.ch/report/srex/
https://regionmask.readthedocs.io/en/stable/defined_scientific.html

contact: maxwell.t.elling@nasa.gov

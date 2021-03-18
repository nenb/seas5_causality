#!/usr/bin/env python3

import cdsapi
import calendar

c = cdsapi.Client()
for year in range(1979, 2021):
    for month in [11, 12, 1, 2, 3]:
        print(f"Retrieving ERA5, year = {year}, month = {month}")

        month_len = calendar.monthrange(year, month)[1]
        start_date = f"{year}-{month:02}-01"
        end_date = f"{year}-{month:02}-{month_len}"
        dates = f"{start_date}/{end_date}"

        c.retrieve(
            "reanalysis-era5-pressure-levels",
            {
                "variable": ["u_component_of_wind"],
                "pressure_level": "500",
                "product_type": "reanalysis",
                "date": dates,
                "time": "00:00",
                "format": "netcdf",
            },
            f"u_ERA5_{start_date}_500_0000.nc",
        )

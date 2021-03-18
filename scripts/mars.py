#!/usr/bin/env python3

from ecmwfapi import ECMWFService

server = ECMWFService("mars")

for month in [11, 12, 1, 2, 3]:
    for year in range(1981, 2020):
        print(f"Retrieving SEAS5, year = {year}, init_date = {month}")

        start_date = f"{year}-{month:02}-01"

        server.execute(
            {
                "class": "od",
                "levelist": "500",
                "step": "0/to/3648/by/24",
                "number": "0",
                "levtype": "pl",
                "expver": "1",
                "method": "1",
                "origin": "ecmf",
                "date": start_date,
                "time": "00:00:00",
                "type": "fc",
                "param": "131",
                "stream": "mmsf",
                "system": "5",
                "grid": "128",
                "format": "netcdf",
            },
            f"u_500_01_{start_date}_S5Hindcasts_24H_0000.nc",
        )

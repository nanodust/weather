# weather
Consumes Dark Sky API for Lat/Long/Date and formats CSV for easy processing with R. 

#usage

final CLI something like:

getWeatherDataWithin -l NWLatLong -r SELatLong -s StartDate - e EndDate

meanwhile:

set up localhost mongo (or connect elsewhere per config.cfg)

python getData.py 

will get data for whatever interval in the method

then 

python writeData.py 

will write the data into CSV
# Suntime
Calculate sunrises and sunsets. In an arguably messy way. Also doesn't support midnight sun (days without sunset) or polar night (days without sunrise).

Adapted from NOAA's solar calculations spreadsheets, found here:
* https://www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html

## Use
Use it as a module. Suntime.py consists of three classes, where `Sun` is the main one. 

```python3
# date is a datetime object
# location is a Location object
# timezone is a TimeZone object, defaults to UTC
Sun (date, location, timezone)

# N, E are latitude and longitude, positive towards north and east
Location (name, N, E)

# hours, minutes, seconds ahead of UTC
# minutes, seconds defaults to 0
Timezone (name, hours, minutes, seconds)
```

The `Sun` object will have the properties `sunrise`, `sunset`, and `noon`, which all will be `datetime` objects.

## Example

```python3
import datetime
import suntime

# Datetime of today
today = datetime.datetime.now()

# Location
rome = suntime.Location("Rome", 41.89, 12.48)

# Time zone
CET = suntime.TimeZone("CET", 1)

sun = suntime.Sun(today, rome, CET)

print(sun.sunrise)
print(sun.noon)
print(sun.sunset)

print("Day lenght:", sun.sunset - sun.sunrise)
```

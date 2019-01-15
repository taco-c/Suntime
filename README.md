# Suntime
Calculate sunrises and sunsets. In an arguably messy way. Also doesn't support midnight sun (days without sunset) or polar night (days without sunrise).

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

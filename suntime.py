from math import sin, cos, tan, radians, degrees, asin, acos, floor, modf
import datetime

class TimeZone():
    def __init__(self, name, hours, minutes=0, seconds=0):
        self.name = name
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.timedelta = datetime.timedelta(
                hours=self.hours,
                minutes=self.minutes,
                seconds=self.minutes)

    def __add__(self, other):
        h = self.hours + other.hours
        m = self.minutes + other.minutes
        s = self.seconds + other.seconds
        return TimeZone(
                "{}+{}".format(self.name, other.name),
                h,
                minutes=m,
                seconds=s)

    def __sub__(self, other):
        h = self.hours - other.hours
        m = self.minutes - other.minutes
        s = self.seconds - other.seconds
        return TimeZone(
                "{}-{}".format(self.name, other.name),
                h,
                minutes=m,
                seconds=s)

    def __eq__(self, other):
        return self.timedelta == other.timedelta

    def __lt__(self, other):
        return self.timedelta < other.timedelta

    def __le__(self, other):
        return self.timedelta <= other.timedelta

    def __gt__(self, other):
        return self.timedelta > other.timedelta

    def __ge__(self, other):
        return self.timedelta >= other.timedelta

    def __repr__(self):
        return "TimeZone(name={}, hours={}, minutes={}, seconds={})".format(
                self.name,
                self.hours,
                self.minutes,
                self.seconds)

class Location:
    def __init__(self, name, N, E):
        self.name = name
        self.N = N
        self.E = E

    def __repr__(self):
        return "Location(name={}, N={}, E={})".format(self.name, self.N, self.E)

class Sun:
    def __init__(self, date, location, timezone=TimeZone("UTC", 0)):
        self.date = date
        self.location = location
        self.timezone = timezone
        self.sunrise, self.sunset, self.noon = self._calculate_sun()
        self.sunrise += self.timezone.timedelta
        self.sunset += self.timezone.timedelta
        self.noon += self.timezone.timedelta

    def __repr__(self):
            return "Sun()".format()

    def _calculate_sun(self):
        # The confusing part.
        # Put these in sepparate functions?
        
        # Julian day
        Jday = self._jday(self.date)
        
        # Julian century
        Jcent = (Jday - 2451545) / 36525
        
        # Geometric Mean Long Sun (deg)
        I2 = (280.46646 + Jcent*(36000.76983 + Jcent*0.0003032)) % 360
        
        # Geom Mean Anom Sun (deg)
        J2 = 357.52911 + Jcent*(35999.05029 - 0.0001537*Jcent)
        
        # Eccent earth orbit
        K2 = 0.016708634 - Jcent*(0.000042037 + 0.0000001267*Jcent)
        
        # Sun Eq of Ctr
        L2 = sin(radians(J2)) * (1.914602 - Jcent*(0.004817 + 0.000014*Jcent)) \
                + sin(radians(2*J2)) * (0.019993 - 0.000101*Jcent) \
                + sin(radians(3*J2)) * 0.000289
        
        # Sun True Long (deg)
        M2 = I2 + L2
        
        # Sun app long (deg)
        P2 = M2 - 0.00569 - 0.00478*sin(radians(125.04 - 1934.136*Jcent))
        
        # Mean oblique ecliptic (deg)
        Q2 = 23 + (26 + ((21.448 - Jcent*(46.815 + Jcent \
                * (0.00059 - Jcent*0.001813))))/60) / 60
        
        # Oblique Corr (deg)
        R2 = Q2 + 0.00256*cos(radians(125.04 - 1934.136*Jcent))
        
        # Sun declination
        T2 = degrees(asin(sin(radians(R2)) * sin(radians(P2))))
        
        # Var y
        y = tan(radians(R2/2)) * tan(radians(R2/2))
        
        # Equation of time
        V2 = 4*degrees(y*sin(2*radians(I2)) - 2*K2*sin(radians(J2)) \
                + 4*K2*y*sin(radians(J2))*cos(2*radians(I2)) \
                - 0.5*y*y*sin(4*radians(I2)) - 1.25*K2*K2*sin(2*radians(J2)))
        
        # Solar noon
        X2 = (720 - 4*self.location.E - V2)/1440
        
        # HA Sunrise (deg)
        W2 = degrees(acos(cos(radians(90.833)) \
                /(cos(radians(self.location.N))*cos(radians(T2))) \
                - tan(radians(self.location.N))*tan(radians(T2))))
        
        sunrise = ((X2*1440-W2*4)/1440) + Jday
        sunset = ((X2*1440+W2*4)/1440) + Jday
        noon = X2 + Jday
        
        return (self._time(sunrise), self._time(sunset), self._time(noon))

    def _date(self, J): # From julian day to gregorian date
        f = J + 1401 + (((4 * J + 274277) // 146097) * 3) // 4 - 38
        e = 4 * f + 3
        h = 5 * ((e % 1461) // 4) + 2
        D = (h % 153) // 5 + 1
        M = ((h // 153 + 2) % 12) + 1
        Y = (e // 1461) - 4716 + (12 + 2 - M) // 12
        try:
            return datetime.datetime(int(Y), int(M), int(D))
        except ValueError:
            return datetime.datetime(int(Y), int(M), int(D)-1) \
                    + datetime.timedelta(days=1)

    def _time(self, J):
        date = self._date(J)
        h = modf(J-0.5)[0] * 24
        m = modf(h)[0] * 60
        s = modf(m)[0] * 60
        return datetime.datetime(
                date.year,
                date.month,
                date.day,
                hour=floor(h),
                minute=floor(m),
                second=floor(s))

    def _jday(self, date): # Julian date
        Y, M, D = date.year, date.month, date.day
        if M <= 2:
            Y -= 1
            M += 12
        A = floor(Y/100)
        B = 2 - A + floor(A/4)
        JD = floor(365.25*(Y + 4716)) + floor(30.6001*(M+1)) + D + B - 1524.5
        return JD

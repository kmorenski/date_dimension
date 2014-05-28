#!/usr/bin/env python
#
# Copyright 2014 Kevin M. Morenski <kmm2254@columbia.edu>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import calendar
import calendar_util
from datetime import date, timedelta

# Indices for the time tuple
YEAR = 0
MONTH = 1
DAY = 2
WEEKDAY = 6

# Months
JAN =  1
FEB =  2
MAR =  3
APR =  4
MAY =  5
JUN =  6
JUL =  7
AUG =  8
SEP =  9
OCT = 10
NOV = 11
DEC = 12

# Weekdays
MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

# Hebrew Months
NISAN   =  1
IYYAR   =  2
SIVAN   =  3
TAMMUZ  =  4
AV      =  5
ELUL	=  6
TISHRI	=  7
HESHVAN	=  8
KISLEV	=  9
TEVETH  = 10
SHEVAT	= 11
ADAR	= 12
VEADAR	= 13

HEBREW_YEAR_OFFSET = 3760

# U.S. presidential elections occur quadrennially, beginning with year 1792
IS_PRESIDENTIAL_ELECTION_YEAR = lambda yyyy: yyyy > 1791 and yyyy % 4 == 0


class Holidays(object):
    def __init__(self, year=None):
        if year:
            self.year = year

    def get_nth_weekday_of_month(self, n, weekday, month, year=None):
        if not year:
            year = self.year
        (first_weekday, days_in_month) = calendar.monthrange(year, month)
        delta = abs(weekday - first_weekday)
        day_of_month = delta + 1 if weekday >= first_weekday else 8 - delta

        for i in range(1, n):
            day_of_month += 7
            if day_of_month > days_in_month:
                raise IndexError

        return day_of_month

    def get_first_weekday_of_month(self, weekday, month, year=None):
        return self.get_nth_weekday_of_month(1, weekday, month, year)

    def get_last_weekday_of_month(self, weekday, month, year=None):
        if not year:
            year = self.year
        (first_weekday, days_in_month) = calendar.monthrange(year, month)
        last_day = first_weekday + (days_in_month % 7) - 1

        return days_in_month - abs(last_day - weekday)

    def hebrew_to_gregorian(self, year, hebrew_month, hebrew_day,
                             is_gregorian_year=True):
        if not year:
            year = self.year

        if is_gregorian_year:
            for y in (year + HEBREW_YEAR_OFFSET, year + HEBREW_YEAR_OFFSET + 1):
                jd = calendar_util.hebrew_to_jd(y, hebrew_month, hebrew_day)
                gd = calendar_util.jd_to_gregorian(jd)
                if gd[YEAR] == year:
                    break
                else:
                    gd = None
        else:
            jd = calendar_util.hebrew_to_jd(year, hebrew_month, hebrew_day)
            gd = calendar_util.jd_to_gregorian(jd)

        if not gd:
            raise RangeError, "Couldn't determine the Gregorian year"
        else:
            return gd

	######################################################################
	# HOLIDAYS

    # 1 Jan: New Year's Day
    def holiday_new_years_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, JAN, 1), "New Year's Day")

    # 6 Jan: Epiphany
    def holiday_epiphany(self, year=None):
        if not year:
            year = self.year
        return (date(year, JAN, 6), "Epiphany")

    # 3rd Mon in Jan: Birthday of Martin Luther King, Jr.
    def holiday_birthday_of_martin_luther_king_jr(self, year=None):
        if not year:
            year = self.year
        return (date(year, JAN, self.get_nth_weekday_of_month(3, MON, JAN)),
            "Birthday of Martin Luther King, Jr.")

    # 1st Jan 20 following a Presidential election: Inauguration Day
    def holiday_inauguration_day(self, year=None):
        if not year:
            year = self.year

        if not IS_PRESIDENTIAL_ELECTION_YEAR(year - 1):
            return (None, "Inauguration Day")

        d = date(year, JAN, 20)
        if d.weekday() == SUN:
            d = date(year, JAN, 21)

        return (d, "Inauguration Day")

    # 2 Feb: Groundhog Day
    def holiday_groundhog_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, FEB, 2), "Groundhog Day")

    # 14 Feb: Valentine's Day
    def holiday_valentines_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, FEB, 14), "Valentine's Day")

    # 3rd Mon in Feb: Washington's Birthday/Presidents' Day
    def holiday_presidents_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, FEB, self.get_nth_weekday_of_month(3, MON, FEB)),
            "Washington's Birthday/Presidents' Day")

    # Feb/Mar: Mardi Gras
    def holiday_mardi_gras(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_easter(year)[0] - timedelta(days=47),
                "Mardi Gras")

    # Feb/Mar: Ash Wednesday
    def holiday_ash_wednesday(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_easter(year)[0] - timedelta(days=46),
                "Ash Wednesday")

    # 17 Mar: Saint Patrick's Day
    def holiday_saint_patricks_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, MAR, 17), "Saint Patrick's Day")

    # 1 Apr: April Fools' Day
    def holiday_april_fools_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, APR, 1), "April Fools' Day")

    # Sun before Easter: Palm Sunday
    def holiday_palm_sunday(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_easter(year)[0] - timedelta(days=7),
                "Palm Sunday")

    # Fri before Easter: Good Friday
    def holiday_good_friday(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_easter(year)[0] - timedelta(days=2),
                "Good Friday")

    # Sun following the Paschal Full Moon: Easter
    def holiday_easter(self, year=None):
        if not year:
            year = self.year

        a = year % 19
        b, c = divmod(year, 100)
        d, e = divmod(b, 4)
        f = (b + 8) / 25
        g = (b - f + 1) / 3
        h = (19 * a + b - d - g + 15) % 30
        i, k = divmod(c, 4)
        L = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * L) / 451
        month, day = divmod(h + L - 7 * m + 114, 31)
        day += 1

        return (date(year, month, day), "Easter")

    # 22 Apr: Earth Day
    def holiday_earth_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, APR, 22), "Earth Day")

    # Last Fri in Apr: Arbor Day
    def holiday_arbor_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, APR,
                     self.get_last_weekday_of_month(FRI, APR, year)),
                "Arbor Day")

    # 1 May: May Day
    def holiday_may_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, MAY, 1), "May Day")

    # 5 May: Cinco de Mayo
    def holiday_cinco_de_mayo(self, year=None):
        if not year:
            year = self.year
        return (date(year, MAY, 5), "Cinco de Mayo")

    # 2nd Sun in May: Mother's Day
    def holiday_mothers_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, MAY,
                     self.get_nth_weekday_of_month(2, SUN, MAY, year)),
                "Mother's Day")

    # Last Mon in May: Memorial Day
    def holiday_memorial_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, MAY,
                     self.get_last_weekday_of_month(MON, MAY, year)),
                "Memorial Day")

    # 14 Jun: Flag Day
    def holiday_flag_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, JUN, 14), "Flag Day")

    # 3rd Sun in Jun: Father's Day
    def holiday_fathers_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, JUN,
                     self.get_nth_weekday_of_month(3, SUN, JUN, year)),
                "Father's Day")

    # 4 Jul: Independence Day
    def holiday_independence_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, JUL, 4), "Independence Day")

    # 26 Aug: Women's Equality Day
    def holiday_womens_equality_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, AUG, 26), "Women's Equality Day")

    # 1st Mon in Sep: Labor Day
    def holiday_labor_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, SEP,
                     self.get_first_weekday_of_month(MON, SEP, year)),
                "Labor Day")

    # 11 Sep: Patriot Day
    def holiday_patriot_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, SEP, 11), "Patriot Day")

    # 17 Sep: Constitution/Citizenship Day
    def holiday_constitution_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, SEP, 17), "Constitution/Citizenship Day")

    # 2nd Mon in Oct: Columbus Day
    def holiday_columbus_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, OCT,
                     self.get_nth_weekday_of_month(2, MON, OCT, year)),
                "Columbus Day")

    # 31 Oct: Halloween
    def holiday_halloween(self, year=None):
        if not year:
            year = self.year
        return (date(year, OCT, 31), "Halloween")

    # 1st Tue after 1st Mon in Nov: Election Day
    def holiday_election_day(self, year=None):
        if not year:
            year = self.year
        if not IS_PRESIDENTIAL_ELECTION_YEAR(year):
            return (None, "Election Day")
        return (date(year, NOV,
                     self.get_first_weekday_of_month(MON, NOV, year)) +
                timedelta(days=1), "Election Day")

    # 11 Nov: Veterans Day
    def holiday_veterans_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, NOV, 11), "Veterans Day")

    # 4th Thu in Nov: Thanksgiving Day
    def holiday_thanksgiving_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, NOV,
                     self.get_nth_weekday_of_month(4, THU, NOV, year)),
                "Thanksgiving Day")

    # 1st Fri after 4th Thu in Nov: Black Friday
    def holiday_black_friday(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_thanksgiving_day(year)[0] + timedelta(days=1),
                "Black Friday")

    # 7 Dec: Pearl Harbor Remembrance Day
    def holiday_pearl_harbor_remembrance_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 7), "Pearl Harbor Remembrance Day")

    # 8 Dec: Immaculate Conception of the Virgin Mary
    def holiday_immaculate_conception_of_the_virgin_mary(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 8), "Immaculate Conception of the Virgin Mary")

    # 24 Dec: Christmas Eve
    def holiday_christmas_eve(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 24), "Christmas Eve")

    # 25 Dec: Christmas Day
    def holiday_christmas_day(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 25), "Christmas Day")

    # 26 Dec - 1 Jan: Kwanzaa
    def holiday_kwanzaa(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 26), "Kwanzaa")
        #([map(lambda x: date(year, DEC, x), range(26:31))], "Kwanzaa")

    # 31 Dec: New Year's Eve
    def holiday_new_years_eve(self, year=None):
        if not year:
            year = self.year
        return (date(year, DEC, 31), "New Year's Eve")

    def holiday_hanukkah(self, year=None):
        # need an algorithm to comute gregorian first day...
        if not year:
            year = self.year
        gd = self.hebrew_to_gregorian(year, KISLEV, 25)
        return (date(year, gd[MONTH], gd[DAY]), "Hanukkah")

    def holiday_hanukkah_eve(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_hanukkah(year)[0] - timedelta(days=1),
                "Hanukkah Eve")

    def holiday_rosh_hashanah(self, year=None):
        if not year:
            year = self.year
        gd = self.hebrew_to_gregorian(year, TISHRI, 1)
        return (date(year, gd[MONTH], gd[DAY]), "Rosh Hashanah")

    def holiday_rosh_hashanah_eve(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_rosh_hashanah(year)[0] - timedelta(days=1),
                "Rosh Hashanah Eve")

    def holiday_yom_kippur(self, year=None):
        if not year:
            year = self.year
        gd = self.hebrew_to_gregorian(year, TISHRI, 10)
        return (date(year, gd[MONTH], gd[DAY]), "Yom Kippur")

    def holiday_yom_kippur_eve(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_rosh_hashanah(year)[0] +
                timedelta(days=8), "Yom Kippur Eve")

    def holiday_passover(self, year=None):
        if not year:
            year = self.year
        gd = self.hebrew_to_gregorian(year, NISAN, 15)
        return (date(year, gd[MONTH], gd[DAY]), "Passover")

    def holiday_passover_eve(self, year=None):
        if not year:
            year = self.year
        return (self.holiday_passover(year)[0] - timedelta(days=1),
                "Passover Eve")

    def is_holiday(self, d=None):
        if d:
            for holiday_fn in [k for k in dir(self)
                               if k.startswith('holiday_')]:
                holiday_date, holiday_name = getattr(self, holiday_fn)()
                if holiday_date == d:
                    return True, holiday_name
        return False, "No Holiday"

    def get_holiday_name(self, d=None):
        return self.is_holiday(d)[1]

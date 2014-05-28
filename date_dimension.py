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

import sys
import time
from datetime import date, timedelta
import calendar
from calendars.holidays import Holidays


MONTH_NAMES = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November',
               'December']
MONTH_ABBREVIATIONS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
             'Saturday', 'Sunday']
DAY_ABBREVIATIONS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class SqlQuery(object):
    def __init__(self):
        self.sql = list()

    def to_str(self):
        return '\n'.join(self.sql)

    def insert(self, **kwargs):
        return


class DateDimension(object):

    ## Date Key Functions ##

    def make_date_key(self, d):
        return d.year*10000 + d.month*100 + d.day

    def make_year_month_key(self, d):
        return d.year*100 + d.month

    def make_year_key(self, d):
        return d.year

    ## Year Functions ##

    def get_week_number_in_year(self, d):
        y = d.year
        w = 0
        while d.year >= y:
            w += 1
            d -= timedelta(days=7)
        return w

    def get_days_remaining_in_year(self, d):
        return (date(d.year, 12, 31) - d).days

    ## Half Year Functions ##

    def get_half_from_date(self, d):
        return 1 if 1 <= self.get_quarter_from_date(d) <= 2 else 2

    def get_half_months(self, h, d):
        return [h*6-m for m in range(5,-1,-1)]

    def get_month_number_in_half(self, h, d):
        return self.get_half_months(h,d).index(d.month)

    def get_week_number_in_half(self, h, d):
        y = d.year
        m = 1 if h == 1 else 7
        w = 0
        while d.month >= m and d.year == y:
            w += 1
            d -= timedelta(days=7)
        return w
        """
        week = 0
        half_first_month = 1 if h == 1 else 7
        start = date(d.year, half_first_month, self.get_first_weekday_of_month(THU, half_first_month)) - timedelta(days=3)
        while start <= d:
            week += 1
            start += timedelta(days=7)
        if start.month > d.month:
            week -= 1 if start - d >= timedelta(days=4) else 0

        return week
        """

    def get_day_number_in_half(self, h, d):
        half_months = self.get_half_months(h,d)
        half_month_days = [calendar.monthrange(d.year, n)[1] for n in half_months]
        return d.day + sum([half_month_days[i] for i in range(0, half_months.index(d.month))])

    def get_first_day_in_half(self, h, d):
        return d - timedelta(self.get_day_number_in_half(h,d)-1)

    def get_last_day_in_half(self, h, d):
        return date(d.year, h*6, calendar.monthrange(d.year, h*6)[1])

    ## Quarter Functions ##

    def get_quarter_from_date(self, d):
        return [i for j in map(lambda x: [x]*3, range(1,5)) for i in j][d.month-1]

    def get_quarter_months(self, q, d):
        return [q*3-m for m in range(2,-1,-1)]

    def get_month_number_in_quarter(self, q, d):
        return self.get_quarter_months(q,d).index(d.month)

    def get_week_number_in_quarter(self, q, d):
        y = d.year
        m = q*3-2
        w = 0
        while d.month >= m and d.year == y:
            w += 1
            d -= timedelta(days=7)
        return w
        """
        week = 0
        qtr_first_month = q*3-2
        start = date(d.year, qtr_first_month, self.get_first_weekday_of_month(THU, qtr_first_month)) - timedelta(days=3)
        while start <= d:
            week += 1
            start += timedelta(days=7)
        if start.month > d.month:
            week -= 1 if start - d >= timedelta(days=4) else 0

        return week
        """

    def get_day_number_in_quarter(self, q, d):
        qtr_months = self.get_quarter_months(q,d)
        qtr_month_days = [calendar.monthrange(d.year, n)[1] for n in qtr_months]
        return d.day + sum([qtr_month_days[i] for i in range(0, qtr_months.index(d.month))])

    def get_first_day_in_quarter(self, q, d):
        return d - timedelta(self.get_day_number_in_quarter(q,d)-1)

    def get_last_day_in_quarter(self, q, d):
        return date(d.year, q*3, calendar.monthrange(d.year, q*3)[1])

    ## Month Functions ##

    def get_week_number_in_month(self, d):
        m = d.month
        w = 0
        while d.month == m:
            w += 1
            d -= timedelta(days=7)
        return w
        """
        week = 0
        start = date(d.year, d.month, self.get_first_weekday_of_month(THU, d.month)) - timedelta(days=3)
        while start <= d:
            week += 1
            start += timedelta(days=7)
        if start.month > d.month:
            week -= 1 if start - d >= timedelta(days=4) else 0

        return week
        """

    def get_nth_weekday_of_month(self, n, weekday, month, d):
        (first_weekday, days_in_month) = calendar.monthrange(d.year, month)
        delta = abs(weekday - first_weekday)
        day_of_month = delta + 1 if weekday >= first_weekday else 8 - delta

        for i in range(1, n):
            day_of_month += 7
            if day_of_month > days_in_month:
                raise IndexError

        return day_of_month

    def get_first_weekday_of_month(self, weekday, month, d):
        return self.get_nth_weekday_of_month(1, weekday, month, d.year)

    def get_last_weekday_of_month(self, weekday, month, d):
        (first_weekday, days_in_month) = calendar.monthrange(d.year, month)
        last_day = first_weekday + (days_in_month % 7) - 1

        return days_in_month - abs(last_day - weekday)

    ## Misc. Functions ##

    def get_season(self, d):
        if d < date(d.year, 3, 20) or d >= date(d.year, 12, 21):
            return "Winter"
        elif d < date(d.year, 6, 20):
            return "Spring"
        elif d < date(d.year, 9, 22):
            return "Summer"
        elif d < date(d.year, 12, 21):
            return "Fall"

    ## Fiscal Year Conversions ##

    def convert_calendar_date_to_fiscal_date(self, d, o):
        if not o:
            o = self.fiscal_offset
        return date(d.year + o.year, d.month + o.month, d.day + o.day)

    def convert_fiscal_date_to_calendar_date(self, fd, d):
        delta = self.fy_begin - fd
        return
        #dy = self.fy_begin.year - fd.year
        #dm = self.fy_begin.month - fd.month
        #dd = self.fy_begin.day - fd.day
        #return date(d.year + dy, d.month + dm, d.day + dd)
        #return d + (self.fy_begin - fd)

    ## Initialization ##

    # d is the current calendar date
    # fd is the equivalent fiscal calendar date -- it's assumd a priori that
    # the conversion has already taken place. All fiscal begin/end dates and
    # date keys, however, correspond to the calendar date.
    def initialize_table(self):
        d = self.date
        #fd = self.fiscal_date
        h = Holidays(d.year)

        self.columns['date_key'] = self.make_date_key(d)
        self.columns['full_date'] = d.isoformat()


        self.columns['year_key'] = self.make_year_key(d)
        self.columns['year_month_key'] = self.make_year_month_key(d)
        self.columns['iso8601_year'] = d.isocalendar()[0]
        self.columns['is_leap_year'] = ('yes' if calendar.isleap(d.year)
                                        else 'no')


        self.columns['half_number_in_year'] = self.get_half_from_date(d)
        self.columns['half_duration_in_days'] = (
            self.get_last_day_in_half(self.columns['half_number_in_year'],
                                      d).toordinal() -
            self.get_first_day_in_half(self.columns['half_number_in_year'],
                                       d).toordinal() + 1)
        self.columns['half_label'] = 'S%d%d' % (
            self.columns['half_number_in_year'],
            d.year)
        self.columns['half_begin_date'] = self.get_first_day_in_half(
            self.columns['half_number_in_year'], d).isoformat()
        self.columns['half_begin_date_key'] = self.make_date_key(
            self.get_first_day_in_half(self.columns['half_number_in_year'], d))
        self.columns['half_end_date'] = self.get_last_day_in_half(
            self.columns['half_number_in_year'], d).isoformat()
        self.columns['half_end_date_key'] = self.make_date_key(
            self.get_last_day_in_half(self.columns['half_number_in_year'], d))


        self.columns['quarter_number_in_year'] = self.get_quarter_from_date(d)
        self.columns['quarter_number_in_half'] = (
            self.columns['quarter_number_in_year'] - 1) % 2 + 1
        self.columns['quarter_duration_in_days'] = (
            self.get_last_day_in_quarter(
                self.columns['quarter_number_in_year'], d).toordinal() -
            self.get_first_day_in_quarter(self.columns['quarter_number_in_year'],
                                          d).toordinal() + 1)
        self.columns['quarter_label'] = 'Q%d%d' % (
            self.columns['quarter_number_in_year'],
            d.year)
        self.columns['quarter_begin_date'] = self.get_first_day_in_quarter(
            self.columns['quarter_number_in_year'], d).isoformat()
        self.columns['quarter_begin_date_key'] = self.make_date_key(
            self.get_first_day_in_quarter(
                self.columns['quarter_number_in_year'], d))
        self.columns['quarter_end_date'] = self.get_last_day_in_quarter(
            self.columns['quarter_number_in_year'], d).isoformat()
        self.columns['quarter_end_date_key'] = self.make_date_key(
            self.get_last_day_in_quarter(
                self.columns['quarter_number_in_year'], d))


        self.columns['month_number_in_year'] = d.month
        self.columns['month_number_in_half'] = (
            self.columns['month_number_in_year'] - 1) % 6 + 1
        self.columns['month_number_in_quarter'] = (
            self.columns['month_number_in_half'] - 1) % 3 + 1
        self.columns['month_duration_in_days'] = calendar.monthrange(
            d.year, d.month)[1]
        self.columns['month_name'] = MONTH_NAMES[d.month-1]
        self.columns['month_abbreviation'] = MONTH_ABBREVIATIONS[d.month-1]
        self.columns['month_begin_date'] = date(d.year, d.month, 1).isoformat()
        self.columns['month_begin_date_key'] = self.make_date_key(
            date(d.year, d.month, 1))
        self.columns['month_end_date'] = date(
            d.year, d.month, self.columns['month_duration_in_days']).isoformat()
        self.columns['month_end_date_key'] = self.make_date_key(
            date(d.year, d.month, self.columns['month_duration_in_days']))


        self.columns['week_number_in_year'] = self.get_week_number_in_year(d)
        self.columns['iso8601_week_number_in_year'] = d.isocalendar()[1]
        self.columns['week_number_in_half'] = self.get_week_number_in_half(
            self.columns['half_number_in_year'], d)
        self.columns['week_number_in_quarter'] = (
            self.get_week_number_in_quarter(
                self.columns['quarter_number_in_year'], d))
        self.columns['week_number_in_month'] = self.get_week_number_in_month(d)
        self.columns['week_label'] = (
            'W%02d' % self.columns['week_number_in_year'])
        self.columns['week_begin_date'] = (d - timedelta(
            days=d.isoweekday())).isoformat()
        self.columns['week_begin_date_key'] = self.make_date_key(
            d - timedelta(days=d.isoweekday()))
        self.columns['week_end_date'] = (d + timedelta(
            days=6-(d.isoweekday()-1))).isoformat()
        self.columns['week_end_date_key'] = self.make_date_key(
            d + timedelta(days=6-(d.isoweekday()-1)))


        # Calendar weeks start on Sunday
        self.columns['day_number_in_year'] = (
            d.toordinal() - date(d.year, 1, 1).toordinal() + 1)
        self.columns['day_number_in_half'] = self.get_day_number_in_half(
            self.columns['half_number_in_year'], d)
        self.columns['day_number_in_quarter'] = self.get_day_number_in_quarter(
            self.columns['quarter_number_in_year'], d)
        self.columns['day_number_in_month'] = d.day
        self.columns['day_number_in_week'] = d.isoweekday()+1
        self.columns['iso8601_day_number_in_week'] = d.isocalendar()[2]
        self.columns['day_name'] = DAY_NAMES[d.isoweekday()-1]
        self.columns['day_abbreviation'] = DAY_ABBREVIATIONS[d.isoweekday()-1]
        self.columns['is_weekday'] = ('yes'
                                      if self.columns['day_number_in_week'] < 6
                                      else 'no')
        self.columns['is_weekend'] = ('yes'
                                      if 4 < self.columns['day_number_in_week']
                                      else 'no')
        self.columns['is_workday'] = 'no'
        self.columns['is_last_day_in_workweek'] = (
            'yes'
            if self.columns['day_number_in_week'] == 5
            else 'no')
        self.columns['is_last_day_in_week'] = (
            'yes'
            if self.columns['day_number_in_week'] == 7
            else 'no')
        self.columns['is_last_day_in_month'] = (
            'yes'
            if d.day == calendar.monthrange(d.year, d.month)[1]
            else 'no')
        self.columns['is_last_day_in_quarter'] = (
            'yes'
            if d == self.get_last_day_in_quarter(self.columns['quarter_number_in_year'], d)
            else 'no')
        self.columns['is_last_day_in_half'] = (
            'yes'
            if d == self.get_last_day_in_half(self.columns['half_number_in_year'], d)
            else 'no')
        self.columns['is_last_day_in_year'] = ('yes'
                                               if d.month == 12 and d.day == 31
                                               else 'no')
        self.columns['is_holiday'] = ('yes'
                                      if h.is_holiday(d)
                                      else 'no')
        self.columns['holiday_name'] = h.get_holiday_name(d)
        self.columns['season_name'] = self.get_season(d)
        self.columns['one_year_ago_date'] = (
            d - timedelta(days=366
                          if calendar.isleap(d.year)
                          else 365)).isoformat()
        self.columns['one_year_ago_date_key'] = self.make_date_key(
            (d - timedelta(days=366 if calendar.isleap(d.year) else 365)))

    def generate_insert_statement(self):
        #insert = ("INSERT INTO date_dimension (%s) VALUES (%s)\n" %
        #          (', '.join(['%s']*(len.self.columns),)*2)
        keys = sorted(self.columns.keys())
        return ("INSERT INTO date_dimension (%s) VALUES (%s);\n" %
                (', '.join(keys),
                 ', '.join(map(lambda k:
                               ("'%s'" % self.columns[k].replace("'", "''"))
                               if isinstance(self.columns[k], str)
                               else '%d' % self.columns[k], keys))))


    def __init__(self, d):
        # Week starts on Sunday
        calendar.setfirstweekday(calendar.SUNDAY)
        self.date = d
        self.columns = dict()
        self.initialize_table()

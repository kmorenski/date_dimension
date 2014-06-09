#!/usr/bin/env python

import sys
import os
import datetime
from date_dimension import DateDimension


def iterate_calendar(start, end):
    curr = start
    one_day = datetime.timedelta(days=1)
    while curr < end:
        curr += one_day
        yield curr


def generate_date_dimension(start, end=datetime.date(2020,12,31)):
    e = {
        'year_number_in_epoch': 0,
        'half_number_in_epoch': 0,
        'quarter_number_in_epoch': 0,
        'month_number_in_epoch': 0,
        'week_number_in_epoch': 0,
        'day_number_in_epoch': 0,
    }
    prev_date_dim = DateDimension(start)
    for d in iterate_calendar(start, end):
        date_dim = DateDimension(d)
        if date_dim.columns['year_key'] != prev_date_dim.columns['year_key']:
            e['year_number_in_epoch'] += 1
        if date_dim.columns['half_number_in_year'] != prev_date_dim.columns['half_number_in_year']:
            e['half_number_in_epoch'] += 1
        if date_dim.columns['quarter_number_in_year'] != prev_date_dim.columns['quarter_number_in_year']:
            e['quarter_number_in_epoch'] += 1
        if date_dim.columns['month_number_in_year'] != prev_date_dim.columns['month_number_in_year']:
            e['month_number_in_epoch'] += 1
        if date_dim.columns['week_number_in_year'] != prev_date_dim.columns['week_number_in_year']:
            e['week_number_in_epoch'] += 1
        if date_dim.columns['day_number_in_year'] != prev_date_dim.columns['day_number_in_year']:
            e['day_number_in_epoch'] += 1
        for k in e.keys():
            date_dim.columns[k] = e[k]
        prev_date_dim = date_dim
        yield date_dim


if __name__ == '__main__':
    #with open('date_dimension_inserts.sql', 'w') as f:
    #    for dim in generate_date_dimension(datetime.date(2000, 1, 1)):
    #        f.write(dim.generate_insert_statement())
    sys.stdout.write(sql)
    sys.stdout.flush()


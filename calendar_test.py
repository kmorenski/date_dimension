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
from calendars.holidays import Holidays


# def iterate_calendar(start, fmt='%Y%m%d'):
#     """Generates each day of the calendar, starting from the given date in the
#     format specified."""
#     curr_day = datetime.date(*time.strptime(start, fmt)[:3])
#     day_offset = datetime.timedelta(days=1)
#     while True:
#         curr_day += day_offset
#         yield curr_day

def display_holidays(start, end):
    """Displays the holiday names and dates in the range of years specified
    (inclusive)."""
    for year in xrange(start, end+1):
        holidays = Holidays(year)
        sys.stdout.write("%d:\n" % year)  # display the year in YYYY format
        for holiday_str in [k for k in dir(holidays)
                            if k.startswith('holiday_')]:
            #sys.stdout.write("\t%s: " % holiday_str)
            sys.stdout.write("\t%s\t%s\n" % getattr(holidays, holiday_str)())
        sys.stdout.flush()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Process year arguments")
    parser.add_argument('start_year', metavar='FIRST_YEAR', type=int,
                        help='the first year (in YYYY format)')
    parser.add_argument('end_year', metavar='FINAL_YEAR', type=int,
                        help='the final year (in YYYY format)')
    args = parser.parse_args()
    display_holidays(int(args.start_year), int(args.end_year))



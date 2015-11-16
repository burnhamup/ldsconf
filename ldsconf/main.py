import argparse
import math
from datetime import datetime, timedelta

from ldsconf import studyplan


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def get_default_dates():
    now = datetime.now()
    if 4 <= now.month < 10:
        month = 4
    else:
        month = 10
    year = now.year
    if now.month < 4:
        year -= 1
    start_date = studyplan.get_conference_start_date(month, year)
    start_date += timedelta(days=7)

    next_month = 4 if month == 10 else 10
    next_year = year + (1 if month == 10 else 0)
    end_date = studyplan.get_conference_start_date(next_month, next_year)
    end_date += timedelta(days=7)

    return start_date, end_date


def main():
    parser = argparse.ArgumentParser()
    default_start_date, default_end_date = get_default_dates()
    parser.add_argument('-s', '--start_date', help="Start date for the study plan - format YYYY-MM-DD",
                        default=default_start_date, type=valid_date)
    parser.add_argument('-e', '--end_date', help="End date for the study plan - format YYYY-MM-DD",
                        default=default_end_date, type=valid_date)
    parser.add_argument('-n', '--study_periods', help="Number of study periods", default=None, type=int)
    args = parser.parse_args()

    # Validation
    if args.start_date >= args.end_date:
        raise Exception("Start date must be before end date")
    number_of_days = (args.end_date - args.start_date).days
    number_of_talks = studyplan.get_number_of_talks_in_most_recent_conference()
    maximum_study_periods = math.ceil(number_of_days / float(number_of_talks))
    study_periods = args.study_periods
    while study_periods is None:
        try:
            study_periods = int(raw_input("How many study periods would like? (1-%d)" % maximum_study_periods))
        except ValueError:
            print "Please enter a number."

    if study_periods > maximum_study_periods or study_periods <= 0:
        raise Exception("Number of study periods must be in range 1-%d" % maximum_study_periods)

    result = studyplan.generate_study_plan(args.start_date, args.end_date, study_periods)
    for plan in result:
        print "Conference Plan"
        for date, talk in plan:
            print "  %s -- %s, %s (%s-%s)" % (date.strftime("%m-%d-%Y"), talk.title, talk.author, talk.year, talk.month)

if __name__ == '__main__':
    main()

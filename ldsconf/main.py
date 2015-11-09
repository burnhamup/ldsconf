"""
    Questions to ask:
    Start Date
    End Date
    Calculate number of days
    Calculate number of talks in the most recent conference.
    Max number of study periods is equal to days / number of talks.
    Ask how many study periods to have.
"""
import argparse
import math
from datetime import datetime
from pprint import pprint
import studyplan


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_date', help="Start date for the study plan - format YYYY-MM-DD", default=None, type=valid_date)
    parser.add_argument('end_date', help="End date for the study plan - format YYYY-MM-DD", default=None, type=valid_date)
    parser.add_argument('study_periods', help="Number of study periods", default=None, type=int)
    args = parser.parse_args()

    # Validation
    if args.start_date >= args.end_date:
        raise Exception("Start date must be before end date")
    number_of_days =  (args.end_date -args.start_date).days
    number_of_talks = studyplan.get_number_of_talks_in_most_recent_conference()
    maximum_study_plans = math.ceil(number_of_days / float(number_of_talks))
    if args.study_periods > maximum_study_plans or args.study_periods <= 0:
        raise Exception("Number of study periods must be in range 1-%d" % maximum_study_plans)

    result = studyplan.generate_study_plan(args.start_date, args.end_date, args.study_periods)
    for plan in result:
        print "Conference Plan"
        for date, talk in plan:
            print "  %s -- %s, %s (%s-%s)" % (date.strftime("%m-%d-%Y"), talk.title, talk.author, talk.year, talk.month)


if __name__ == "__main__":
    main()

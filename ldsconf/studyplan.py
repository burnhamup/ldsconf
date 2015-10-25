import copy
from datetime import date, timedelta
from random import randint, shuffle
import json

__author__ = 'Chris'


def generate_study_plan(month, year):
    """

    :param start_date: The date of the conference you want to start with.
    :return:  A list of tuples containing ( <date>, <Talk Name> )
    """
    study_periods = 3
    # Calculate the dates of the conferences
    start_date = get_conference_start_date(month, year)
    next_month = 4 if month == 10 else 10
    next_year = year + (1 if month == 10 else 0)
    end_date = get_conference_start_date(next_month, next_year)
    start_date += timedelta(days=7)
    end_date += timedelta(days=7)
    dates = get_partition_dates(end_date, start_date, study_periods)

    with open('../data/conferences.json', 'r') as json_file:
        all_conference_talks = json.load(json_file)
    results = []
    for segment_start, segment_end in zip(dates[:-1], dates[1:]):
        talks = sort_talks(segment_start, segment_end, all_conference_talks, month, year)
        for n, talk in zip(range((segment_end-segment_start).days), talks):
            current_date = segment_start + timedelta(days=n)
            results.append((current_date.isoformat(), talk))

    return results


def get_partition_dates(end_date, start_date, study_periods):
    days_difference = (end_date - start_date).days
    days_length = days_difference / study_periods
    dates = [start_date]
    for n in range(1, study_periods):
        partition_date = dates[-1] + timedelta(days=days_length)
        if days_difference % study_periods >= n:
            partition_date += timedelta(days=1)
        dates.append(partition_date)
    dates.append(end_date)
    return dates


def sort_talks(start_date, end_date, all_conference_talks, month, year):
    number_of_talks_to_grab = (end_date - start_date).days
    # Always include the most recent conference
    key = "%s-%s" % (month, year)
    assert key in all_conference_talks
    assert number_of_talks_to_grab >= len(all_conference_talks[key]['talks'])
    results = []
    results.extend(all_conference_talks[key]['talks'])
    number_of_talks_to_grab -= len(results)

    conference_talks = copy.copy(all_conference_talks)
    conference_talks.pop(key)

    weighted_sum = sum(conference['weight'] for conference in conference_talks.itervalues())
    while number_of_talks_to_grab > 0:
        choice = randint(1, weighted_sum)
        chosen_conference = None
        for conference in conference_talks.itervalues():
            choice -= conference['weight']
            if choice <= 0:
                chosen_conference = conference
                break
        talks = chosen_conference['talks']

        chosen_talk_index = randint(0, len(talks)-1)
        chosen_talk = copy.copy(talks[chosen_talk_index])
        chosen_talk['year'] = chosen_conference['year']
        chosen_talk['month'] = chosen_conference['month']

        if chosen_talk not in results:
            number_of_talks_to_grab -= 1
            results.append(chosen_talk)
    shuffle(results)
    return results


def get_conference_start_date(month, year):
    start = date(year, month, 1)
    days_to_first_sunday = 6 - start.weekday()
    start += timedelta(days=days_to_first_sunday)
    return start
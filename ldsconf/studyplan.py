import copy
from datetime import date, timedelta
from random import randint, shuffle

from ldsconf.conference import get_all_conferences


def generate_study_plan(start_date, end_date, study_periods, file_location=None):
    dates = get_partition_dates(end_date, start_date, study_periods)
    conferences = get_all_conferences(file_location)
    results = []
    for segment_start, segment_end in zip(dates[:-1], dates[1:]):
        talks = pick_talks(segment_start, segment_end, conferences)
        results.append(talks)
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


def get_number_of_talks_in_most_recent_conference():
    conferences = get_all_conferences()
    latest_conference_talk_key = sorted(conferences.keys(), reverse=True)[0]
    return len(conferences[latest_conference_talk_key])


def pick_talks(start_date, end_date, all_conference_talks):
    number_of_talks_to_grab = (end_date - start_date).days
    # Include the most recent conference
    latest_conference_talk_key = sorted(all_conference_talks.keys(), reverse=True)[0]
    selected_talks = []
    selected_talks.extend(all_conference_talks[latest_conference_talk_key].talks)
    if len(selected_talks) >= number_of_talks_to_grab:
        shuffle(selected_talks)
        return package_talks(start_date, end_date, selected_talks[:number_of_talks_to_grab])

    number_of_talks_to_grab -= len(selected_talks)

    conference_talks = copy.copy(all_conference_talks)
    conference_talks.pop(latest_conference_talk_key)

    weighted_sum = sum(conference.weight for conference in conference_talks.itervalues())
    while number_of_talks_to_grab > 0:
        choice = randint(1, weighted_sum)
        chosen_conference = None
        for conference in conference_talks.itervalues():
            choice -= conference.weight
            if choice <= 0:
                chosen_conference = conference
                break
        talks = chosen_conference.talks

        chosen_talk_index = randint(0, len(talks)-1)
        chosen_talk = copy.copy(talks[chosen_talk_index])

        if chosen_talk not in selected_talks:
            number_of_talks_to_grab -= 1
            selected_talks.append(chosen_talk)
    shuffle(selected_talks)
    return package_talks(start_date, end_date, selected_talks)


def package_talks(start_date, end_date, selected_talks):
    shuffle(selected_talks)
    results = []

    for n, talk in zip(range((end_date-start_date).days), selected_talks):
        current_date = start_date + timedelta(days=n)
        results.append((current_date, talk))
    return results


def get_conference_start_date(month, year):
    start = date(year, month, 1)
    days_to_first_sunday = 6 - start.weekday()
    start += timedelta(days=days_to_first_sunday)
    return start

from datetime import date, timedelta
from time import sleep
from lxml import html
import requests
import json

__author__ = 'Chris'


def generate_study_plan(month, year):
    """

    :param start_date: The date of the conference you want to start with.
    :return:  A list of tuples containing ( <date>, <Talk Name> )
    """

    # Calculate the dates of the conferences
    start_date = get_conference_start_date(month, year)
    next_month = 4 if month == 10 else 10
    next_year = year + (1 if month == 10 else 0)
    end_date = get_conference_start_date(next_month, next_year)
    start_date += timedelta(days=7)
    end_date += timedelta(days=7)

    with open('conferences.json', 'r') as json_file:
        all_conference_talks = json.load(json_file)
    

    # Partition the dates into 3 sections
    # talks = sort_talks(start_date, end_date, all_conference_talks)

    # Combine these three together and return

    pass

CONFERENCE_URL = "https://www.lds.org/general-conference/sessions/%s/%s?lang=eng"


def get_conference_talks(year, month):
    url = CONFERENCE_URL % (year, month)
    page = requests.get(url)

    tree = html.fromstring(page.text)
    talks_html = tree.xpath('//td[span[@class="talk"]/a]')
    talks = []
    for talk_html in talks_html:
        title = talk_html[0][0].text
        link = talk_html[0][0].attrib['href']
        author = talk_html[1].text
        talk = Talk(title, link, author)
        talks.append(talk)
    weight = year - 1970 + (1 if month == 10 else 0)
    conference = {
        'month': month,
        'year': year,
        'key': '%s-%s' % (month, year),
        'talks': talks,
        'weight': pow(2, weight - 2)
    }
    return conference


class Talk(dict):
    def __init__(self, title, url, author):
        self['title'] = title
        self['url'] = url
        self['author'] = author


def generate_conference_history(start_year, end_year):
    conferences = {}
    for year in range(start_year, end_year):
        for month in (4, 10):
            conference = get_conference_talks(year, month)
            sleep(1)
            conferences[conference['key']] = conference
            print "%s - %s" % (year, month)
    return conferences




def sort_talks(start_date, end_date, all_conference_talks):
    pass


def get_conference_start_date(month, year):
    start = date(year, month, 1)
    days_to_first_sunday = 7 - start.weekday()
    start + timedelta(days=days_to_first_sunday)
    return start




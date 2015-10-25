import json
from time import sleep
from lxml import html
import requests

__author__ = 'Chris'
CONFERENCE_URL = "https://www.lds.org/general-conference/sessions/%s/%02d?lang=eng"


def get_conference(year, month):
    url = CONFERENCE_URL % (year, month)
    print url
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
        'weight': pow(2, max(weight - 1, 0))
    }
    return conference


class Talk(dict):
    def __init__(self, title, url, author, **kwargs):
        super(Talk, self).__init__(**kwargs)
        self['title'] = title
        self['url'] = url
        self['author'] = author


def generate_conference_history(start_year, end_year):
    conferences = {}
    for year in range(start_year, end_year + 1):
        for month in (4, 10):
            conference = get_conference(year, month)
            sleep(1)
            conferences[conference['key']] = conference
            print "%s - %s" % (year, month)
    return conferences


def update_file():
    with open('../data/conferences.json', 'r') as json_file:
        all_conference_talks = json.load(json_file)
    for conference_key, conference in all_conference_talks.items():
        weight = conference['year'] - 1970 + (1 if conference['month'] == 10 else 0)
        conference['weight'] = pow(2, max(weight-1, 0))
    with open('../data/conferences.json', 'w') as json_file:
        json.dump(all_conference_talks, json_file, indent=2)

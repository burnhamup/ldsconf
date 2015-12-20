import json
from time import sleep
import os
import sys


CONFERENCE_URL = "https://www.lds.org/general-conference/sessions/%s/%02d?lang=eng"
CONFERENCE_FILE_NAME = os.path.join(sys.prefix, 'data', 'conferences.json')

conferences = None

def get_conference(month, year):
    from lxml import html
    import requests
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
        talk = Talk(title, link, author, month, year)
        talks.append(talk)
    return Conference(month, year, talks)

def get_all_conferences(conference_file=None):
    global conferences
    if conferences is None:
      conferences = {}
      if conference_file is None:
        conference_file = CONFERENCE_FILE_NAME
      with open(conference_file, 'r') as json_file:
          all_conference_talks = json.load(json_file)
      for conference_key, conference in all_conference_talks.iteritems():
          talks = []
          for talk in conference['talks']:
              talks.append(Talk(talk['title'], talk['url'], talk['author'], conference['month'], conference['year']))
          conferences[conference_key] = Conference(conference['month'], conference['year'], talks)
    return conferences


class Conference(object):
    def __init__(self, month, year, talks):
        self.month = month
        self.year = year
        self.key = '%d-%02d' % (year, month)
        self.talks = talks

    def __len__(self):
        return len(self.talks)

    @property
    def weight(self):
        weight = self.year - 1970 + (1 if self.month == 10 else 0)
        return pow(2, max(weight - 1, 0))

    def to_dict(self):
        return {
            'month': self.month,
            'year': self.year,
            'talks': [talk.to_dict() for talk in self.talks]
        }

    @staticmethod
    def get_all_conferences(conference_file=None):
        if conferences is None:
          if conference_file is None:
            conference_file = CONFERENCE_FILE_NAME
          with open(conference_file, 'r') as json_file:
              all_conference_talks = json.load(json_file)
          for conference_key, conference in all_conference_talks.iteritems():
              talks = []
              for talk in conference['talks']:
                  talks.append(Talk(talk['title'], talk['url'], talk['author'], conference['month'], conference['year']))
              conferences[conference_key] = Conference(conference['month'], conference['year'], talks)
        return conferences

    @staticmethod
    def save(conferences):
        raw_data = {}
        for conference_key, conference in conferences.iteritems():
            raw_data[conference_key] = conference.to_dict()
        with open(CONFERENCE_FILE_NAME, 'w') as json_file:
            json.dump(raw_data, json_file, indent=2)


class Talk(object):
    def __init__(self, title, url, author, month, year):
        self.title = title
        self.url = url
        self.author = author
        self.month = month
        self.year = year

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'author': self.author
        }


def generate_conference_history(start_year, end_year):
    conferences = {}
    for year in range(start_year, end_year + 1):
        for month in (4, 10):
            conference = get_conference(month, year)
            sleep(1)
            conferences[conference.key] = conference
            print "%s - %s" % (year, month)
    return conferences


def update_file():
    with open(CONFERENCE_FILE_NAME, 'r') as json_file:
        all_conference_talks = json.load(json_file)
    for conference_key, conference in all_conference_talks.items():
        weight = conference['year'] - 1970 + (1 if conference['month'] == 10 else 0)
        conference['weight'] = pow(2, max(weight-1, 0))
    with open('../data/conferences.json', 'w') as json_file:
        json.dump(all_conference_talks, json_file, indent=2)

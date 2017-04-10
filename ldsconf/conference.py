import json
from time import sleep
import os
import sys


CONFERENCE_URL = 'https://www.lds.org/general-conference/%s/%02d?lang=eng'
CONFERENCE_FILE_NAME = os.path.join(sys.prefix, 'data', 'conferences.json')

conferences = None

def get_conference(month, year):
    from lxml import html
    import requests
    url = CONFERENCE_URL % (year, month)
    print url
    page = requests.get(url)

    tree = html.fromstring(page.text)
    talks_html = tree.xpath('//a[@class="lumen-tile__link"]')
    talks = []
    for talk_html in talks_html:
        link = 'https://www.lds.org' + talk_html.attrib['href']
        if 'media' in link:
            continue

        title = talk_html[1][0][0].text.strip()
        author = talk_html[1][1].text.strip()

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

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.year, self.month, self.author, self.title, self.url))

def generate_conference_history(start_year, end_year):
    conferences = {}
    for year in range(start_year, end_year + 1):
        for month in (4, 10):
            conference = get_conference(month, year)
            sleep(1)
            conferences[conference.key] = conference
            print "%s - %s" % (year, month)
    return conferences


def add_latest_conference(month, year):
    existing_conferences = get_all_conferences()
    newest_conference = get_conference(month, year)
    existing_conferences[newest_conference.key] = newest_conference
    Conference.save(existing_conferences)


def save_conference(conferences):
    with open(CONFERENCE_FILE_NAME, 'w') as json_file:
        json.dump(conferences, json_file, indent=2)

def update_file():
    with open(CONFERENCE_FILE_NAME, 'r') as json_file:
        all_conference_talks = json.load(json_file)
    for conference_key, conference in all_conference_talks.items():
        weight = conference['year'] - 1970 + (1 if conference['month'] == 10 else 0)
        conference['weight'] = pow(2, max(weight-1, 0))
    with open('../data/conferences.json', 'w') as json_file:
        json.dump(all_conference_talks, json_file, indent=2)

if __name__ == '__main__':
    add_latest_conference(4, 2017)

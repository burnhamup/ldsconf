from pprint import pprint
from ldsconf.conference import update_file, Conference
from ldsconf.studyplan import generate_study_plan

__author__ = 'Chris'


conferences = Conference.get_all_conferences()
Conference.save(conferences)
# results = generate_study_plan(10, 2015)
# for date, talk in results:
#     print "%s - %s, %s (%s, %s)" % (date, talk['title'], talk['author'], talk.get('year', 2015), talk.get('month', 10))
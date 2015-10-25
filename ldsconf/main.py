from pprint import pprint
from ldsconf.conference import update_file, Conference
from ldsconf.studyplan import generate_study_plan

__author__ = 'Chris'

#
# conferences = Conference.get_all_conferences()
# Conference.save(conferences)
results = generate_study_plan(10, 2015)
for plan in results:
    print "Plan"
    for date, talk in plan:
        print "%s - %s, %s (%s, %s)" % (date, talk.title, talk.author, talk.year, talk.month)

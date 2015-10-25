from pprint import pprint
from ldsconf.conference import update_file, Conference
from ldsconf.studyplan import generate_study_plan

__author__ = 'Chris'

#
conferences = Conference.get_all_conferences()
for conference in conferences.itervalues():
    def keep_talk(talk):
        if 'Presented' in talk.author or 'Statistical Report' in talk.title or 'Church Audit' in talk.title or 'Sustaining of Church Officers' in talk.title or 'Church Finance Committee Report' in talk.title:
            return False
        return True
    conference.talks = filter(keep_talk, conference.talks)
Conference.save(conferences)


# results = generate_study_plan(10, 2015)
# for plan in results:
#     print "Plan"
#     for date, talk in plan:
#         print "%s - %s, %s (%s, %s)" % (date, talk.title, talk.author, talk.year, talk.month)

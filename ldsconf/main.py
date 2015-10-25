from pprint import pprint
from ldsconf.conference import update_file
from ldsconf.studyplan import generate_study_plan

__author__ = 'Chris'

results = generate_study_plan(10, 2015)
for talk in results:
    pprint(talk)
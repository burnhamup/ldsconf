# LDS General Conference Study Plan

This program will create a study plan for General Conference. Specify a start data, an end date, and the number of study plans you wish to create. Talks will be gathered first from the most recent General Conference and any gaps will be filled in with talks from previous conferences.

## Installation
`pip install git+git://github.com/myuser/foo.git`

## Basic Usage
`ldsconf -s 2015-10-12 -e 2016-04-03`
You can also use the library to access the study plans directly for help with formatting.
```
from datetime import date
from ldsconf import studyplan

result = studyplan.generate_study_plan(date(2015, 10, 12) , date(2016, 4, 3), 3)
for plan in result:
    print "Conference Plan"
    for date, talk in plan:
        print "  %s -- %s, %s (%s-%s)" % (date.strftime("%m-%d-%Y"), talk.title, talk.author, talk.year, talk.month)  
```       
## Example Output
[See example.md](example.md)

## TODO
* Update flag to grab the latest talks after a new conference has happened.
* My next project is to hook this script up to a website to generate these plans in a user friendly way.
* Improved formatting options
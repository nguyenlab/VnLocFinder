__author__ = 'danilo@jaist.ac.jp'

import re
import csv
import urllib2
from qa_model import PersonAnswer
from dal.db import QAStore

FILE_SCHOOLS = "data/jaist_staff_schools.csv"
PRESIDENT_ID = 33

def load_file():
    store = QAStore()
    with open(FILE_SCHOOLS) as staff_file:
        csvr = csv.reader(staff_file, delimiter=",", quotechar='"')
        for row in csvr:
            person = PersonAnswer()
            person.name = row[0]
            person.uri = row[5]

            staff_id_mo = re.search(r"profile_id=(?P<sid>\d+)&", person.uri)
            if (staff_id_mo):
                staff_id = int(staff_id_mo.group("sid"))
            else:
                staff_id = PRESIDENT_ID

            person.pictureURL = "http://www.jaist.ac.jp/profiles/pict/{:05d}.jpeg".format(staff_id)

            try:
                picture = urllib2.urlopen(person.pictureURL).read()
            except:
                try:
                    person.pictureURL = "http://www.jaist.ac.jp/profiles/pict/{:05d}.pjpeg".format(staff_id)
                    picture = urllib2.urlopen(person.pictureURL).read()
                except:
                    person.pictureURL = "http://www.jaist.ac.jp/profiles/pict/{:05d}.x-citrix-pjpeg".format(staff_id)

            for i in [1, 2, 3]:
                person.keywords.append(row[i])

            person.keywords.extend(row[4].split(","))

            store.insert_answer(person)

            print person.to_dict()


def main():
    load_file()



if __name__ == '__main__':
    main()
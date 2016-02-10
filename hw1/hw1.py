import urllib2
import sys
import re

RE_CLASSES_MAIN = re.compile('<div class="classes-main-toggle-buttons">(.+)</div>', re.DOTALL)
RE_CLASS_TITLE  = re.compile('<table .*?class="class-title">(.+?)</table>')
RE_CLASS_NAME   = re.compile('<td class="class-name">(.+?)</td>', re.DOTALL)
RE_CLASS_INFO   = re.compile('<td class="class-number">(.+?)</td><td class="class-location">(.+?)</td><td class="class-schedule">(.+?)</td>', re.DOTALL)

year     = 2015
term     = 2
graduate = 0
url      = 'http://www.mathcs.emory.edu/classes-semester.php?subject=CS&year=%d&term=%d&graduate=%d' % (year, term, graduate)

request  = urllib2.Request(url)
response = urllib2.urlopen(request)
page     = response.read()
atlas_kb       = dict()

m = RE_CLASSES_MAIN.search(page)
main = m.group(1)

titles = [(m.group(1), m.start(), m.end()) for m in RE_CLASS_TITLE.finditer(main)]


def splitTitle(title):
    name = RE_CLASS_NAME.search(title).group(1)
    t = name.split(':')
    cnum = ''.join(t[0].split())
    cdes = t[1].strip()
    return (cnum, cdes)

for i,title in enumerate(titles):
    (course_number, course_title) = splitTitle(title[0])

    start = title[2]
    if i+1 < len(titles): end = titles[i+1][1]
    else: end = -1

    for m1 in RE_CLASS_INFO.finditer(main, start, end):
        section  = m1.group(1).strip()
        location = m1.group(2).strip()
        schedule = m1.group(3).strip()

        k = (course_number+'-'+section).upper()
        atlas_kb[k] = (course_title, location, schedule)

# course = sys.argv[1]

RE_EXAM_MAIN = re.compile('<section class="clearfix" id="section2">(.+?)</section>', re.DOTALL)
RE_EXAM_TABLE = re.compile('<tbody>(.+?)</tbody>', re.DOTALL)
RE_EXAM_ROWS = re.compile('<tr>(.+?)</tr>', re.DOTALL)
RE_EXAM_TUPLE = re.compile('<p>(?!<strong>)(.+?)</p>')
RE_COURSE_TIME = re.compile('^(([\d]+):\d{2})', re.MULTILINE)

exam_url = 'http://registrar.emory.edu/Students/Calendars/examcalendar/emorycollege_examcalendar.html'

exam_request  = urllib2.Request(exam_url)
exam_response = urllib2.urlopen(exam_request)
exam_page     = exam_response.read()
exam_kb       = dict()

page_match = RE_EXAM_MAIN.search(exam_page)
page_html = page_match.group(1)

table = RE_EXAM_TABLE.search(page_html)
t = table.group(1)

rows = [(r.group(1), r.start(), r.end()) for r in RE_EXAM_ROWS.finditer(t)]


def split_row(table_row):
    match = RE_EXAM_TUPLE.findall(table_row)
    if match:
        match[0] = match[0].replace('&#160;', '')
        return match

    return None


def create_key(course_hours):
    data = course_hours.split()
    days = data[0].upper().replace('TU', 'T')
    match = RE_COURSE_TIME.search(data[1][:-2])
    if match:
        time = match.group(1)
        hour = match.group(2)
        if int(hour) in range(8, 10):
            return '0' + time + ' ' + days
        return time + ' ' + days

    return None

for row in rows:
    record = split_row(row[0])
    if record is not None:
        key = record[0].upper()
        value = record[1:]
        exam_kb[key] = tuple(value)


sorted_courses = sorted(atlas_kb)

for i in range(len(sorted_courses)):
    course = sorted_courses[i]
    course_full_name = course.split('-')
    course_title = course_full_name[0]
    course_section = course_full_name[1]

    if 'LAB' in course_section:
        lab_day = atlas_kb[course][2].split()[0]
        lecture_course = sorted_courses[i-1]
        original_tuple = atlas_kb[lecture_course]
        original_lecture_day = original_tuple[2].split()[0]
        new_lecture_day = original_tuple[2].replace(original_lecture_day, original_lecture_day + lab_day)
        new_tuple = original_tuple[:2] + (new_lecture_day,)
        atlas_kb[lecture_course] = new_tuple


def pretty_print(strings):
    result = '%10s %10s %20s %25s %15s %25s' % tuple(strings)
    return result


print pretty_print(['Course', 'Section', 'Location', 'Class hours', 'Final date', 'Final hours'])

for k in sorted_courses:
    if 'L' not in k:
        exam_tuple = exam_kb[create_key(atlas_kb[k][2])]
        exam_date = exam_tuple[1]
        exam_hours = exam_tuple[2]

        full_name = k.split('-')
        course = full_name[0]
        section = full_name[1]

        details = atlas_kb[k]
        location = details[1].replace(':', '')
        hours = details[2]

        print pretty_print([course, section, location, hours, exam_date, exam_hours])

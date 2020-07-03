from collections import deque

from schedule import parse
from schedule import errors


class Section:

    def __init__(self, course_name, times: tuple):
        self.course_name = course_name
        self.start = times[0]
        self.end = times[1]

    def __str__(self) -> str:
        s = str(self.course_name) + ": (" + str(self.start) + ", " + str(self.end) + ")"
        return s


# Intent: Sort a list of events by their end times
# Precondition 1: events is a non-empty list of 2-element tuples of floats
# Precondition 2: For each tuple (s,f) in events, 9 <= s < f <= 17,
#   where s and f refer to the start and end times of an event in 24-hr time
def sortByEndTime(courses):
    print(courses)
    # TODO: Create sorting function from scratch, according to Dr. Braude (1 Jul 2020)
    courses.sort(key=lambda x: x[1])
    print(courses)


# INVARIANT: events_sorted contains the same tuples as events

# POSTCONDITION: events are sorted by their end time

# ==============================================================

# PRECONDITION:

def flattenCourses(courses) -> deque:

    x = deque()
    return x


# ==============================================================

def retrieveSections(courses_str):
    raw_section_data  = list(map(parse.convertCourseToTime, parse.splitByCourse(courses_str)))
    res = []
    for section in raw_section_data:
        for time in section[1]:
            res.append(Section(section[0], time))

    return res



# ==============================================================


if __name__ == '__main__':
    course_str = "Calc_I 900 945 1201 1320  1030 1115 1345 1500 / Physics_II 1450 1700 1600 1630 1645 1700"
    sections = retrieveSections(course_str)
    for s in sections:
        print(s)

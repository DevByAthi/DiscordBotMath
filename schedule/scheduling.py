from collections import deque

from schedule import parse
from schedule import errors


class Section:

    def __init__(self, course_name, times: tuple):
        self.course_name = course_name
        self.start = times[0]
        self.end = times[1]

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        s = str(self.course_name) + " from " + str(self.start) + " to " + str(self.end)
        return s

    def __lt__(self, other):
        return self.end < other.end


def doesConflict(section1, section2):
    return (section1.start <= section2.start < section1.end) or (section2.start <= section1.start <= section2.end)


# Intent: Sort a list of events by their end times
# Precondition 1: events is a non-empty list of 2-element tuples of floats
# Precondition 2: For each tuple (s,f) in events, 9 <= s < f <= 17,
#   where s and f refer to the start and end times of an event in 24-hr time
def sortByEndTime(sections):
    print(sections)
    # TODO: Create sorting function from scratch, according to Dr. Braude (1 Jul 2020)
    sections.sort()
    print(sections)


# INVARIANT: events_sorted contains the same tuples as events

# POSTCONDITION: events are sorted by their end time

# ==============================================================

# INTENT: Sort from dictionary of sections, where

# PRECONDITION: each

def flattenCourses(sections_input) -> list:
    res = []
    while len(sections_input) > 0:
        min_val = 1701
        min_key = ""
        for course_name in sections_input.keys():
            cur_deque = sections_input[course_name]
            print("DEQUE: ", cur_deque)
            if len(cur_deque) == 0:
                continue
            if (cur_deque)[0].end < min_val:
                min_val = (cur_deque)[0].end
                min_key = (cur_deque)[0].course_name
                print(min_key, min_val)
        if min_key == "":
            break
        val = sections_input[min_key].popleft()
        res.append(val)
        print("TEST ", val, min_val)
    return res


# ==============================================================

def retrieveSections(courses_str):
    raw_section_data  = list(map(parse.convertCourseToTime, parse.splitByCourse(courses_str)))
    res = dict()
    for section in raw_section_data:
        if not section[0] in res:
            res[section[0]] = deque()
        for time in section[1]:
            res[section[0]].append(Section(section[0], time))

    return res

# POSTCONDITION: A dictionary with keys as the class names
# and values as lists of Section objects is returned

# ==============================================================


if __name__ == '__main__':
    course_str = "Calc_I 900 945  1030 1115 1201 1320 1345 1700 / Physics_II 1600 1630 1645 1700 1450 1700"
    sections = retrieveSections(course_str)
    print(sections)
    flattenCourses(sections)
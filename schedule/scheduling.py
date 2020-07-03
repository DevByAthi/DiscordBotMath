from collections import deque

from schedule import parse


class Section:

    def __init__(self, course_name, times):
        self.course_name = course_name
        self.times = times


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

def flattenCourses(course_name, sessions) -> deque:
    print(course_name)
    print(sessions)
    x = deque()
    return x


# ==============================================================


if __name__ == '__main__':
    course_str = "Calc_I 900 945 1201 1320  1030 1115 1345 1500"
    print(flattenCourses(*parse.convertCourseToTime(course_str)))

from schedule.parse import *

# Intent: Sort a list of events by their end times
# Precondition 1: events is a non-empty list of 2-element tuples of floats
# Precondition 2: For each tuple (s,f) in events, 9 <= s < f <= 17,
#   where s and f refer to the start and end times of an event in 24-hr time
def sortByEndTime(events):
    for event in events:
        # check that event has start and end times within working hours
        if not(900 <= event[0] <= event[1] <= 1700):
            return False
        # check that time format is valid, with minutes within an hour
        elif event[0] % 100 > 59 or event[1] % 100 > 59:
            return False

    print(events)
    # TODO: Create sorting function from scratch, according to Dr. Braude (1 Jul 2020)
    events.sort(key=lambda x: x[1])

    return True


# INVARIANT: events_sorted contains the same tuples as events

# POSTCONDITION: events are sorted by their end time

# ==============================================================

# Checks that input list is a list of only tuples of floats/ints

def checkFormat(events):
    validity = [(isinstance(x, tuple)) and (len(x) == 2)
                and (isinstance(x[0], int) or isinstance(x[0], float))
                and (isinstance(x[1], int) or isinstance(x[1], float))
                for x in events]
    print(validity)
    return all(validity)
# ==============================================================




if __name__ == '__main__':

    convertCourseToTime("1 2 3 4 5 8 5 8")

    print("===============")

    events = [(1, 2), (1.0, 2), (1.0, 2.0), (5,7), (4,6)]
    sortByEndTime(convertCourseToTime("1 2 3 4 5 8 5 8"))
    sortByEndTime(convertCourseToTime("900 930 1045 1100"))
    print(events)

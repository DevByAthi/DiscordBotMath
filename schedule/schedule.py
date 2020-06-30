# Intent: Sort a list of events by their end times
# Precondition 1: events is a non-empty list of 2-element tuples of floats
# Precondition 2: For each tuple (s,f) in events, 9 <= s < f <= 17,
#   where s and f refer to the start and end times of an event in 24-hr time
def sortByEndTime(events):
    if not(checkFormat(events)):
        return

    # TODO: May have to create sorting function from scratch, check with Dr. Braude
    events.sort(key=lambda x: x[1])

# INVARIANT: events_sorted contains the same tuples as events

# POSTCONDITION: events are sorted by their end time

#==============================================================

# Checks that input list is a list of only tuples

def checkFormat(events):
    validity = [(isinstance(x, tuple)) and (len(x) == 2)
                and (isinstance(x[0], int) or isinstance(x[0], float))
                and (isinstance(x[1], int) or isinstance(x[1], float))
                for x in events]
    print(validity)
    return all(validity)


if __name__ == '__main__':
    events = [(1, 2), (1.0,2),(111, 20,2),9,'1',(1,'2'),(1.0,2.0),(1,0,'2.0')]
    print(checkFormat(events))

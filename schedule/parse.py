import schedule
from schedule import errors


def checkPartialSorting(events):
    for i in range(len(events) - 1):
        if events[i + 1] < events[i]:
            return False
    return True

def convertToTimeInt(inStr):
    val = -1
    try:
        val = int(inStr)
    except ValueError:
        raise errors.TimeFormatError("Input must be an integer value representing a time between 900 and 1700")

    if val < 900:
        raise errors.TimeFormatError("Given time is too early. Must be on or after 9 am.")

    if val > 1700:
        raise errors.TimeFormatError("Given time is too late. Must be on or before 5 pm.")

    if val % 100 > 59:
        raise errors.TimeFormatError("Not a valid time. Minutes must be less than 60")

    return val


def convertCourseToTime(course_str):
    raw_list = course_str.split()
    course_name = raw_list[0]
    processed_list = list(map(convertToTimeInt, raw_list[1:]))

    if len(processed_list) % 2 == 1:
        print("fail")
        raise errors.ScheduleFormatError("A listed section is missing either a start or end time")

    events = []
    for i in range(0, len(processed_list), 2):
        events.append((processed_list[i], processed_list[i + 1]))

    if not(checkPartialSorting(events)):
        raise errors.ScheduleFormatError("A course in your input does not have its section correctly ordered!")

    return course_name, events

def splitByCourse(raw_str):
    derived_courses = raw_str.split('/')
    for derived_course in derived_courses:
        if derived_course.strip() == '':
            raise errors.ScheduleFormatError("A course with no sections is listed. Remove any extra / in the file, "
                                             "including the very end")

    return derived_courses

if __name__ == "__main__":
    raw_in = "Calc_I 900 945 1030 1115 1345 1500 / Physics_II 1450 1700"
    courses = splitByCourse(raw_in)
    for course in courses:
        print(course)
        print(convertCourseToTime(course)[1])

    print(list(map(convertCourseToTime, courses)))

    print("Good:")
    good = ["945", "1232","1700","900","1459","1432"]
    for time in good:
        try:
            convertToTimeInt(time)
        except errors.TimeFormatError as error:
            print("Error ", error, " with time ", time)

    bad = ["0645","645","859","960","1275","1701","-1432", "a1432", "Zee", "10:45"]

    print("Good completed\n\nBad:")

    for time in bad:
        try:
            convertToTimeInt(time)
        except errors.TimeFormatError as err:
            print("Error ", err, " with time ", time)

import schedule
from schedule import errors


def splitByCourse(raw_str):
    derived_courses = raw_str.split('/')
    for derived_course in derived_courses:
        if derived_course.strip() == '':
            raise errors.ScheduleFormatError("A course with no sections is listed. Remove any extra / in the file, "
                                             "including the very end")

    return derived_courses


def convertCourseToTime(course):
    raw_list = course.split()
    course_name = raw_list[0]
    processed_list = list(map(errors.convertToTimeInt, raw_list[1:]))

    if len(processed_list) % 2 == 1:
        print("fail")
        raise errors.ScheduleFormatError("A listed section is missing either a start or end time")

    events = []
    for i in range(0, len(processed_list), 2):
        events.append((processed_list[i], processed_list[i + 1]))
    return events


if __name__ == "__main__":
    raw_in = "Calc_I 900 945 1030 1115 1345 1500 / Physics_II 1450 1700"
    courses = splitByCourse(raw_in)
    for course in courses:
        print(course)
        print(convertCourseToTime(course))
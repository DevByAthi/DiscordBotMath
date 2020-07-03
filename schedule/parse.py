def convertCourseToTime(in_str):
    raw_list = in_str.split()
    processed_list = []
    try:
        processed_list = list(map(int, raw_list))
    except ValueError:
        return

    if len(processed_list) % 2 == 1:
        return

    events = []
    for i in range(0, len(processed_list), 2):
        events.append((processed_list[i], processed_list[i+1]))
    return events
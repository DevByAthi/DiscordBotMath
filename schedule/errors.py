class TimeFormatError(ValueError):
    def __init__(self, message):
        self.message = message


def parseFormat(inStr):
    val = -1
    try:
        val = int(inStr)
    except ValueError:
        raise TimeFormatError("input must be an integer value representing a time between 900 and 1700")

    if val < 900:
        raise TimeFormatError("Given time is too early. Must be on or after 9 am.")

    if val > 1700:
        raise TimeFormatError("Given time is too late. Must be on or before 5 pm.")

    if val % 100 > 59:
        raise TimeFormatError("Not a valid time. Minutes must be less than 60")

    return val


if __name__ == "__main__":
    print("Good:")
    good = ["945", "1232","1700","900","1459","1432"]
    for time in good:
        try:
            parseFormat(time)
        except TimeFormatError as error:
            print("Error ", error, " with time ", time)

    bad = ["0645","645","859","960","1275","1701","-1432", "a1432", "Zee", "10:45"]

    print("Good completed\n\nBad:")

    for time in bad:
        try:
            parseFormat(time)
        except TimeFormatError as error:
            print("Error ", error, " with time ", time)
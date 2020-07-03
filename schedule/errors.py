class ScheduleFormatError(Exception):
    def __init__(self,message):
        self.message = message


class TimeFormatError(ValueError):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    from schedule import parse
    print("Good:")
    good = ["945", "1232","1700","900","1459","1432"]
    for time in good:
        try:
            parse.convertToTimeInt(time)
        except TimeFormatError as error:
            print("Error ", error, " with time ", time)

    bad = ["0645","645","859","960","1275","1701","-1432", "a1432", "Zee", "10:45"]

    print("Good completed\n\nBad:")

    for time in bad:
        try:
            parse.convertToTimeInt(time)
        except TimeFormatError as err:
            print("HI")
            print("Error ", err, " with time ", time)
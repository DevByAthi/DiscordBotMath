class ScheduleFormatError(Exception):
    def __init__(self,message):
        self.message = message


class TimeFormatError(ValueError):
    def __init__(self, message):
        self.message = message


if __name__ == "__main__":
    pass

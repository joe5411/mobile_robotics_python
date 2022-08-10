import time
from datetime import datetime


def get_time():
    stamp = datetime.utcnow()
    return float(datetime.timestamp(stamp))


def sleep(duration):
    if duration < 0.0:
        return
    else:
        time.sleep(duration)


class Rate(object):
    """
    Convenience class for sleeping in a loop at a specified rate
    """

    def __init__(self, hz):
        """
        Constructor.
        @param hz: hz rate to determine sleeping
        @type  hz: int
        """
        self.last_time = get_time()
        self.sleep_dur = 1.0 / hz

    def _remaining(self, curr_time):
        """
        Calculate the time remaining for rate to sleep.
        @param curr_time: current time
        @type  curr_time: L{Time}
        @return: time remaining
        @rtype: L{Time}
        """
        # detect time jumping backwards
        if self.last_time > curr_time:
            self.last_time = curr_time

        # calculate remaining time
        elapsed = curr_time - self.last_time
        return self.sleep_dur - elapsed

    def remaining(self):
        """
        Return the time remaining for rate to sleep.
        @return: time remaining
        @rtype: L{Time}
        """
        curr_time = get_time()
        return self._remaining(curr_time)

    def sleep(self):
        """
        Attempt sleep at the specified rate. sleep() takes into
        account the time elapsed since the last successful
        sleep().
        """
        curr_time = get_time()
        sleep(self._remaining(curr_time))
        self.last_time = self.last_time + self.sleep_dur

        # detect time jumping forwards, as well as loops that are
        # inherently too slow
        if curr_time - self.last_time > self.sleep_dur * 2:
            self.last_time = curr_time


if __name__ == "__main__":
    import random

    r = Rate(10.0)
    curr_time = get_time()
    while True:
        diff = 1.0 / (get_time() - curr_time)
        curr_time = get_time()
        x = random.random() / 10.0
        print(diff, x)
        # Random time-lenght long computation
        time.sleep(x)
        r.sleep()

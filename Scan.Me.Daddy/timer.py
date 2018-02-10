import time


def pretty_time(ms):
    if ms < 1000:
        return '%dMS' % (int(ms))
    seconds = int(ms / 1000.0)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%d Days %d Hrs %d Mins %d Secs' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%d Hrs %d Mins %dSecs' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%d Mins %d Secs' % (minutes, seconds)
    else:
        return '%dSecs' % (seconds)

class Timer:
    def __init__(self):
        self.before = 0

    def start(self, msg):
        print msg
        self.before = time.time()
        return self

    def stop(self, msg):
        print msg,pretty_time((time.time()-self.before)*1000)
        return self
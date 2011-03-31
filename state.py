from collections import namedtuple
from Queue import Queue, Empty

class User(object):
    __slots__ = ["other", "lang", "queue"]
    def __init__(self, other, lang="en", queue=None):
        if queue is None: queue = Queue()
        self.other = other
        self.lang = lang
        self.queue = queue
    def __repr__(self):
        return "User({other}, lang={lang}, queue({qsize})".format(other=self.other, lang=self.lang, qsize=self.queue.qsize())

SW = {} # Switchboard
SINGLE = Queue()

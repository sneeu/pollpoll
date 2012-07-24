import redis


rconn = redis.StrictRedis(host='localhost', port=6379, db=0)


def _poll_key(key):
    return 'poll:%s' % key


def _choices_key(key):
    return '%s:choices' % _poll_key(key)


class Poll(object):
    def __init__(self, key, question, choices):
        self.key = key
        self.question = question
        self.choices = choices

    @classmethod
    def create(cls, question):
        key = rconn.incr(_poll_key('_id'))
        rconn.set(_poll_key(key), question)
        return Poll(key, question, [])

    @classmethod
    def load(cls, key, and_choices=True):
        raw_poll = rconn.get(_poll_key(key))
        choices = None
        if and_choices:
            choices = Choice.load(key)
        return cls(key, raw_poll, choices)

    def choice_by_name(self, name):
        for choice in self.choices:
            if choice.name == name:
                return choice
        return None


class Choice(object):
    def __init__(self, key, name, votes=0):
        self.key = key
        self.name = name
        self.votes = votes

    @classmethod
    def create(cls, key, name):
        rconn.zincrby(_choices_key(key), name, 0)
        return Choice(key, name, 0)

    @classmethod
    def load(cls, key):
        raw_choices = rconn.zrange(
            _choices_key(key), 0, -1, withscores=True)
        return [cls(key, name, int(score)) for name, score in raw_choices]

    def register_vote(self):
        return rconn.zincrby(_choices_key(self.key), self.name, 1)

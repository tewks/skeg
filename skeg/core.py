# vim:ts=4:sw=4:expandtab
"""
diesel_redis_wrap

simple redis prototyping in diesel.

forked from https://github.com/amix/redis_wrap

"""
from diesel.protocols import redis 

def get_redis(host='localhost', port=6379):
    # TODO use connection pool
    return redis.RedisClient(host=host, port=port)

class Composite(object):
    # A composite class that is composed of Wrappers
    properties = {}

    def key(self, key):
        return ':'.join([self.id, key])

    def __init__(self, id):
        self.id = id 
        for property_name in self.properties:
            setattr(self, property_name, self.properties[property_name](self.key(property_name)))


class Wrapper(object):
    # Base class for a wrapper around a Redis object
    def __init__(self, name):
        self.name = name

    @property
    def redis(self):
        return redis.RedisClient()

class List(Wrapper):
    def push(self, item):
        self.redis.lpush(self.name, item)

    def insert(self, i, x):
        self.redis.linsert(self.name, i, x)

    def append(self, x):
        self.redis.rpush(self.name, x)
 
    def extend(self, iterable):
        for item in iterable:
            self.append(item)

    def remove(self, value):
        self.redis.lrem(self.name, value)

    def pop(self, index=None):
        if index:
            raise ValueError('Not supported')
        return self.redis.rpop(self.name)

    def __len__(self):
        return self.redis.llen(self.name)

    def __iter__(self):
        client = self.redis
        i = 0
        while True:
            items = client.lrange(self.name, i, i+30)
            if len(items) == 0:
                raise StopIteration
            for item in items:
                yield item
            i += 30

    def __getitem__(self, s):
       if not s.stop:
           s = slice(s.start, len(self), s.step)
       if not s.start:
           s = slice(0, s.stop, s.step)
       result = self.redis.lrange(self.name, s.start, s.stop-1) 
       if (s.step == None or s.step == 1):
            return result
       else:
            return result.__getitem__(s)
	

class Dict(Wrapper):
    def get(self, key, default=None):
        return self.redis.hget(self.name, key) or default

    def keys(self):
        return self.redis.hkeys(self.name) or []

    def values(self):
        return self.redis.hvals(self.name) or []

    def __len__(self):
        return self.redis.hlen(self.name) or 0

    def __getitem__(self, key):
        val = self.get(key)
        if not val:
            raise KeyError
        return val

    def __setitem__(self, key, value):
        self.redis.hset(self.name, key, value)

    def __delitem__(self, key):
        self.redis.hdel(self.name, key)

    def __contains__(self, key):
        return self.redis.hexists(self.name, key)


class Set(Wrapper):
    def add(self, item):
        self.redis.sadd(self.name, item)

    def remove(self, item):
        self.redis.srem(self.name, item)

    def pop(self, item):
        return self.redis.spop(self.name, item)

    def __iter__(self):
        client = self.redis
        for item in client.smembers(self.name):
            yield item

    def __len__(self):
        return len(self.redis.smembers(self.name))

    def __contains__(self, item):
        return self.redis.sismember(self.name, item)

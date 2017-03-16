import redis

redis_server = redis.Redis("127.0.0.1")
print "Entries left",redis_server.llen("activeServer")
redis_server.flushall()
print "Entries left",redis_server.llen("activeServer")
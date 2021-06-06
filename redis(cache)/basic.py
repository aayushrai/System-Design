import redis

r= redis.Redis()

r.set("yash","verma")
r.mset({"ankit":"kasrniya","shaily":"rai"})

print(r.get("shaily"))
print(r.mget({"mayank","ankit"}))

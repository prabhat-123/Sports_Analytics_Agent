import redis

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6375, db=0)

# Example: Get all keys and their values
keys = redis_client.keys()
for key in keys:
    print(f"{key.decode('utf-8')}: {redis_client.get(key).decode('utf-8')}")

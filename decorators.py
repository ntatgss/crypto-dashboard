from functools import wraps
from flask import request, jsonify
from time import time

def rate_limited(max_per_minute):
    storage = {}
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            key = f"{request.remote_addr}:{f.__name__}"
            now = time()
            storage.setdefault(key, [])
            storage[key] = [t for t in storage[key] if now - t < 60]
            if len(storage[key]) >= max_per_minute:
                return jsonify(error="Rate limit exceeded"), 429
            storage[key].append(now)
            return f(*args, **kwargs)
        return wrapper
    return decorator
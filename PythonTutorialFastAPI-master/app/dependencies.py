import time

from fastapi import HTTPException, Response

count = 0
start_time = time.time()
reset_interval = 10
limit = 50


def rate_limit(response: Response) -> None:
    global start_time
    global count

    if time.time() > start_time + reset_interval:
        start_time = time.time()
        count = 0

    if count >= limit:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "timeout": round(start_time + reset_interval - time.time(), 2) + 0.01,
            },
        )
    count += 1
    response.headers["X-app-rate-limit"] = f"{count}:{limit}"
    return None

import time


class Time:
    delta: float = 0.0
    timeSinceStart: float = 0.0
    frameCount: int = 0

    _last_time: float = time.time()

    @staticmethod
    def Update():
        now = time.time()
        Time.delta = now - Time._last_time
        Time.timeSinceStart += Time.delta
        Time._last_time = now
        Time.frameCount += 1
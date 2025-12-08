from pyre.time import Time


class Timer:
    def __init__(self, duration: float, flag: bool = False):
        self.m_flag: bool = flag
        self._m_duration: float = duration
        self._m_elapsedTime: float = duration

    def Tick(self) -> bool:
        if self.m_flag:
            return self.m_flag

        self._m_elapsedTime -= Time.deltaTime

        if self._m_elapsedTime <= 0:
            self.m_flag = True
            self._m_elapsedTime = 0

        return self.m_flag

    def Reset(self) -> None:
        self.m_flag = False
        self._m_elapsedTime = self._m_duration
from pyre.components import BaseComponent


class Movement(BaseComponent):
    def __init__(self, *, moveSpeed: float, rotSpeed: float) -> None:
        super().__init__()
        self.m_moveSpeed = moveSpeed
        self.m_rotSpeed = rotSpeed

    def Init(self) -> None:
        super().Init()

    def Uninit(self) -> None:
        super().Uninit()
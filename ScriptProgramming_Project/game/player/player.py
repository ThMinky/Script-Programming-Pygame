from pyre.behaviours import Behaviour


class Player(Behaviour):
    def __init__(self) -> None:
        super().__init__()

        self.m_moveSpeed: float = 50.0
        self.m_rotSpeed: float = 25.0

    def Update(self) -> None:
        super().Update()
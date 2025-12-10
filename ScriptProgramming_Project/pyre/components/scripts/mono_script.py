from pyre.components import BaseComponent


class MonoScript(BaseComponent):
    def __init__(self) -> None:
        super().__init__()

        self._m_started: bool = False

    def Enable(self) -> None:
        super().Enable()

        self.OnEnable()

    def Disable(self) -> None:
        self.OnDisable()

        super().Disable()

    def Destroy(self) -> None:
        super().Destroy()

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        pass

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass
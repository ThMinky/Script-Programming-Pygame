from pyre.components import BaseComponent


class BaseScript(BaseComponent):
    def __init__(self) -> None:
        super().__init__()

        self.Init()

    def Enable(self) -> None:
        super().Enable()

        self.OnEnable()

    def Disable(self) -> None:
        self.OnDisable()

        super().Disable()

    def Destroy(self) -> None:
        super().Destroy()

    def Awake(self) -> None:
        pass

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        pass

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass
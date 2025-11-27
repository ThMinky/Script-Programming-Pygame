from pyre.components import BaseComponent


class Script(BaseComponent):
    def __init__(self) -> None:
        super().__init__()

        self.Init()

    def Awake(self) -> None:
        pass

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        pass

    def Enable(self):
        super().Enable()

        self.OnEnable()

    def Disable(self):
        self.OnDisable()

        super().Disable()

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def Destroy(self) -> None:
        self.Uninit()
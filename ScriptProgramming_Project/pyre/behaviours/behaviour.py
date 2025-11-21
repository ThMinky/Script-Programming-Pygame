class Behaviour:
    def __init__(self) -> None:
        from pyre.managers import BehaviourManager

        BehaviourManager.GetInstance().Register(self)

    def Update(self) -> None:
        pass

    def Destroy(self) -> None:
        from pyre.managers import BehaviourManager

        BehaviourManager.GetInstance().Unregister(self)
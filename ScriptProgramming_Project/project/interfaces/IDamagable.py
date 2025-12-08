from typing import Protocol, runtime_checkable


@runtime_checkable
class IDamagable(Protocol):
    def TakeDamage(self, amount: int) -> None:
        ...
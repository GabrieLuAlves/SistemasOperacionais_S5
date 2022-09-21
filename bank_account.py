from datetime import datetime
from enum import Enum
from multiprocessing import Semaphore
from threading import Thread
from time import sleep
from typing import Any, Iterable, List, Mapping

nCaixas = 5


class Logger:
    instance = None

    def __init__(self) -> None:
        self.semaphore = Semaphore(1)
        self.begin = datetime.now()
        Logger.instance = None

    def getInstance():
        if not Logger.instance:
            Logger.instance = Logger()

        return Logger.instance

    def __call__(self, string: str) -> Any:
        self.semaphore.acquire(1)

        time = (datetime.now() - self.begin).total_seconds()
        print(f"[{time}]", string)

        self.semaphore.release()


log = Logger.getInstance()


class CashMachineStatus(Enum):
    AVAILABLE = 0,
    OPERATING = 1


class CashMachineOperation:
    def __init__(self):
        self.semaphore = Semaphore(0)

    def execute(self):
        sleep(1)
        self.semaphore.release()


class CashMachine(Thread):
    sessions = Semaphore(nCaixas)

    def __init__(self, name: str | None = ..., args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = ...) -> None:
        self.lock = Semaphore(0)
        self.status = CashMachineStatus.AVAILABLE
        self.operation: CashMachineOperation = None
        super().__init__(None, None, name, args, kwargs)

    def start(self) -> None:
        super().start()

    def run(self) -> None:
        log(f"[{self.name}] started")
        while True:
            self.lock.acquire(True)
            self.operation.execute()


class Client(Thread):
    def __init__(
        self,
        name: str | None = ...,
        attendance_period: int = ...,
        args: Iterable[Any] = ...,
        kwargs: Mapping[str, Any] | None = ...
    ) -> None:
        super().__init__(None, None, name, args, kwargs)

        self.attendance_period = attendance_period

    def start(self, cash_machines: List[CashMachine]) -> None:
        self.cash_machines = cash_machines
        super().start()

    def run(self) -> None:
        log(f"{self.name} joined the queue")
        CashMachine.sessions.acquire(True)

        # Client looks for cash machine
        cash_machine: CashMachine = None
        for cm in self.cash_machines:
            if cm.status == CashMachineStatus.AVAILABLE:
                cm.status = CashMachineStatus.OPERATING
                cash_machine = cm
                break

        # In the case there are no cash machines available
        if not cash_machine:
            raise Exception("Unexpected error happened on schedule")

        # begin attendament
        operation = CashMachineOperation()
        for i in range(self.attendance_period):
            cash_machine.operation = operation
            cash_machine.lock.release()
            operation.semaphore.acquire(True)

        # finish
        log(f"{self.name} leaves")
        cm.status = CashMachineStatus.AVAILABLE
        CashMachine.sessions.release()


def main():
    nClients = nCaixas * 2 + 1
    cash_machines: List[CashMachine] = []
    clients: List[Client] = []

    for i in range(nCaixas):
        cash_machines.append(CashMachine(name=f"Cash machine #{i}"))

    for i in range(nClients):
        clients.append(Client(name=f"Client {i}", attendance_period=2))

    for cash_machine in cash_machines:
        cash_machine.start()

    for i in range(nClients):
        clients[i].start(cash_machines)


if __name__ == "__main__":
    main()

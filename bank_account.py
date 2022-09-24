from calendar import c
from datetime import datetime
from enum import Enum
from multiprocessing import Semaphore
from threading import Thread
from time import sleep
from tracemalloc import start
from typing import Any, Iterable, List, Mapping


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


class CashMachine(Thread):
    def __init__(self, cash_machine_id: str = ...) -> None:
        super().__init__(name=cash_machine_id)
        self.lock = Semaphore(0)
        self.operation_lock = Semaphore(0)
        self.status = CashMachineStatus.AVAILABLE
        self.attendance_period = 0

    def start(self) -> None:
        super().start()

    def run(self) -> None:
        log(f"[{self.name}] started")
        while True:
            self.lock.acquire(True)
            start = datetime.now()

            prev_fib = 0
            fib = 1
            while(datetime.now() - start).total_seconds() <= self.attendance_period:
                aux = fib
                fib += prev_fib
                prev_fib = aux

            self.operation_lock.release()


class Client(Thread):
    def __init__(
        self,
        client_name: str = ...,
        attendance_period: int = ...,
        code: int = ...,
    ) -> None:
        super().__init__(name=client_name)

        self.attendance_period = attendance_period
        self.code = code

        self.cash_machine: CashMachine = None

    def run(self) -> None:
        sessions.acquire(True)

        cash_machines_semaphore.acquire(True)

        for cash_machine in cash_machines:
            if cash_machine.status == CashMachineStatus.AVAILABLE:
                self.cash_machine = cash_machine
                self.cash_machine.status = CashMachineStatus.OPERATING
                break

        cash_machines_semaphore.release()

        assert self.cash_machine is not None, "Schedule error"
        log(f"[{self.name}] attendament started on {self.cash_machine.name}")

        self.cash_machine.attendance_period = self.attendance_period

        start = datetime.now()
        self.cash_machine.lock.release()
        self.cash_machine.operation_lock.acquire(True)
        end = datetime.now()

        self.cash_machine.status = CashMachineStatus.AVAILABLE

        log(f"[{self.name}] attendament finished ({(end - start).total_seconds()})")
        sessions.release()


def main():
    global sessions
    global cash_machines_semaphore
    global cash_machines

    nCaixas = 5
    nClients = nCaixas + 1

    sessions = Semaphore(nCaixas)
    cash_machines_semaphore = Semaphore(1)
    cash_machines = []

    for i in range(nCaixas):
        cash_machines.append(CashMachine(cash_machine_id=f"Cash machine #{i}"))

    for cash_machine in cash_machines:
        cash_machine.start()

    for i in range(nClients):
        Client(client_name=f"Client {i}", attendance_period=4, code=i).start()


if __name__ == "__main__":
    main()

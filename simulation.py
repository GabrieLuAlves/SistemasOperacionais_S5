from datetime import datetime
from enum import Enum
from multiprocessing import Semaphore
from threading import Thread
from time import sleep
from typing import Any, List

from shared import Observer


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


class ClientStatus(Enum):
    WAITING = 0,
    ON_ATTENDAMENT = 1,
    FINISHED = 2


class CashMachine(Thread):
    instances = []
    sessions = Semaphore(0)

    def __init__(self, id: int = ...) -> None:
        super().__init__(name=f"Caixa {id}")
        self.lock = Semaphore(0)

        self.id = id
        self.available = True

        self.progress = 0
        self.attendance_period = 0

        self.observers: List[Observer] = []

    def run(self) -> None:
        CashMachine.instances.append(self)

        log(f"[{self.name}] started")

        while True:
            elapsed_time = 0

            self.available = True
            self.progress = 0
            self.notifyAll()

            CashMachine.sessions.release()

            self.lock.acquire(True)

            start = datetime.now()

            while elapsed_time <= self.attendance_period:
                elapsed_time = (datetime.now() - start).total_seconds()
                self.progress = elapsed_time / self.attendance_period * 100
                self.notifyAll()
                sleep(0.00000001)

    def attach(self, observer):
        self.observers.append(observer)

    def notifyAll(self):
        for observer in self.observers:
            observer.notify()


class Client(Thread):
    semaphore = Semaphore(1)

    def __init__(
        self,
        client_name: str = ...,
        attendance_period: int = ...,
        code: int = ...,
    ) -> None:
        super().__init__(name=client_name)

        self.elapsed_time = 0
        self.attendance_period = attendance_period
        self.code = code

        self.status = "Na fila"

        self.cash_machine: CashMachine = None
        self.observers: List[Observer] = []

    def run(self) -> None:
        CashMachine.sessions.acquire(True)

        Client.semaphore.acquire(True)

        for cash_machine in CashMachine.instances:
            if cash_machine.available:
                self.cash_machine = cash_machine
                self.cash_machine.attendance_period = self.attendance_period
                self.cash_machine.available = False

                break

        Client.semaphore.release()

        assert self.cash_machine is not None, "Schedule error"

        start = datetime.now()

        self.cash_machine.lock.release()
        log(f"{self.name} on attendament ({self.cash_machine.name})")
        self.status = "Em atendimento"
        self.notifyAll()

        while self.elapsed_time < self.attendance_period:
            self.elapsed_time = (datetime.now() - start).total_seconds()
            self.notifyAll()
            sleep(0.00000001)
           

        end = datetime.now()

        self.elapsed_time = (end - start).total_seconds()
        self.status = "Atendido"
        self.notifyAll()

        log(f"[{self.name}] attendament finished ({self.elapsed_time})")

    def attach(self, observer: Observer):
        self.observers.append(observer)

    def notifyAll(self):
        for observer in self.observers:
            observer.notify()


def main():
    global sessions

    nCaixas = 5
    nClients = 5

    sessions = Semaphore(nCaixas)

    for i in range(nClients):
        Client(f"Client {i}", 5, i).start()


if __name__ == "__main__":
    main()

from enum import Enum
from queue import Queue
from threading import Semaphore, Thread
from time import sleep
from typing import List


class CashMachineStatus(Enum):
    WAITING_FOR_CLIENT = 0,
    PROCESSING_REQUEST = 1


class Operation:
    def __init__(self) -> None:
        self.operationSemaphore = Semaphore(1)

    def run(self, time):
        sleep(time)


class CashMachine(Thread):
    def start(self, id) -> None:
        self.id = id
        self.status = CashMachineStatus.WAITING_FOR_CLIENT

        self.attendance = Semaphore(1)

        super().start()

    def run(self):
        print(f"[{self.id}] started")
        while True:
            self.status = CashMachineStatus.WAITING_FOR_CLIENT
            self.attendance.acquire(True)

    def isAvailable(self):
        return self.status == CashMachineStatus.WAITING_FOR_CLIENT


class Client(Thread):
    def start(self, name: str, ta: int, senha: str) -> None:
        self.name = name
        self.ta = ta
        self.senha = senha
        self.cash_machine = None

        self.attendanceSemaphore = Semaphore(1)

        super().start()

    def run(self):
        # await for cash machine
        self.attendanceSemaphore.acquire(True)

    def proceedToAttendance(self, cash_machine: CashMachine):
        self.cash_machine = cash_machine
        self.attendanceSemaphore.release()

        self.cash_machine.attendance.release()


class BankQueue(Thread):
    def start(self) -> None:
        self.clientQueue = Queue()
        super().start()


def main(nCaixas):
    cashMachines: List[CashMachine] = []
    for i in range(nCaixas):
        cashMachines.append(CashMachine())

    for index, cashMachine in enumerate(cashMachines):
        cashMachine.start(f"Cash machine n.{index}")

    sleep(1)


if __name__ == '__main__':
    main(3)

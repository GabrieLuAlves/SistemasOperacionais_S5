from queue import Queue
from threading import Semaphore, Thread
from time import sleep
from typing import List

from models import CashMachine, Client


class CashMachineAttendance(Thread):
    def start(self, cash_machine: CashMachine) -> None:
        self.cash_machine: CashMachine = cash_machine
        self.client: Client = None

        self.semaphore = Semaphore(1)

        super().start()

    def run(self):
        while True:
            # await for client
            self.semaphore.acquire(True)

            self.cash_machine.account = self.client.account
            self.cash_machine.deposit(100)
            sleep(1)

            self.client = None
            self.cash_machine.account = None


class BankQueue(Thread):
    def __init__(self, listCashMachines):
        self.queue = Queue()
        self.mutex = Semaphore(1)

    def wait(self, mySem):
        self.mutex.wait()
        self.queue.add(mySem)
        self.mutex.signal()
        mySem.wait()

    def signal(self):
        self.mutex.wait()
        sem = self.queue.remove()
        self.mutex.signal()
        sem.signal()


def main():
    cashMachineAttendances: List(CashMachineAttendance) = []
    for i in range(10):
        cashMachine = CashMachine()
        cashMachineAttendances.append(CashMachineAttendance(cashMachine))

    for cashMachineAttendance in cashMachineAttendances:
        cashMachineAttendance.start()

    BankQueue(cashMachineAttendances).start()


if __name__ == '__main__':
    main()

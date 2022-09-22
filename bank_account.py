from datetime import datetime
from enum import Enum
from multiprocessing import Semaphore
from threading import Thread
from time import sleep
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


class CashMachineOperation:
    def execute(self):
        sleep(1)


class CashMachine(Thread):
    def __init__(self, name: str = ...) -> None:
        super().__init__(None, None, name)
        self.lock = Semaphore(0)
        self.operation_lock = Semaphore(0)
        self.status = CashMachineStatus.AVAILABLE
        self.operation: CashMachineOperation = None

    def start(self) -> None:
        super().start()

    def run(self) -> None:
        log(f"[{self.name}] started")
        while True:
            self.lock.acquire(True)
            self.operation.execute()
            self.operation_lock.release()


class Client(Thread):
    def __init__(
        self,
        name: str = ...,
        attendance_period: int = ...,
        code: int = ...,
    ) -> None:
        super().__init__(None, None, name)

        self.attendance_period = attendance_period
        self.code = code

        self.cash_machine: CashMachine = None
        self.session: Semaphore = None

        self.client_lock = Semaphore(0)

    def run(self) -> None:
        self.client_lock.acquire(True)
        log(f"{self.name} - Attendance started")

        assert self.cash_machine is not None, "Schedule error"
        assert self.session is not None, "Schedule error"

        for _ in range(self.attendance_period):
            self.cash_machine.operation = CashMachineOperation()
            self.cash_machine.lock.release()
            self.cash_machine.operation_lock.acquire(True)
            # sleep(1)

        log(f"{self.name} - Attendance finished")
        self.cash_machine.status = CashMachineStatus.AVAILABLE
        self.session.release()


class BankQueue:
    def __init__(self):
        self.list: List[Client] = []
        self.queue_semaphore = Semaphore(1)

    def insert(self, client: Client) -> None:
        self.queue_semaphore.acquire(True)
        self.list.append(client)
        client.start()
        self.queue_semaphore.release()

    def pop(self) -> Client | None:
        client = None
        self.queue_semaphore.acquire(True)

        if len(self.list) > 0:
            client = self.list.pop(0)

        self.queue_semaphore.release()

        return client


class CashMachineList:
    def __init__(self, number: int):
        self.list: List[CashMachine] = []
        self.cash_machines_semaphore = Semaphore(1)

        for i in range(number):
            self.list.append(CashMachine(name=f"Cash machine #{i + 1}"))

    def startAll(self):
        for cash_machine in self.list:
            cash_machine.start()

    def reserveOne(self) -> CashMachine:
        cm: CashMachine = None
        self.cash_machines_semaphore.acquire(True)
        for cash_machine in self.list:
            if cash_machine.status == CashMachineStatus.AVAILABLE:
                cash_machine.status = CashMachineStatus.OPERATING
                cm = cash_machine
                break

        self.cash_machines_semaphore.release()

        return cm


class Scheduler(Thread):
    def __init__(self, bank_queue: BankQueue, cash_machines: CashMachineList) -> None:
        super().__init__(None, None, "Scheduler")
        self.cash_machines = cash_machines
        self.bank_queue = bank_queue

        self.sessions = Semaphore(len(cash_machines.list))

    def run(self):
        while True:
            self.sessions.acquire(True)

            client: Client = None
            while not client:
                client = self.bank_queue.pop()

            log(f"Allocating cash machine for: {client.name}")

            cash_machine = self.cash_machines.reserveOne()

            assert cash_machine is not None, "Schedule error"
            log(f"{client.name} using {cash_machine.name}")

            client.session = self.sessions
            client.cash_machine = cash_machine
            client.client_lock.release()


def main():
    nCaixas = 2
    nClients = 5

    cash_machines = CashMachineList(nCaixas)
    bank_queue = BankQueue()

    cash_machines.startAll()

    scheduler = Scheduler(bank_queue, cash_machines)
    scheduler.start()

    for i in range(nClients):
        client = Client(name=f"Client {i + 1}", attendance_period=5, code=i)
        bank_queue.insert(client)


if __name__ == "__main__":
    main()

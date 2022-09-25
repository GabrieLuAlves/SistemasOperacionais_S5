from calendar import c
from datetime import datetime
from enum import Enum
from multiprocessing import Semaphore
from threading import Thread
from time import sleep
from tracemalloc import start
from typing import Any, Iterable, List, Mapping

import pygame
from pygame.locals import *
from sys import exit

from interface import *

import random

pygame.init()


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
        self.progress = 0

    def start(self) -> None:
        super().start()

    def run(self) -> None:
        log(f"[{self.name}] started")
        while True:
            self.lock.acquire(True)

            self.progress = 0
            elapsed_time = 0
            start = datetime.now()

            while elapsed_time <= self.attendance_period:
                elapsed_time = (datetime.now() - start).total_seconds()
                self.progress = elapsed_time / self.attendance_period * 100

            self.operation_lock.release()


cash_machines: List[CashMachine] = []
cash_machines_semaphore = Semaphore(1)


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
        self.cash_machine = None

        log(f"[{self.name}] attendament finished ({(end - start).total_seconds()})")
        sessions.release()


clients: List[Client] = []

window = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Trabalho SO")


def main():
    global sessions

    nCaixas = 3
    nClients = 8

    sessions = Semaphore(nCaixas)

    for i in range(nCaixas):
        cash_machines.append(CashMachine(cash_machine_id=f"Cash machine #{i}"))

    for cash_machine in cash_machines:
        cash_machine.start()

    for i in range(nClients):
        client = Client(
            client_name=f"Client {i}", attendance_period=random.randint(3, 5), code=i)
        client.start()
        clients.append(client)

    window_width = 640
    window_height = 480

    pygame.init()
    pygame.display.set_caption("Projeto de Sistemas Operacionais")

    window = pygame.display.set_mode((window_width, window_height))
    window.set_colorkey((255, 255, 255))

    margin_left = window_width * (1 - 0.8) / 2
    top = 30
    height = 30
    width = window_width * 0.25
    padding = 10

    distance = height + padding

    while True:
        window.fill((50, 50, 50))

        i = 0
        for client in clients:
            if client.cash_machine is not None:
                cash_machine = client.cash_machine
                if client.cash_machine.progress < 100:
                    Label(
                        surface=window,
                        left=margin_left,
                        top=top + distance * i,
                        size=24,
                        height=height,
                        colour=(255, 255, 255),
                        background=(50, 50, 50),
                        text=f"{client.name}"
                    ).draw()

                    ProgressBar(
                        window,
                        margin_left + 100,
                        top + distance * i,
                        width,
                        height
                    ).draw(cash_machine.progress)

                    i += 1

        for event in pygame.event.get():
            if event.type == locals.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()


if __name__ == "__main__":
    main()


from multiprocessing import Semaphore


class Database:
    def __init__(self):
        self.semaphore = Semaphore(1)

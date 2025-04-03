import queue
import threading
import time

class SingletonQueue:
    _instances = {}

    def __new__(cls, thread_name):
        if thread_name not in cls._instances:
            cls._instances[thread_name] = queue.Queue()
        return cls._instances[thread_name]
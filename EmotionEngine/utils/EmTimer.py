import time


class EmTimer:
    def __init__(self, delay_ms: float, callback_on_finished: any) -> None:
        self.__started = False
        self.__finished = False
        self.__delay_ms = delay_ms

        self.__started_at = None
        self.__callback_on_finished = callback_on_finished

    def get_current_milli_time(self):
        return time.time() * 1000

    def start(self):
        self.__started = True
        self.__finished = False
        self.__started_at = self.get_current_milli_time()

    def update(self):

        if self.__started and not self.__finished:
            diff: float = self.get_current_milli_time() - self.__started_at

            if diff >= self.__delay_ms:
                self.__finished = True
                self.__callback_on_finished()

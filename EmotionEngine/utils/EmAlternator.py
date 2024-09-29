import time


class EmAlternator:
    def __init__(self, delay_ms: float, count: int = 3) -> None:
        self.__running = False
        self.__delay_ms = delay_ms
        self.__count = 0
        self.__max_count = count
        self.__visible = True
        self.__started_at = None

    def get_current_milli_time(self):
        return time.time() * 1000

    def start(self):
        self.__running = True
        self.__visible = False
        self.__count = 0
        self.__started_at = self.get_current_milli_time()

    def get_visible(self) -> bool:
        return self.__visible or (not self.__running)

    def update(self):
        if not self.__running:
            return

        diff: float = self.get_current_milli_time() - self.__started_at

        if diff > self.__delay_ms:
            if self.__count >= self.__max_count + 1:
                self.__running = False

            self.__started_at = self.get_current_milli_time()
            self.__count += 1
            self.__visible = not self.__visible

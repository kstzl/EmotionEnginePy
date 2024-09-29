import time


class EmAlternator:
    """
    A class to create an alternator effect that toggles visibility at a specified interval.

    This class allows you to start an alternation effect that changes the visibility state
    between `True` and `False` for a specified number of times, with a configurable delay
    between each toggle.
    """

    def __init__(self, delay_ms: float, count: int = 3) -> None:
        self.__running = False
        self.__delay_ms = delay_ms
        self.__count = 0
        self.__max_count = count
        self.__visible = True
        self.__started_at = None

    def get_current_milli_time(self):
        """
        Gets the current time in milliseconds.

        Returns:
            float: The current time in milliseconds since the epoch.
        """
        return time.time() * 1000

    def start(self):
        """
        Starts the alternator effect, resetting the state and visibility.

        This method initializes the count and sets the start time for the alternation.
        """
        self.__running = True
        self.__visible = False
        self.__count = 0
        self.__started_at = self.get_current_milli_time()

    def get_visible(self) -> bool:
        """
        Checks the current visibility state.

        Returns:
            bool: True if visible, or if the alternator is not running; otherwise False.
        """
        return self.__visible or (not self.__running)

    def update(self):
        """
        Updates the alternator's state based on the elapsed time.

        This method toggles the visibility if the specified delay has passed and the
        maximum toggle count has not been reached.
        """
        if not self.__running:
            return

        diff: float = self.get_current_milli_time() - self.__started_at

        if diff > self.__delay_ms:
            if self.__count >= self.__max_count + 1:
                self.__running = False

            self.__started_at = self.get_current_milli_time()
            self.__count += 1
            self.__visible = not self.__visible

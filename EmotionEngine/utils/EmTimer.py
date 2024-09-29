import time


class EmTimer:
    """
    A class that represents a timer which executes a callback after a specified delay.

    This timer can be started, updated, and will invoke a provided callback function
    when the specified delay in milliseconds has elapsed.
    """

    def __init__(self, delay_ms: float, callback_on_finished: any) -> None:
        """
        Initializes the timer with a specified delay and a callback function.

        Args:
            delay_ms (float): The delay in milliseconds after which the callback will be executed.
            callback_on_finished (callable): The function to be called when the timer finishes.
        """
        self.__started = False
        self.__finished = False
        self.__delay_ms = delay_ms

        self.__started_at = None
        self.__callback_on_finished = callback_on_finished

    def get_current_milli_time(self):
        """
        Gets the current time in milliseconds.

        Returns:
            float: The current time in milliseconds since the epoch.
        """
        return time.time() * 1000

    def start(self):
        """
        Starts the timer and resets its state.

        This method sets the timer to started, marks it as unfinished,
        and records the starting time.
        """
        self.__started = True
        self.__finished = False
        self.__started_at = self.get_current_milli_time()

    def update(self):
        """
        Updates the timer's state and invokes the callback if the timer has finished.

        This method checks if the timer has started and is not finished,
        and if the specified delay has elapsed, it marks the timer as finished
        and calls the provided callback function.
        """
        if self.__started and not self.__finished:
            diff: float = self.get_current_milli_time() - self.__started_at

            if diff >= self.__delay_ms:
                self.__finished = True
                self.__callback_on_finished()

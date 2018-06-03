from enum import Enum
from datetime import datetime
from functools import wraps
from threading import Lock
from typing import Callable, Any


class State(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3


class CircuitBreaker:

    def __init__(self,
                 failure_threshold: int = 5,
                 recovery_time: int = 3,
                 failure_exception_type: Callable[..., Exception] = Exception) -> None:
        self._failure_threshold: int = failure_threshold
        self._recover_time_seconds: int = recovery_time
        self._failure_exception_type: Callable[..., Exception] = failure_exception_type
        self._state: State = State.CLOSED
        self._tripped_time: datetime = datetime.utcnow()
        self._failure_count: int = 0
        self._lock: Lock = Lock()

    def __call__(self, target_fn: Callable) -> Callable:
        return self.decorate(target_fn)

    def decorate(self, target_fn: Callable) -> Callable:
        @wraps(target_fn)
        def wrapper(*args, **kwargs):
            return self.__apply(target_fn, *args, **kwargs)

        return wrapper

    def __apply(self, target_fn: Callable, *args, **kwargs) -> Any:
        if self.__is_open_state_expired():
            self.__change_state(State.CLOSED)

        if self._state == State.OPEN:
            raise self._failure_exception_type()
        try:
            result = target_fn(*args, *kwargs)
        except self._failure_exception_type:
            self.__failure_procedure()
            raise

        self.__success_procedure()
        return result

    def __is_open_state_expired(self) -> bool:
        return (datetime.utcnow() - self._tripped_time).seconds >= self._recover_time_seconds

    def __success_procedure(self) -> None:
        self.__change_state(State.CLOSED)
        self.__reset_failure_count()

    def __failure_procedure(self) -> None:
        if self._failure_count > self._failure_threshold:
            self.__change_state(State.OPEN)
        self.__increment_failures()

    def __change_state(self, new_state: State) -> None:
        with self._lock:
            self._state = new_state

    def __increment_failures(self) -> None:
        with self._lock:
            self._failure_count += 1

    def __reset_failure_count(self) -> None:
        with self._lock:
            self._failure_count = 0

from circuitBreaker import CircuitBreaker
import time
import unittest


class TestException(Exception):
    pass


class TestCB(unittest.TestCase):
    breaker = CircuitBreaker(failure_exception_type=TestException, recovery_time=3)

    @breaker
    def fail_operation(self):
        raise TestException()

    @breaker
    def success_operation(self):
        pass

    def test_basic_functionality(self):
        self.success_operation()

        for i in range(8):
            try:
                self.fail_operation()
            except TestException:
                pass

        with self.assertRaises(TestException):
            self.success_operation()

        time.sleep(5)
        try:
            self.success_operation()
        except(TestException):
            self.assertTrue(False, "this operation should succeed after waiting on the circuit timeout")


if __name__ == "__main__":
    unittest.main()

# python-circuit-breaker
Implements a basic and easy to use decorator that applies the Circuit Breaker design pattern to the decorated method.

## Key Feature
The circuit breaker object that is created is statefull across usaged. This means that you can hold a single circuit breaker instance in a provider and apply the same state to all calls in the provider. In short this means that we can have multiple methods on the same circuit. This is useful when there are multiple calls to a single provider (say Github for example) we may want all of our calls to Github to be on the same circuit instead of each type of call to github being independent.

## Usage
Usage is simple. import the CircuitBreaker class, construct an object (instances of CircuitBreaker are callable), and decorate any methods you want to be on the circuit.

```Python
from circuitBreaker import CircuitBreaker

class ExceptionToBreakOn(Exception):
  pass

# Create the circuit with configuration
circuit = CircuitBreaker(failure_threshold=10, recovery_time=3, failure_exception_type=ExceptionToBreakOn)

@circuit
def fn1():
  # do stuff
  pass
  
@circuit
def fn2():
  # do stuff
  pass

@CircuitBreaker()
def fn3():
  # do stuff
  pass
```

In the example above fn1 and fn2 are on the same circuit. Failures in fn2 will affect fn1. This may not be desired so it is good to be aware. This circuit is configured to break on exceptions of type ExceptionToBreakOn. This allows you to only count certain exceptions (such as service unavailable) to the breaking threshold


Fn3 is on a separate circuit that is constructed with default configuration. The default configuration will break with the Exception type

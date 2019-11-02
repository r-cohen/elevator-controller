## Python module for controlling and managing the state of elevators.

### Running & editing the test script
The `main.py` script instantiates the controller and runs a few test by adding requests,
and prints out a debug string at a 1 second refresh rate indicating the state of the elevators.
Each `Elevator` instantiated by the controller has a dedicated thread created for processing requests
and simulating the movement of the elevator (see the `Elevator` class for details).
The `Controller` is responsible for determining which elevator should handle a request,
and each `Elevator` holds its own pending requests list.

### Sample usage

```python
elevators_count = 3
controller = ElevatorController.Controller(3)
```

### Debug helper string

```python
debug_string = controller.elevators_state_debug_string()
```

"""Main entry point for testing the elevator-controller module"""
import time
import sys
import os
import thread
from elevatorcontroller import ElevatorController


def _long_running():
    """prevent calling process to terminate"""
    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        sys.exit(0)


def main():
    """Main entry point of the elevator-controller test"""
    elevators_count = 3  # number of elevators which the controller will handle
    controller = ElevatorController.Controller(elevators_count)

    thread.start_new_thread(_print_elevators_states, (controller, 1, ))
    time.sleep(1)

    assert controller.add_request(0, 2)  # simple test adding a request from floor 0 to 2
    assert not controller.add_request(0, 2)  # request will be ignored because already pending
    assert not controller.add_request(3, 3)  # request will be ignored for same floors
    assert controller.add_request(4, 0)  # test someone going down
    time.sleep(1)
    assert controller.add_request(2, 3)  # request added after elevator is moving

    _long_running()


def _print_elevators_states(controller, refresh_rate_seconds):
    """recursive function outputing the state of elevators"""
    os.system("clear")  # replace with `cls` on windows
    print controller.elevators_state_debug_string()
    time.sleep(refresh_rate_seconds)
    _print_elevators_states(controller, refresh_rate_seconds)


if __name__ == '__main__':
    main()




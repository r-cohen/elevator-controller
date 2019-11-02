import thread
import time
from ElevatorState import State
from ElevatorDirection import Direction


class Elevator(object):
    def __init__(self, index):
        self.id = index
        self.current_floor = 0
        self.state = State.AT_FLOOR
        self.direction = Direction.UP
        self.pending_requests = []  # list of pending requests
        self.destination_floors = []  # list of floors that the elevator must stop at while going up or down
        thread.start_new_thread(self._move_elevator, ())

    def add_request(self, request):
        """adds a request to list of pending requests"""
        self.pending_requests.append(request)

    def _process_pending_requests(self):
        """
        pops items from the pending requests
        and adds them to the destinations_floors
        """
        to_remove = []
        for request in self.pending_requests:
            if (self.direction == Direction.UP and request.going_up()) or \
                    (self.direction == Direction.DOWN and request.going_down()):
                if request.from_floor not in self.destination_floors:
                    self.destination_floors.append(request.from_floor)
                if request.to_floor not in self.destination_floors:
                    self.destination_floors.append(request.to_floor)
                to_remove.append(request)
        for request in to_remove:
            self.pending_requests.remove(request)

    def _move_elevator(self):
        """simulates moving the elevator to the destination floors"""
        self._process_pending_requests()

        if self.state == State.MOVING:
            #  increment/decrement floor
            self.current_floor += 1 if self.direction == Direction.UP else -1

            if self.current_floor in self.destination_floors:
                # we should stop here
                self.state = State.AT_FLOOR
                self.destination_floors.remove(self.current_floor)
                time.sleep(10)
            else:  # keep on moving
                time.sleep(2)
        else:  # state == State.AT_FLOOR
            if len(self.destination_floors) == 0:
                #  here we can toggle direction, looking for requests
                self._toggle_direction()
            else:  # there are destinations, got to get moving
                #  should we toggle direction?
                should_toggle_direction = True
                for floor in self.destination_floors:
                    if (self.direction == Direction.UP and floor > self.current_floor) or \
                            (self.direction == Direction.DOWN and floor < self.current_floor):
                        should_toggle_direction = False
                        break
                if should_toggle_direction:
                    self._toggle_direction()
                self.state = State.MOVING
            time.sleep(1)

        self._move_elevator()

    def _toggle_direction(self):
        self.direction = Direction.UP if self.direction == Direction.DOWN else Direction.DOWN

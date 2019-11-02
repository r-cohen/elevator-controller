from random import randrange
from GoToFloorRequest import GoToFloorRequestFactory
from Elevator import Elevator
from ElevatorDirection import Direction
from ElevatorState import State


class Controller(object):
    """Handles incoming go to floor requests and manages elevators states"""
    def __init__(self, elevators_count):
        if elevators_count <= 0:
            raise Exception("elevators count must be greater than 0")
        self.elevators_count = elevators_count
        self.elevators = {}  # dictionary of elevators and their state
        #  populate elevators
        for i in range(self.elevators_count):
            self.elevators[i] = Elevator(i)
        #  keep instance of factory for building requests
        self._request_factory = GoToFloorRequestFactory()

    def add_request(self, from_floor, to_floor):
        """Adds a request to go from a floor to another floor to an elevator's pending requests"""
        try:
            request = self._request_factory.build(from_floor, to_floor)
            if self._is_request_already_pending(request):
                #  this request is already pending in an elevator
                return False
            elevator = self._get_best_elevator_for_request(request)
            elevator.add_request(request)
            return True
        except ValueError:
            return False

    def _is_request_already_pending(self, request):
        """Checks if this request is already pending in an elevator's pending requests"""
        for _, elevator in self.elevators.items():
            for pending_request in elevator.pending_requests:
                if pending_request.equals(request):
                    return True
        return False

    def _get_best_elevator_for_request(self, request):
        """Determins the best elevator for this request"""
        elevators_candidates_scores = {}  # index of elevators found for that request, and their score

        if request.going_up():
            # look for an elevator which is located on a floor beneath request from_floor (or equal to from_floor)
            # AND which is going up, so it will stop at that from_floor of the request on the way up
            for _, elevator in self.elevators.items():
                if elevator.current_floor <= request.from_floor and elevator.direction == Direction.UP:
                    elevators_candidates_scores[elevator.id] = request.from_floor - elevator.current_floor
        else:  # request going down
            # look for an elevator which is located above request from_floor
            # AND which is going down, so it will stop at that from_floor of the request on the way down
            for _, elevator in self.elevators.items():
                if elevator.current_floor > request.from_floor and elevator.direction == Direction.DOWN:
                    elevators_candidates_scores[elevator.id] = elevator.current_floor - request.from_floor

        # many possible elevators, the closest to the from_floor of the request is the best score
        best_score = 1000  # could be equal to the max number of floors in the building
        best_elevator_id = -1
        for i, score in elevators_candidates_scores.items():
            if score < best_score:
                best_score = score
                best_elevator_id = i

        if best_elevator_id >= 0:
            return self.elevators[best_elevator_id]

        return self.elevators[randrange(self.elevators_count)]  # by default chose a random elevator

    def elevators_state_debug_string(self):
        """returns a debug string displaying the elevators states"""
        debug_string = ""
        for i, elevator in self.elevators.items():
            debug_string += "elevator {0}:\t".format(i)
            debug_string += "floor {0}\t".format(elevator.current_floor)
            debug_string += "requests={0}\t".format(len(elevator.pending_requests))
            debug_string += "destinations={0}\t".format(len(elevator.destination_floors))
            direction = "up" if elevator.direction == Direction.UP else "down"
            debug_string += "going {0}\t".format(direction)
            state = "moving" if elevator.state == State.MOVING else "at floor"
            debug_string += "{0}\t".format(state)
            debug_string += "\n"
        return debug_string

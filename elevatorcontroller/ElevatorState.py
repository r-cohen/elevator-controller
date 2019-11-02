class State(object):
    """Enumeration defining the list of moving states in which an elevator can be"""
    AT_FLOOR = 0  # the elevator is stopped at a floor waiting for passengers to go in/out
    MOVING = 1  # the elevator is moving

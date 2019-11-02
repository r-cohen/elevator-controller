class GoToFloorRequest(object):
    def __init__(self, from_floor, to_floor):
        self.from_floor = from_floor
        self.to_floor = to_floor

    def equals(self, request):
        return self.from_floor == request.from_floor and self.to_floor == request.to_floor

    def going_up(self):
        return self.to_floor > self.from_floor

    def going_down(self):
        return self.to_floor < self.from_floor


class GoToFloorRequestFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def build(from_floor, to_floor):
        if from_floor == to_floor:
            raise ValueError("from_floor and to_floor cannot be identical")
        return GoToFloorRequest(from_floor, to_floor)

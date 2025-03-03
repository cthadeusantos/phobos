from source.cable import Cable

class Edge:
    def __init__(self, weight=0, distance=0, **kwargs):
        """ Constructor

        Returns:
            None
        """
        cable = kwargs.get('cable') if kwargs and 'cable' in kwargs else None
        self.weight = weight
        self.distance = distance
        self.cable = cable
        self.installation = 0

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("Weight needs to be a number")
        if value < 0:
            raise ValueError("Weight can be a non negative value.")
        self._weight = float(value)

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TypeError("Weight needs to be a number")
        if value < 0:
            raise ValueError("Weight can be a non negative value.")
        self._distance = float(value)

    def __str__(self):
        return f"Edge: weight={self.weight}, distance={self.distance}, cable={self.cable}"
    
    @property
    def cable(self):
        return self._cable

    @cable.setter
    def cable(self, value):
        if value is not None:
            if not isinstance(value, Cable):
                raise TypeError("Cable must to be a cable instance!")
        else:
            value = Cable()
        # if value < 0:
        #     raise ValueError("Weight can be a non negative value.")
        self._cable = value
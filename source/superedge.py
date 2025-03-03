from source.cable import Cable
from source.edge import Edge

class Superedge(Edge):
    def __init__(self, weight=0, distance=0, **kwargs):
        """ Constructor

        Returns:
            None
        """
        cable = kwargs.get('cable') if kwargs and 'cable' in kwargs else None
        installation = kwargs.get('installation') if kwargs and 'installation' in kwargs else None
        distributed_type = kwargs.get('distributed') if kwargs and 'distributed' in kwargs else 0
        total = kwargs.get('total') if kwargs and 'total' in kwargs else None
        super().__init__(weight, distance)
        self.cable = cable
        self.installation = installation
        self.distributed_type = distributed_type
        #self.total = total
    
    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        if value is not None:
            if not (isinstance(value, int) or isinstance(value, float)):
                raise TypeError("Total needs to be a number")
            if value < 0:
                raise ValueError("Total can be a non negative value.")
            value = float(value)
        self._total = value
    
    @property
    def cable(self):
        return self._cable

    @cable.setter
    def cable(self, value):
        if value is not None:
            if value is not None:
                if not isinstance(value, Cable):
                    raise TypeError("Cable must to be a cable instance!")
            else:
                value = Cable()
        # if value < 0:
        #     raise ValueError("Weight can be a non negative value.")
        self._cable = value


    @property
    def installation(self):
        return self._installation

    @installation.setter
    def installation(self, value):
        if value is not None:
            if not (isinstance(value, int)):
                raise TypeError("Installation needs to be an integer number")
            if value < 0:
                raise ValueError("Installation can be a non negative value.")
        self._installation = value

    
    def __str__(self):
        return f"Edge: weight={self.weight}, distance={self.distance}, cable={self.cable}"
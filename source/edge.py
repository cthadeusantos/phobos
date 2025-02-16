class Edge:
    def __init__(self, weight=0, distance=0, **kwargs):
        cable = kwargs.get('cable') if kwargs and 'cable' in kwargs else None

        if weight < 0 or distance < 0 or isinstance(weight, str) or isinstance(distance, str):
            raise ValueError("Invalid input!")
        
        self.weight = weight
        self.distance = distance
        self.cable = cable

    def __str__(self):
        return f"Edge: weight={self.weight}, distance={self.distance}, cable={self.cable}"
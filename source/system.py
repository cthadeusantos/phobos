from math import sqrt

from source.graph import Graph

class System(Graph):

    def __init__(self, root=None):
        """ Constructor

        Returns:
            None
        """
        super().__init__()
        self.root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value=None):
        if value is not None:
            if not isinstance(value, (int, str)):
                raise TypeError("Invalid root value")

            if isinstance(value, int) and value < 0:
                raise ValueError("root must be a non-negative integer.")

        self._root = value

    def unbalance(self, Ia=None, Ib=None, Ic=None):
        if Ic is not None:  # Ver documento cemig nd3_1_000001p.pdf
            des3F_percentual= ((3 * sqrt((Ia**2 + Ib**2 + Ic**2) -
                            (Ia * Ib + Ib * Ic + Ic * Ia))
                            )/ (Ia + Ib + Ic)) * 100
        else:   # Ver documento cemig nd3_1_000001p.pdf
            des1F_percentual = (2 * (Ia - Ib) / (Ia + Ib)) * 100

    def __str__(self):
        return f"System: {self.root}"
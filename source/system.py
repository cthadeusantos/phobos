from math import sqrt

from source.graph import Graph

class System(Graph):

    def __init__(self, root=None):
        """ Constructor

        Returns:
            None
        """
        self.root = root

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        if not (isinstance(value, int) or isinstance(value, str)):
            raise TypeError("root needs to be an integer")
        if value < 0:
            raise ValueError("root can be a non negative value.")
        self._root = float(value)

    def unbalance(self, Ia=None, Ib=None, Ic=None):
        if Ic is not None:  # Ver documento cemig nd3_1_000001p.pdf
            des3F_percentual= ((3 * sqrt((Ia**2 + Ib**2 + Ic**2) -
                            (Ia * Ib + Ib * Ic + Ic * Ia))
                            )/ (Ia + Ib + Ic)) * 100
        else:   # Ver documento cemig nd3_1_000001p.pdf
            des1F_percentual = (2 * (Ia - Ib) / (Ia + Ib)) * 100
class ElectricalHandler:
    def __init__(self, vline=0, vphase=0):
        self._vline = vline
        self._vphase = vphase

    @property
    def vline(self):
        return self._vline

    @vline.setter
    def vline(self, value=0.0):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid value for vline")

            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("vline must be a non-negative integer.")
        self._vline = value

    @property
    def vphase(self):
        return self._vphase

    @vphase.setter
    def vphase(self, value=0.0):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid value for vphase")

            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("vline must be a non-negative integer.")
        self._vphase = value

    # def unbalance(self, Ia=None, Ib=None, Ic=None):
    #     if Ic is not None:  # Ver documento cemig nd3_1_000001p.pdf
    #         des3F_percentual= ((3 * sqrt((Ia**2 + Ib**2 + Ic**2) -
    #                         (Ia * Ib + Ib * Ic + Ic * Ia))
    #                         )/ (Ia + Ib + Ic)) * 100
    #     else:   # Ver documento cemig nd3_1_000001p.pdf
    #         des1F_percentual = (2 * (Ia - Ib) / (Ia + Ib)) * 100
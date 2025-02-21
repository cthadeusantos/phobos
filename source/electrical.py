class ElectricalHandler:
    def __init__(self, vpp=0, vpn=0):
        self._vpp = vpp
        self._vpn = vpn

    @property
    def vpp(self):
        return self._vpp

    @vpp.setter
    def vpp(self, value=0.0):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid value for Vpp")

            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Vpp must be a non-negative integer.")
        self._vpp = value

    @property
    def vpn(self):
        return self._vpn

    @vpn.setter
    def vpn(self, value=0.0):
        if value is not None:
            if not isinstance(value, (int, float)):
                raise TypeError("Invalid value for Vpn")

            if isinstance(value, (int, float)) and value < 0:
                raise ValueError("Vpp must be a non-negative integer.")
        self._vpn = value

    # def unbalance(self, Ia=None, Ib=None, Ic=None):
    #     if Ic is not None:  # Ver documento cemig nd3_1_000001p.pdf
    #         des3F_percentual= ((3 * sqrt((Ia**2 + Ib**2 + Ic**2) -
    #                         (Ia * Ib + Ib * Ic + Ic * Ia))
    #                         )/ (Ia + Ib + Ic)) * 100
    #     else:   # Ver documento cemig nd3_1_000001p.pdf
    #         des1F_percentual = (2 * (Ia - Ib) / (Ia + Ib)) * 100
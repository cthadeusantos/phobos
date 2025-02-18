from random import randint

class Cable:
    def __init__(self, tipo=None, resistance=0.0, reactance=0.0):
        """ Constructor

        Returns:
            None
        """
        self.tipo = tipo  # Usa o setter para validar o tipo
        self.resistance = resistance # Usa o setter para validar e converter
        self.reactance = reactance # Converte diretamente, sem necessidade de setter

    @property
    def tipo(self):
        return self._tipo  # Retorna o atributo "privado"

    @tipo.setter
    def tipo(self, value):
        if not isinstance(value, str) and value is not None:
            raise TypeError("Type must be a string.")
        if value is None:
            self._tipo = str(hex(randint(1,16777215))).replace('0x','')
        else:
            self._tipo = value  # Define o atributo "privado"

    @property
    def resistance(self):
        return self._resistance  # Retorna o atributo "privado"

    @resistance.setter
    def resistance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Resistance must be a number (int or float).")
        if value < 0:
            raise ValueError("Resistance must be non-negative.")
        self._resistance = float(value)  # Define o atributo "privado"

    @property
    def reactance(self):
        return self._reactance

    @reactance.setter
    def reactance(self, value):
        if not isinstance(value, (int, float)):  # Aceita int ou float
            raise TypeError("Reactance must be a number (int or float).")
        if value < 0:
            raise ValueError("Reactance must be non-negative.")
        self._reactance = float(value) # Armazena sempre como float

    def __str__(self):
        return f"Cable: Type={self.tipo}, Resistance={self.resistance}, Reactance={self.reactance}"
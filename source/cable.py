class Cable:
    def __init__(self, tipo, resistance):
        self.tipo = tipo
        self.resistance = resistance

    def __str__(self):
        return f"Cable: Type={self.tipo}, resistance={self.resistance}"
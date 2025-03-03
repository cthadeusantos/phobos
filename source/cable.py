import math

class Cable:
    #def __init__(self, tipo=None, resistanceCA=0.0, reactance=0.0):
    def __init__(self, rcc=0.0, xc=0.0, rca=0.0, xl=0.0, parameters=None, id=0):
        """ Constructor

        Returns:
            None
        """
        #self.tipo = tipo  # Usa o setter para validar o tipo
        self.id = id
        self.resistanceCC = rca # Usa o setter para validar e converter
        self.capacitance = xc # Usa o setter para validar e converter
        self.resistanceCA = rca # Usa o setter para validar e converter
        self.reactance = xl # Converte diretamente, sem necessidade de setter
        self.parameters = {}
        if parameters is None:
            self.reset_parameters()
        else:
            self.set_parameters(parameters)

    # @property
    # def tipo(self):
    #     return self._tipo  # Retorna o atributo "privado"

    # @tipo.setter
    # def tipo(self, value):
    #     if not isinstance(value, str) and value is not None:
    #         raise TypeError("Type must be a string.")
    #     if value is None:
    #         self._tipo = str(hex(randint(1,16777215))).replace('0x','')
    #     else:
    #         self._tipo = value  # Define o atributo "privado"

    @property
    def id(self):
        return self._id  # Retorna o atributo "privado"

    @id.setter
    def id(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("resistanceCC must be a number (int or float).")
            if value < 0:
                raise ValueError("id must be greater than zero.")
        self._id = value  # Define o atributo "privado"

    @property
    def resistanceCC(self):
        return self._resistanceCC  # Retorna o atributo "privado"

    @resistanceCC.setter
    def resistanceCC(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("resistanceCC must be a number (int or float).")
        if value < 0:
            raise ValueError("resistanceCC must be non-negative.")
        self._resistanceCC = float(value)  # Define o atributo "privado"

    @property
    def capacitance(self):
        return self._capacitance  # Retorna o atributo "privado"

    @capacitance.setter
    def capacitance(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("resistanceCC must be a number (int or float).")
        if value < 0:
            raise ValueError("resistanceCC must be non-negative.")
        self._capacitance = float(value)  # Define o atributo "privado"

    @property
    def resistanceCA(self):
        return self._resistanceCA  # Retorna o atributo "privado"

    @resistanceCA.setter
    def resistanceCA(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("resistanceCA must be a number (int or float).")
        if value < 0:
            raise ValueError("resistanceCA must be non-negative.")
        self._resistanceCA = float(value)  # Define o atributo "privado"

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

    def impedance(self, power_factor=1.0):
        if not isinstance(power_factor, (int, float)):  # Aceita int ou float
            raise TypeError("Power factor must be a number (int or float).")
        if power_factor < 0 or power_factor > 1:
            raise ValueError("The power factor value must be between 0 and 1.")
        angle = math.acos(power_factor)
        cos_phi = math.cos(angle)
        sin_phi = math.sin(angle)
        return self.resistanceCA * cos_phi + self.reactance * sin_phi

    def pf_angle_degree(self, power_factor=1.0):
        if not isinstance(power_factor, (int, float)):  # Aceita int ou float
            raise TypeError("Power factor must be a number (int or float).")
        if power_factor < 0 or power_factor > 1:
            raise ValueError("The power factor value must be between 0 and 1.")
        angle = round(math.degrees(math.acos(power_factor)), 2)
        return angle

    def setting(self, cable_tuple):
        data, parameters = cable_tuple
        self.set_data(data)
        self.set_parameters(parameters)

    def set_data(self, data=(None, None, None, None, None)):
        self.id, self.resistanceCC, self.capacitance,self.resistanceCA, self.reactance = data

    def set_parameters(self, parameters=None):
        if not isinstance(parameters, dict):
            raise TypeError("Parameters must be a dictionary!")

        required_keys = ['gauge', 'conductor', 'description', 'manufacture', 'temperature', 'voltage']

        if len(parameters) != len(required_keys):
            raise ValueError("Invalid number of parameters!")

        for key in required_keys:
            if parameters.get(key) is None:
                raise ValueError(f"Parameter '{key}' is missing or None.")
        
        self.parameters['gauge'] = parameters['gauge']
        self.parameters['conductor'] = parameters['conductor']
        self.parameters['description'] = parameters['description']
        self.parameters['manufacture'] = parameters['manufacture']
        self.parameters['temperature'] = parameters['temperature']
        self.parameters['voltage'] = parameters['voltage']

    def reset_parameters(self):
        self.parameters = {
            'gauge': (None, None),
            'conductor': (None, None),
            'description': (None, None),
            'manufacture': (None, None),
            'temperature': (None, None),
            'voltage': (None, None),
            }
        
    def get_parameter(self, parameter=None, tipo=None):
        """
        parameter: A string with parameter name
        tipo: A string with words 'id' or 'tag'
        """
        if parameter is None:
            raise ValueError('Parameter name not assign!')
        if parameter not in self.parameters.keys():
            raise AttributeError("Invalid parameter name!")
        if tipo is None:
            raise ValueError('Type name not assign!')
        if tipo not in ['id', 'tag']:
            raise ValueError('Invalid type assign!')
        value = 0 if tipo == 'id' else 1
        #for parameter in self.parameters.keys():
        if parameter in self.parameters:
            return self.parameters[parameter][value]
        raise ValueError('Invalid parameter name!')
    
    def get_rcc(self):
        return self.resistanceCC
    
    def get_rca(self):
        return self.resistanceCA
    
    def get_xl(self):
        return self.reactance
    
    def get_xc(self):
        return self.capacitance

    def __str__(self):
        return f"Cable: Type={self.get_parameter('conductor', 'tag')}, resistanceCA={self.resistanceCA}, Reactance={self.reactance}"
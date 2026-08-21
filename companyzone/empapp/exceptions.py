class NegativeValueError(Exception):
    def __init__(self, value_name = ''):
        full_msg = "Error: " + value_name + " cannot be Negative Value."
        super().__init__(full_msg)

class ZeroValueError(Exception):
    def __init__(self, value_name = ''):
        full_msg = "Error: " + value_name + " cannot be Zero."
        super().__init__(full_msg)

_warnings = []
_header = ""

class Warning:
    def __init__(self, message, header):
        self.message = message
        self.header = header 

    def out(self) -> str:
        return f"########## Warning ##########\n"\
            f"{self.header}\n"\
            f"{self.message}\n"\
            "#############################"
        
def add_warning(message):
    _warnings.append(Warning(message, _header))

def set_header(header):
    _header = header

def flush():
    pass
    # for warn in _warnings:
    #     print(warn.out())
    # _warnings.clear()
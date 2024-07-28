import json
import re

def correoValido(email):
    regex = r'^[a-zA-Z0-9][a-zA-Z0-9._]{3,}[a-zA-Z0-9]@(hotmail\.com|gmail\.com|outlook\.com|epn\.edu\.ec)$'

    if re.match(regex, email):
        return True
    else:
        return False

import random
from string import ascii_uppercase



rooms = {}
def generate_unique_code(length):
    while True:
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            rooms[code] = True
            break
    return code



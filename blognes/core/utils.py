def generate_id():
    number = 0
    while True:
        yield number
        number += 1

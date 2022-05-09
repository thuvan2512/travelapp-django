import random
def random_for_confirm_code():
    num = random.randrange(1, 10000)
    num_with_zeros = '{:04}'.format(num)
    return num_with_zeros
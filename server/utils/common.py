import random


def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(to, subject, body):
    # TODO
    print(to, subject, body)

if __name__ == '__main__':
    print(generate_otp())
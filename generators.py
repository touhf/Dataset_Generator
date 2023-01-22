import names
import random
import string
import rcoc


def get_random_name(arg1, arg2):
    return names.get_full_name()


def get_random_phone_number(arg1, arg2):
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)

    last = str(random.randint(1, 9998)).zfill(4)
    while last in ["1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888"]:
        last = str(random.randint(1, 9998)).zfill(4)

    return "{}-{}-{}".format(first, second, last)


def get_random_email(arg1, arg2):
    name = "".join(
        random.choice(string.ascii_letters) for i in range(random.randint(6, 12))
    )
    return name + "@gmail.com"


def get_random_number(low, high):
    return random.randint(low, high)


def get_random_city(arg1, arg2):
    res = rcoc.get_random_city_by_country(arg1)
    if res.strip() == "":
        return rcoc.get_random_city()
    else:
        return res


def get_random_country(arg1, arg2):
    return rcoc.get_random_country()


def get_random_password(arg1, arg2):
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for i in range(random.randint(8, 16)))
    return password


def get_all_countries():
    return rcoc.get_all_countries()

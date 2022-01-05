import string
import random


class Slug():

    def slug():

        # создаем пустой массив
        base_arr = []
        # добавляем в массив цифры
        for i in list(string.digits):
            base_arr.append(i)

        # добавляем символы нижнего регистра
        for i in list(string.ascii_lowercase):
            base_arr.append(i)

        # добавляем симоволы верхнего регистра
        for i in list(string.ascii_uppercase):
            base_arr.append(i)

        slug = []
        for i in range(random.randint(1, 7)):
            slug.append(random.choice(base_arr))

        return ''.join(slug)


class SecureSlug():

    def secure_slug():

        # создаем пустой массив
        base_arr = []
        # добавляем в массив цифры
        for i in list(string.digits):
            base_arr.append(i)

        # добавляем символы нижнего регистра
        for i in list(string.ascii_lowercase):
            base_arr.append(i)

        # добавляем символы верхнего регистра
        for i in list(string.ascii_uppercase):
            base_arr.append(i)

        secure_slug = []
        for i in range(20):
            secure_slug.append(random.choice(base_arr))

        return ''.join(secure_slug)

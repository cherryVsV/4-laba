from hashlib import md5


class User(object):
    def __init__(self, login, password):
        self._login = login
        self._password = self._hash(password)

    def _hash(self, string):
        string = string.encode()
        string_hash = md5(string)
        string_hash.update(string_hash.digest()[1::3])
        return string_hash.hexdigest()

    def auth(self, login, password):
        return (self._login == login and
                self._password == self._hash(password))

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._password
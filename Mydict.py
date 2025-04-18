import bcrypt

class MyDict:
    __values: list
    __keys: list
    
    def __init__(self):
        self.__values = []
        self.__keys = []
    
    def my_hash(self, x):
        if isinstance(x, str):
            x = x.encode('utf-8')
        elif isinstance(x, (int, float)):
            x = str(x).encode('utf-8')
        elif not isinstance(x, bytes):
            x = str(x).encode('utf-8')

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(x, salt)
    
    def __getitem__(self, key):
        for i, my_key in enumerate(self.__keys):
            if bcrypt.checkpw(self._encode_key(key), self.my_hash(my_key)):
                return self.__values[i]
        raise KeyError(key)
    
    def __setitem__(self, key, value):
        for i, my_key in enumerate(self.__keys):
            if bcrypt.checkpw(self._encode_key(key), self.my_hash(my_key)):
                self.__values[i] = value
                return
        self.__keys.append(key)
        self.__values.append(value)
    
    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def _encode_key(self, key):
        if isinstance(key, str):
            return key.encode('utf-8')
        return str(key).encode('utf-8')
    
    def __len__(self):
        return len(self.__values)
    
    def __repr__(self):
        items = []
        for i, key in enumerate(self.__keys):
            items.append(f"{key!r}: {self.__values[i]!r}")
        return "{" + ", ".join(items) + "}"
    
    def clear(self):
        self.__values = []
        self.__keys = []
    
    def copy(self):
        new_dict = MyDict()
        new_dict.__keys = self.__keys.copy()
        new_dict.__values = self.__values.copy()
        return new_dict
    
    @classmethod
    def fromkeys(cls, seq, value=None):
        new_dict = cls()
        for key in seq:
            new_dict[key] = value
        return new_dict
    
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self):
        return list(zip(self.__keys, self.__values))
    
    def keys(self):
        return self.__keys.copy()
    
    def pop(self, key, default=KeyError):
        for i, my_key in enumerate(self.__keys):
            if bcrypt.checkpw(self._encode_key(key), self.my_hash(my_key)):
                value = self.__values.pop(i)
                self.__keys.pop(i)
                return value
        if default is KeyError:
            raise KeyError(key)
        return default
    
    def popitem(self):
        if not self.__keys:
            raise KeyError("popitem(): dictionary is empty")
        return (self.__keys.pop(), self.__values.pop())
    
    def setdefault(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default
    
    def update(self, other=None, **kwargs):
        if other is not None:
            if hasattr(other, "items"):
                for key, value in other.items():
                    self[key] = value
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value
    
    def values(self):
        return self.__values.copy()
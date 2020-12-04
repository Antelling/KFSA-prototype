from enum import IntEnum

class AttTypes(IntEnum):
    absent = 1
    partial = 2
    online = 3
    present = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
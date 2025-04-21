from enum import Enum


IP_REGEX = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"


class EnumChoices(Enum):
    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    @classmethod
    def values(cls):
        """Returns list of enum values"""
        return [key.value for key in cls]

    @classmethod
    def all_choice_values(cls):
        return [key.value for key in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def key_by_value(cls, value):
        if cls.has_value(value):
            return cls._value2member_map_.get(value).name
        return None

    @classmethod
    def names(cls):
        """Returns list of enum names"""
        return [key.name for key in cls]

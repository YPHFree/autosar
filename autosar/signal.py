from autosar.base import splitRef
from autosar.element import Element
import sys
import enum


class ISignal(Element):
    class ISignalType(enum.Enum):
        PRIMITIVE = 0

    def __init__(self, name, data_type_policy=None, type=None, initial_value=None, desc=None, parent=None):
        super().__init__(name, parent)
        self.desc = desc
        self.type = type
        self.parent = parent
        self.initial_value = initial_value
        self.data_type_policy = data_type_policy


class SystemSignal(Element):
    def __init__(self, name, desc=None, parent=None):
        super().__init__(name, parent)
        self.desc = desc
        self.parent = parent

    def asdict(self):
        data = {'type': self.__class__.__name__, 'name': self.name,
                'dataTypeRef': self.dataTypeRef,
                'initValueRef': self.initValueRef,
                'length': self.length
                }
        if self.desc is not None: data['desc'] = self.desc
        return data


class SystemSignalGroup(Element):
    def __init__(self, name, systemSignalRefs=None, parent=None):
        super().__init__(name, parent)
        if isinstance(systemSignalRefs, list):
            self.systemSignalRefs = systemSignalRefs
        else:
            self.systemSignalRefs = []

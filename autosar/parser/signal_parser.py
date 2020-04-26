from logging import exception

from autosar.base import parseXMLFile,splitRef,parseTextNode,parseIntNode
from autosar.signal import *
from autosar.parser.parser_base import ElementParser

class SignalParser(ElementParser):
    def __init__(self,version=3):
        self.version=version

        if self.version >= 3.0 and self.version < 4.0:
            self.switcher = {'SYSTEM-SIGNAL': self.parseSystemSignal,
                             'SYSTEM-SIGNAL-GROUP': self.parseSystemSignalGroup
                             }
        elif self.version >= 4.0:
            self.switcher = {'SYSTEM-SIGNAL': self.parseSystemSignal,
                             'I-SIGNAL': self.parseISignal,
                             'SYSTEM-SIGNAL-GROUP': self.parseSystemSignalGroup
                             }

    def getSupportedTags(self):
        return self.switcher.keys()

    def parseElement(self, xmlElement, parent = None):
        parseFunc = self.switcher.get(xmlElement.tag)
        if parseFunc is not None:
            return parseFunc(xmlElement,parent)
        else:
            return None

    def parseISignal(self, xmlRoot, parent=None):
        """
        parses <I-SIGNAL>
        """
        name, desc, data_type_policy, signal_type, length, system_signal_refs, initial_value = None, None, None, None, None, None, None
        for elem in xmlRoot.findall('./*'):
            if elem.tag == 'SHORT-NAME':
                name = parseTextNode(elem)
            elif elem.tag == 'LONG-NAME':
                pass
            elif elem.tag == 'LENGTH':
                length = int(elem.text)
            elif elem.tag == 'INIT-VALUE':
                initial_value_elem = elem.find('NUMERICAL-VALUE-SPECIFICATION/VALUE')
                if initial_value_elem is not None:
                    initial_value = int(initial_value_elem.text)
            elif elem.tag == 'ADMIN-DATA':
                pass
            elif elem.tag == 'SYSTEM-SIGNAL-REF':
                pass
            elif elem.tag == 'NETWORK-REPRESENTATION-PROPS':
                pass
            elif elem.tag == 'DATA-TRANSFORMATIONS':
                pass
            elif elem.tag == 'TRANSFORMATION-I-SIGNAL-PROPSS':
                pass
            elif elem.tag == 'DESC':
                descXml = xmlRoot.find('DESC')
                if descXml is not None:
                    L2Xml = descXml.find('L-2')
                    if L2Xml is not None:
                        desc = parseTextNode(L2Xml)
            elif elem.tag == 'DATA-TYPE-POLICY':
                data_type_policy = elem.text
            elif elem.tag == 'I-SIGNAL-TYPE':
                signal_type = elem.text
            else:
                raise NotImplementedError(elem.tag)

        return ISignal(name, data_type_policy, signal_type, initial_value, desc, parent)

    def parseSystemSignal(self,xmlRoot,parent=None):
        """
        parses <SYSTEM-SIGNAL>
        """
        assert(xmlRoot.tag == 'SYSTEM-SIGNAL')
        name, dynamic_length, desc = None, None, None
        for elem in xmlRoot.findall('./*'):
            if elem.tag == 'SHORT-NAME':
                name=parseTextNode(elem)
            elif elem.tag == 'INIT-VALUE-REF':
                initValueRef = parseTextNode(elem)
            elif elem.tag == 'PHYSICAL-PROPS':
                pass
            elif elem.tag == 'DYNAMIC-LENGTH':
                dynamic_length = elem.text
            elif elem.tag == 'ADMIN-DATA':
                pass
            elif elem.tag == 'LONG-NAME':
                pass
            elif elem.tag=='DESC':
                descXml = xmlRoot.find('DESC')
                if descXml is not None:
                    L2Xml = descXml.find('L-2')
                    if L2Xml is not None:
                        desc = parseTextNode(L2Xml)
            else:
                raise NotImplementedError(elem.tag)
        if name is not None:
            return SystemSignal(name, desc, parent)
        else:
            raise exception('failed to parse %s'%xmlRoot.tag)

    def parseSystemSignalGroup(self, xmlRoot, parent=None):
        name, system_signal_refs = None, None
        for elem in xmlRoot.findall('./*'):
            if elem.tag == 'SHORT-NAME':
                name = parseTextNode(elem)
            elif elem.tag == 'LONG-NAME':
                pass
            elif elem.tag == 'DESC':
                pass
            elif elem.tag == 'ADMIN-DATA':
                pass
            elif elem.tag == 'SYSTEM-SIGNAL-REFS':
                system_signal_refs = []
                for childElem in elem.findall('./*'):
                    if childElem.tag == 'SYSTEM-SIGNAL-REF':
                        system_signal_refs.append(parseTextNode(childElem))
                    else:
                        raise NotImplementedError(childElem.tag)
            else:
                raise NotImplementedError(elem.tag)

        if (name is not None) and (isinstance(system_signal_refs, list)):
            return SystemSignalGroup(name, system_signal_refs)
        else:
            raise exception('failed to parse %s'%xmlRoot.tag)

# -*- coding: utf-8 -*-
"""
    binalyzer_wasm.wasm
    ~~~~~~~~~~~~~~~~~~~

    This module implements WebAssembly specific helpers for binary file parsing.

    :copyright: 2020 Denis Vasilík
    :license: MIT
"""
import leb128

from binalyzer_core import (
    ValueProviderBase,
    PropertyBase,
)


class LEB128UnsignedValueConverter(object):

    def convert(self, value, template):
        return leb128.u.decode(value)

    def convert_back(self, value, template):
        return leb128.u.encode(value)


class LEB128UnsignedBindingValueProvider(ValueProviderBase):

    def __init__(self, template=None):
        self.template = template
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        data = self.template.binding_context.data_provider.data
        absolute_address = self.template.absolute_address
        data.seek(absolute_address)
        size = _get_leb128size(data)
        data.seek(absolute_address)
        leb128_value = list(data.read(size))
        leb128_value.reverse()
        self._cached_value = bytes(leb128_value)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not implemented, yet.')


class LEB128SizeBindingValueProvider(ValueProviderBase):

    def __init__(self, template=None):
        self.template = template
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        data = self.template.binding_context.data_provider.data
        absolute_address = self.template.absolute_address
        data.seek(absolute_address)
        self._cached_value = _get_leb128size(data)
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not implemented, yet.')


class LEB128UnsignedBindingProperty(PropertyBase):

    def __init__(self, template):
        super(LEB128UnsignedBindingProperty, self).__init(
            template=template,
            value_provider=LEB128UnsignedBindingValueProvider(template),
            value_converter=LEB128UnsignedValueConverter(),
        )


class LimitsSizeBindingValueProvider(ValueProviderBase):

    def __init__(self, template=None):
        self.template = template
        self._cached_value = None

    def get_value(self):
        if not self._cached_value is None:
            return self._cached_value
        data = self.template.binding_context.data_provider.data
        absolute_address = self.template.absolute_address
        data.seek(absolute_address)
        flag = data.read(0)
        size = 1
        if flag == 0x00:
            size += _get_leb128size(data)
        elif flag == 0x01:
            size += _get_leb128size(data)
            size += _get_leb128size(data)
        else:
            raise RuntimeError('Invalid value')
        self._cached_value = size
        return self._cached_value

    def set_value(self, value):
        raise RuntimeError('Not implemented, yet.')


def _get_leb128size(data):
    size = 1
    byte_value = int.from_bytes(data.read(1), 'little')
    while ((byte_value & 0x80) == 0x80):
        size += 1
        byte_value = int.from_bytes(data.read(1), 'little')
    return size

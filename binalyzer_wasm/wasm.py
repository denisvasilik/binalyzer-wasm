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
    TemplateFactory,
    value_cache,
)


class LEB128UnsignedBindingValueProvider(ValueProviderBase):
    def __init__(self, property):
        super(LEB128UnsignedBindingValueProvider, self).__init__(property)

    @value_cache
    def get_value(self):
        data = self.property.template.binding_context.data_provider.data
        absolute_address = self.property.template.absolute_address
        data.seek(absolute_address)
        size = _get_leb128size(data)
        data.seek(absolute_address)
        leb128_value = list(data.read(size))
        leb128_bytes = bytes(leb128_value)
        return leb128.u.decode(leb128_bytes)

    def set_value(self, value):
        raise RuntimeError("Not implemented, yet.")


class LEB128SizeBindingValueProvider(ValueProviderBase):
    def __init__(self, property):
        super(LEB128SizeBindingValueProvider, self).__init__(property)

    @value_cache
    def get_value(self):
        template = self.property.template
        data = template.binding_context.data_provider.data
        absolute_address = template.absolute_address
        data.seek(absolute_address)
        return _get_leb128size(data)

    def set_value(self, value):
        raise RuntimeError("Not implemented, yet.")


class LimitsSizeBindingValueProvider(ValueProviderBase):
    def __init__(self, property):
        super(LimitsSizeBindingValueProvider, self).__init__(property)

    @value_cache
    def get_value(self):
        template = self.property.template
        data = template.binding_context.data_provider.data
        absolute_address = template.absolute_address
        data.seek(absolute_address)
        flag = int.from_bytes(data.read(1), "little")
        size = 1
        if flag == 0x00:
            size += _get_leb128size(data)
        elif flag == 0x01:
            size += _get_leb128size(data)
            size += _get_leb128size(data)
        else:
            raise RuntimeError("Invalid value")
        return size

    def set_value(self, value):
        raise RuntimeError("Not implemented, yet.")


class ExpressionSizeValueProvider(ValueProviderBase):
    def __init__(self, property):
        super(ExpressionSizeValueProvider, self).__init__(property)

    @value_cache
    def get_value(self):
        template = self.property.template
        data = template.binding_context.data_provider.data
        absolute_address = template.absolute_address
        data.seek(absolute_address)
        value = int.from_bytes(data.read(1), "little")
        size = 1
        while value != 0x0B:
            value = int.from_bytes(data.read(1), "little")
            size += 1
        return size

    def set_value(self, value):
        raise RuntimeError("Not implemented, yet.")


def _get_leb128size(data):
    size = 1
    byte_value = int.from_bytes(data.read(1), "little")
    while (byte_value & 0x80) == 0x80:
        size += 1
        byte_value = int.from_bytes(data.read(1), "little")
    return size

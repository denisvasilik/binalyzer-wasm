"""
    binalyzer_wasm.extension
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Binalyzer WebAssembly extension.
"""
from binalyzer_core import BinalyzerExtension
from .wasm import (
    LEB128SizeBindingValueProvider,
    LEB128UnsignedBindingValueProvider,
    LimitsSizeBindingValueProvider,
    ExpressionSizeValueProvider,
)


class WebAssemblyExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        super(WebAssemblyExtension, self).__init__(binalyzer, "wasm")

    def init_extension(self):
        super(WebAssemblyExtension, self).init_extension()

    def leb128size(self, property):
        return LEB128SizeBindingValueProvider(property)

    def leb128u(self, property):
        return LEB128UnsignedBindingValueProvider(property)

    def limits(self, property):
        return LimitsSizeBindingValueProvider(property)

    def expr_size(self, property):
        return ExpressionSizeValueProvider(property)

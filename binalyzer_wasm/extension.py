"""
    binalyzer_wasm.extension
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Binalyzer WebAssembly extension.
"""
from binalyzer_core import BinalyzerExtension
from .wasm import (
    LEB128SizeBindingValueProvider,
    LEB128UnsignedValueProvider,
    LEB128UnsignedBindingValueProvider,
    LimitsSizeBindingValueProvider,
    ExpressionSizeValueProvider,
    PacketRecordCountValueProvider,
    RepetitionCountValueProvider,
)


class WebAssemblyExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        super(WebAssemblyExtension, self).__init__(binalyzer, "wasm")

    def init_extension(self):
        super(WebAssemblyExtension, self).init_extension()

    def leb128size(self, template):
        return LEB128SizeBindingValueProvider(template)

    def leb128u(self, template):
        return LEB128UnsignedBindingValueProvider(template)

    def limits(self, template):
        return LimitsSizeBindingValueProvider(template)

    def expr_size(self, template):
        return ExpressionSizeValueProvider(template)

    def packet_record_count(self, template):
        return RepetitionCountValueProvider(template)

    def repeat(self, template):
        return RepetitionCountValueProvider(template)

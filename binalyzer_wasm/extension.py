"""
    binalyzer_wasm.extension
    ~~~~~~~~~~~~~~~~~~~~~~~~

    This module implements the Binalyzer WebAssembly extension.
"""
from binalyzer_core import (
    BinalyzerExtension,
    IdentityValueConverter,
)
from .wasm import (
    LEB128SizeBindingValueProvider,
    LEB128UnsignedValueConverter,
    LEB128UnsignedBindingValueProvider,
    LimitsSizeBindingValueProvider,
)


class WebAssemblyExtension(BinalyzerExtension):
    def __init__(self, binalyzer=None):
        super(WebAssemblyExtension, self).__init__(binalyzer, "wasm")

    def init_extension(self):
        super(WebAssemblyExtension, self).init_extension()

    def leb128size(self, template):
        return (
            IdentityValueConverter(),
            LEB128SizeBindingValueProvider(template),
        )

    def leb128u(self, template):
        return (
            LEB128UnsignedValueConverter(),
            LEB128UnsignedBindingValueProvider(template),
        )

    def limits(self, template):
        return (
            IdentityValueConverter(),
            LimitsSizeBindingValueProvider(template),
        )

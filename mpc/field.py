import math

class FieldElement(object):
    """Common base class for elements."""

    value = None
    modulus = None
    field = lambda x: None

    def __int__(self):
        """
        Extract integer value from the field element.
        """
        return self.value

    __long__ = __int__

    def split(self):
        """
        Splits self into bit array LSB first.
        """
        length = int(math.ceil(math.log(self.modulus, 2)))
        result = [0] * length
        temp = self.value
        for i in range(length):
            result[i] = self.field(temp % 2)
            temp = temp // 2
        return result

def GF(modulus):
    """
    Generate a Galois (finite) field with the given modulus.
    The modulus must be a prime
    """
    # Define a new class representing the field. This class will be
    # returned at the end of the function.
    class GFElement(FieldElement):

        def __init__(self, value):
            self.value = value % self.modulus

        def __add__(self, other):
            """Addition."""
            if not isinstance(other, (GFElement, int, long)):
                return NotImplemented
            try:
                # We can do a quick test using 'is' here since
                # there will only be one class representing this
                # field.
                assert self.field is other.field, "Fields must be identical"
                return GFElement(self.value + other.value)
            except AttributeError:
                return GFElement(self.value + other)

        __radd__ = __add__

        def __sub__(self, other):
            """Subtraction."""
            if not isinstance(other, (GFElement, int, long)):
                return NotImplemented
            try:
                assert self.field is other.field, "Fields must be identical"
                return GFElement(self.value - other.value)
            except AttributeError:
                return GFElement(self.value - other)

        def __rsub__(self, other):
            """Subtraction (reflected argument version)."""
            return GFElement(other - self.value)

        def __xor__(self, other):
            """Xor for bitvalues."""
            if not isinstance(other, (GFElement, int, long)):
                return NotImplemented
            try:
                assert self.field is other.field, "Fields must be identical"
                return GFElement(self.value ^ other.value)
            except AttributeError:
                return GFElement(self.value ^ other)

        def __rxor__(self, other):
            """Xor for bitvalues (reflected argument version)."""
            return GFElement(other ^ self.value)

        def __mul__(self, other):
            """Multiplication."""
            if not isinstance(other, (GFElement, int, long)):
                return NotImplemented
            try:
                assert self.field is other.field, "Fields must be identical"
                return GFElement(self.value * other.value)
            except AttributeError:
                return GFElement(self.value * other)

        __rmul__ = __mul__

        def __pow__(self, exponent):
            """Exponentiation."""
            return GFElement(pow(self.value, exponent, self.modulus))

        def __neg__(self):
            """Negation."""
            return GFElement(-self.value)

        def __invert__(self):
            """Inversion.

            Note that zero cannot be inverted, trying to do so
            will raise a ZeroDivisionError.
            """
            if self.value == 0:
                raise ZeroDivisionError("Cannot invert zero")

            def extended_gcd(a, b):
                """The extended Euclidean algorithm."""
                x = 0
                lastx = 1
                y = 1
                lasty = 0
                while b != 0:
                    quotient = a // b
                    a, b = b, a % b
                    x, lastx = lastx - quotient*x, x
                    y, lasty = lasty - quotient*y, y
                return (lastx, lasty, a)

            inverse = extended_gcd(self.value, self.modulus)[0]
            return GFElement(inverse)

        def __div__(self, other):
            """Division."""
            try:
                assert self.field is other.field, "Fields must be identical"
                return self * ~other
            except AttributeError:
                return self * ~GFElement(other)

        __truediv__ = __div__
        __floordiv__ = __div__

        def __rdiv__(self, other):
            """Division (reflected argument version)."""
            return GFElement(other) / self

        __rtruediv__ = __rdiv__
        __rfloordiv__ = __rdiv__

        def sqrt(self):
            """Square root.

            No attempt is made the to return the positive square root.

            Computing square roots is only possible when the modulus
            is a Blum prime (congruent to 3 mod 4).
            """
            assert self.modulus % 4 == 3, "Cannot compute square " \
                "root of %s with modulus %s" % (self, self.modulus)

            # Because we assert that the modulus is a Blum prime
            # (congruent to 3 mod 4), there will be no reminder in the
            # division below.
            root = pow(self.value, (self.modulus+1)//4, self.modulus)
            return GFElement(root)

        def bit(self, index):
            """Extract a bit (index is counted from zero)."""
            return (self.value >> index) & 1

        def signed(self):
            """Return a signed integer representation of the value.

            If x > floor(p/2) then subtract p to obtain negative integer.
            """
            if self.value > ((self.modulus-1)/2):
                return self.value - self.modulus
            else:
                return self.value

        def unsigned(self):
            """Return a unsigned representation of the value"""
            return self.value

        def __repr__(self):
            return "{%d}" % self.value

        def __str__(self):
            """Informal string representation.

            This is simply the value enclosed in curly braces.
            """
            return "{%d}" % self.unsigned()

        def __eq__(self, other):
            """Equality test."""
            try:
                assert self.field is other.field, "Fields must be identical"
                return self.value == other.value
            except AttributeError:
                return self.value == other

        def __ne__(self, other):
            """Inequality test."""
            try:
                assert self.field is other.field, "Fields must be identical"
                return self.value != other.value
            except AttributeError:
                return self.value != other

        def __cmp__(self, other):
            """Comparison."""
            try:
                assert self.field is other.field, "Fields must be identical"
                return cmp(self.value, other.value)
            except AttributeError:
                return cmp(self.value, other)

        def __hash__(self):
            """Hash value."""
            return hash((self.field, self.value))

        def __nonzero__(self):
            """Truth value testing.

            Returns False if this element is zero, True otherwise.
            """
            return self.value != 0

    GFElement.modulus = modulus
    GFElement.field = GFElement

    return GFElement

# TODO: Redefine for optimizations
GF64 = GF(618970019642690137449562111)

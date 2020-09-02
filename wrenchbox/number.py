from decimal import Decimal, InvalidOperation, ROUND_HALF_DOWN


class EnhancedDecimal:
    def __init__(self, n, default=None):
        if n is None:
            if isinstance(default, Decimal):
                self.n = default
            else:
                raise TypeError
        elif not isinstance(n, Decimal):
            try:
                self.n = Decimal(repr(n))
            except InvalidOperation:
                self.n = Decimal(n)
        else:
            self.n = n

    def round(self, r: Decimal, d=ROUND_HALF_DOWN):
        """
        Round the decimal number with a given unit
        :param r: the unit, e.g., 1, 0.5
        :param d: rounding direction, see decimal.ROUND_* for details
        :return: the rounded number
        """
        r = EnhancedDecimal(r)
        return (self.n / r.n).to_integral_exact(rounding=d) * r.n


if __name__ == "__main__":
    print(EnhancedDecimal('3.1415926').round(Decimal('0.1')))

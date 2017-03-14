#!/usr/local/bin/python3
import sys


def greatest_common_divisor(bigger_number, smaller_number):
    if bigger_number < smaller_number:
        bigger_number, smaller_number = smaller_number, bigger_number
    while smaller_number > 0:
        bigger_number, smaller_number = smaller_number, bigger_number % smaller_number
    return bigger_number


class RationalException(Exception):
    pass


class Rational(object):
    def __init__(self, numerator=0, denominator=1):
        if (type(numerator) != int) or (type(denominator) != int):
            raise RationalException()
        if denominator == 0:
            raise ZeroDivisionError("denominator is null")

        self.denominator = denominator
        self.numerator = numerator

        if self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1
        self.reduce()

    def __add__(self, other):
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        result = Rational(new_numerator, new_denominator)
        result.reduce()
        return result

    def __neg__(self):
        return Rational(-self.numerator, self.denominator)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        result = Rational(new_numerator, new_denominator)
        result.reduce()
        return result

    def __div__(self, other):
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        result = Rational(new_numerator, new_denominator)
        result.reduce()
        return result

    def __eq__(self, other):
        return (self.numerator == other.numerator) and (self.denominator == other.denominator)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return str(self.numerator) + '/' + str(self.denominator)

    def reduce(self):
        common_divisor = greatest_common_divisor(abs(self.numerator), abs(self.denominator))
        self.numerator /= common_divisor
        self.denominator /= common_divisor

exec(sys.stdin.read())

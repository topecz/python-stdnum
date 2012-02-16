# vat.py - functions for handling Austrian VAT numbers
#
# Copyright (C) 2012 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""Module for handling Austrian UID (Umsatzsteuer-Identifikationsnummer,
VAT) numbers.

The number is a 9-digit number that always starts with a U (optionally
preceded with AT). The last digit is a check digit.

>>> compact('AT U13585627')
'U13585627'
>>> is_valid('U13585627')
True
>>> calc_check_digit('U1358562')
'7'
>>> is_valid('U13585626')  # incorrect check digit
False
"""

from stdnum import luhn
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -./').upper().strip()
    if number.startswith('AT'):
        number = number[2:]
    return number


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    return str((6 - luhn.checksum(number[1:])) % 10)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 9 and number[0] == 'U' and \
           number[1:].isdigit() and \
           calc_check_digit(number[:-1]) == number[-1]
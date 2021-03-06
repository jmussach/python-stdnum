# brin.py - functions for handling Brin numbers
#
# Copyright (C) 2013-2017 Arthur de Jong
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

"""Brin number (Dutch number for schools).

The Brin (Basis Registratie Instellingen) is a number to identify schools
and related institutions. The number consists of four alphanumeric
characters, sometimes extended with two digits to indicate the site (this
complete code is called the vestigingsnummer).

The register of these numbers can be downloaded from:
https://www.duo.nl/open_onderwijsdata/databestanden/

>>> validate('05 KO')
'05KO'
>>> validate('07NU 00')
'07NU00'
>>> validate('12KB1')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('30AJ0A')  # location code has letter
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


# this regular expression is based on what was found in the online
# database: the first two digits are always numeric, followed by two
# letters and an optional two letter location identifier
_brin_re = re.compile(r'^(?P<brin>[0-9]{2}[A-Z]{2})(?P<location>[0-9]{2})?$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').upper().strip()


def validate(number):
    """Checks to see if the number provided is in the correct format.
    This currently does not check whether the number points to a
    registered school."""
    number = compact(number)
    if len(number) not in (4, 6):
        raise InvalidLength()
    match = _brin_re.search(number)
    if not match:
        raise InvalidFormat()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid Brin number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

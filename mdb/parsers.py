"""ORM model parsers."""

from mdb.config import LOGGER
from mdb.orm import Customer


__all__ = ['customer']


def customer(string: str) -> Customer:
    """Returns the first matched Customer."""

    try:
        first, *ambiguous = Customer.find(string)
    except ValueError:
        raise ValueError('No such customer.') from None

    for customer in ambiguous:  # pylint: disable=W0621
        LOGGER.warning('Found ambiguous customer: %s', customer)

    return first

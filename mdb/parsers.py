"""ORM model parsers."""

from mdb.orm import Customer


__all__ = ['customer']


def customer(string: str) -> Customer:
    """Returns the respective customer."""

    try:
        match, *excess = Customer.find(string)
    except ValueError:
        raise ValueError('No such customer.') from None

    if excess:
        raise ValueError('Ambiguous customer selection.')

    return match

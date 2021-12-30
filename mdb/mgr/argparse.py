"""Argument parser for the mdbmgr."""

from argparse import ArgumentParser, Namespace, _SubParsersAction


__all__ = ['get_args']


def _add_find_address_parser(subparsers: _SubParsersAction):
    """Adds a parser to find address records."""

    parser = subparsers.add_parser('address', help='find addresses')
    parser.add_argument('-s', '--street', metavar='street')
    parser.add_argument('-H', '--house-number', metavar='houseno')
    parser.add_argument('-z', '--zip-code', metavar='zip_code')
    parser.add_argument('-p', '--po-box', metavar='po_box')
    parser.add_argument('-c', '--city', metavar='city')
    parser.add_argument('-d', '--district', metavar='district')
    parser.add_argument('-S', '--state', type=int, metavar='ID')


def _add_find_company_parser(subparsers: _SubParsersAction):
    """Adds a parser to find company records."""

    parser = subparsers.add_parser('company', help='find companies')
    parser.add_argument('-n', '--name', metavar='name')
    parser.add_argument('-s', '--abbreviation', metavar='text')
    parser.add_argument('-A', '--address', type=int, metavar='ID')
    parser.add_argument('-a', '--annotation', metavar='text')


def _add_find_customer_parser(subparsers: _SubParsersAction):
    """Adds a parser to find customers."""

    parser = subparsers.add_parser('customer', help='find customers')
    parser.add_argument('-i', '--id', type=int, metavar='ID')
    parser.add_argument('-C', '--company', type=int, metavar='ID')
    parser.add_argument('-R', '--reseller', type=int, metavar='ID')
    parser.add_argument('-a', '--annotation', metavar='text')
    parser.add_argument('-n', '--name', metavar='company_name')


def _add_find_department_parser(subparsers: _SubParsersAction):
    """Adds a parser to find departments."""

    parser = subparsers.add_parser('department', help='find departments')
    parser.add_argument('-n', '--name', metavar='name')
    parser.add_argument('-t', '--type', metavar='type')


def _add_find_employee_parser(subparsers: _SubParsersAction):
    """Adds a parser to find employees."""

    parser = subparsers.add_parser('employee', help='find employees')
    parser.add_argument('-C', '--company', type=int, metavar='ID')
    parser.add_argument('-D', '--department', type=int, metavar='ID')
    parser.add_argument('-f', '--first-name', metavar='name')
    parser.add_argument('-l', '--last-name', metavar='surname')
    parser.add_argument('-A', '--address', type=int, metavar='ID')


def _add_find_tenement_parser(subparsers: _SubParsersAction):
    """Adds a parser to find tenements."""

    parser = subparsers.add_parser('tenement', help='find tenements')
    parser.add_argument('-C', '--customer', type=int, metavar='ID')
    parser.add_argument('-A', '--address', type=int, metavar='ID')
    parser.add_argument('-r', '--rental-unit', metavar='text')
    parser.add_argument('-l', '--living-unit', metavar='text')
    parser.add_argument('-a', '--annotation', metavar='text')


def _add_find_parsers(subparsers: _SubParsersAction):
    """Adds parsers for the find command."""

    parser = subparsers.add_parser('find', help='find database records')
    subparsers = parser.add_subparsers(dest='table')
    _add_find_address_parser(subparsers)
    _add_find_company_parser(subparsers)
    _add_find_customer_parser(subparsers)
    _add_find_department_parser(subparsers)
    _add_find_employee_parser(subparsers)
    _add_find_tenement_parser(subparsers)


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description='Main database management utility.')
    subparsers = parser.add_subparsers(dest='action')
    _add_find_parsers(subparsers)
    return parser.parse_args()

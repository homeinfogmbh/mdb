"""Common functions."""

from argparse import Namespace

from peewee import ModelSelect

from mdb.orm import Address
from mdb.orm import Company
from mdb.orm import Country
from mdb.orm import Customer
from mdb.orm import Department
from mdb.orm import Employee
from mdb.orm import State
from mdb.orm import Tenement


__all__ = ['find_recods']


def find_addresses(args: Namespace) -> ModelSelect:
    """Finds addresses."""

    condition = True

    if args.street is not None:
        condition &= Address.street ** f'%{args.street}%'

    if args.house_number is not None:
        condition &= Address.house_number ** f'%{args.house_number}%'

    if args.zip_code is not None:
        condition &= Address.zip_code ** f'%{args.zip_code}%'

    if args.po_box is not None:
        condition &= Address.po_box ** f'%{args.po_box}%'

    if args.city is not None:
        condition &= Address.city ** f'%{args.city}%'

    if args.district is not None:
        condition &= Address.district ** f'%{args.district}%'

    if args.state is not None:
        condition &= Address.state == args.state

    return Address.select().where(condition)


def find_companies(args: Namespace) -> ModelSelect:
    """Finds companies."""

    condition = True

    if args.name is not None:
        condition &= Company.name ** f'%{args.name}%'

    if args.abbreviation is not None:
        condition &= Company.abbreviation ** f'%{args.abbreviation}%'

    if args.address is not None:
        condition &= Company.address == args.address

    if args.annotation is not None:
        condition &= Company.annotation ** f'%{args.annotation}%'

    return Company.select().where(condition)


def find_countries(args: Namespace) -> ModelSelect:
    """Finds countries."""

    condition = True

    if args.iso is not None:
        condition &= Country.iso == args.iso

    if args.name is not None:
        condition &= Country.name ** f'%{args.name}%'

    if args.native_name is not None:
        condition &= Country.original_name ** f'%{args.native_name}%'

    return Country.select().where(condition)


def find_customers(args: Namespace) -> ModelSelect:
    """Finds customers."""

    condition = True

    if args.id is not None:
        condition &= Customer.id == args.id

    if args.company is not None:
        condition &= Customer.company == args.company

    if args.reseller is not None:
        condition &= Customer.reseller == args.reseller

    if args.annotation is not None:
        condition &= Customer.annotation ** f'%{args.annotation}%'

    if args.name is not None:
        condition &= Company.name ** f'%{args.name}%'

    return Customer.select(Customer, Company).join(Company).where(condition)


def find_departments(args: Namespace) -> ModelSelect:
    """Finds departments."""

    condition = True

    if args.name is not None:
        condition &= Department.name ** f'%{args.name}%'

    if args.type is not None:
        condition &= Department.type ** f'%{args.type}%'

    return Department.select().where(condition)


def find_employees(args: Namespace) -> ModelSelect:
    """Finds employees."""

    condition = True

    if args.company is not None:
        condition &= Employee.company == args.company

    if args.department is not None:
        condition &= Employee.department == args.department

    if args.first_name is not None:
        condition &= Employee.first_name ** f'%{args.first_name}%'

    if args.last_name is not None:
        condition &= Employee.surname ** f'%{args.last_name}%'

    if args.address is not None:
        condition &= Employee.address == args.address

    return Employee.select().where(condition)


def find_states(args: Namespace) -> ModelSelect:
    """Finds states."""

    condition = True

    if args.country is not None:
        condition &= State.country == args.country

    if args.iso is not None:
        condition &= State.iso == args.iso

    if args.name is not None:
        condition &= State.name ** f'%{args.name}%'

    return State.select().where(condition)


def find_tenements(args: Namespace) -> ModelSelect:
    """Finds tenements."""

    condition = True

    if args.customer is not None:
        condition &= Tenement.customer == args.customer

    if args.address is not None:
        condition &= Tenement.address == args.address

    if args.rental_unit is not None:
        condition &= Tenement.rental_unit ** f'%{args.rental_unit}%'

    if args.living_unit is not None:
        condition &= Tenement.living_unit ** f'%{args.living_unit}%'

    if args.annotation is not None:
        condition &= Tenement.annotation ** f'%{args.annotation}%'

    return Tenement.select().where(condition)


def find_recods(args: Namespace) -> ModelSelect:    # pylint: disable=R0911
    """Finds recods."""

    if args.table == 'address':
        return find_addresses(args)

    if args.table == 'company':
        return find_companies(args)

    if args.table == 'country':
        return find_countries(args)

    if args.table == 'customer':
        return find_customers(args)

    if args.table == 'department':
        return find_departments(args)

    if args.table == 'employee':
        return find_employees(args)

    if args.table == 'state':
        return find_states(args)

    if args.table == 'tenement':
        return find_tenements(args)

    return []

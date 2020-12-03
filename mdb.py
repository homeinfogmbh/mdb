"""HOMEINFO's main data database."""

from __future__ import annotations
from logging import getLogger
from typing import Iterable, Set, Tuple, Union

from peewee import CharField, ForeignKeyField, IntegerField, Model

from configlib import loadcfg
from peeweeplus import MySQLDatabase, JSONModel


__all__ = [
    'AlreadyExists',
    'Country',
    'State',
    'Address',
    'Company',
    'Department',
    'Employee',
    'Customer',
    'Tenement',
    'customer'
]


CONFIG = loadcfg('mdb.conf')
DATABASE = MySQLDatabase.from_config(CONFIG['db'])
LOGGER = getLogger(__file__)
AddrType = Tuple[str, str, str]
AddressType = Tuple[str, str, str, str]


class AlreadyExists(Exception):
    """Indicates that a certainr record already exists."""

    def __init__(self, record: Model, **keys):
        """Sets the record and key."""
        super().__init__(record, keys)
        self.record = record
        self.keys = keys

    def __str__(self):
        """Prints record and keys."""
        record_type = type(self.record).__name__

        if self.keys:
            return f'{record_type} already exists for {self.keys}.'

        return f'{record_type} already exists.'


class MDBModel(JSONModel):  # pylint: disable=R0903
    """Generic HOMEINFO MDB Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database

    def __repr__(self):
        """Returns the model's ID as per default."""
        return str(self.id)


class Country(MDBModel):
    """Countries."""

    iso = CharField(2)  # ISO 3166-2 country code
    name = CharField(64)
    original_name = CharField(64, null=True, default=None)

    def __str__(self):  # pylint: disable=E0307
        """Converts the country to a string."""
        return self.name

    def __repr__(self):     # pylint: disable=E0306
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern: str) -> Iterable[Country]:
        """Finds countries by patterns."""
        return cls.select().where(
            (cls.iso ** f'%{pattern}%')
            | (cls.name ** f'%{pattern}%')
            | (cls.original_name ** f'%{pattern}%')
        )


class State(MDBModel):
    """States within countries."""

    country = ForeignKeyField(Country, column_name='country', backref='states')
    iso = CharField(2)  # ISO 3166-2 state code
    name = CharField(64)

    def __str__(self):  # pylint: disable=E0307
        """Returns the country's name."""
        return self.name

    def __repr__(self):     # pylint: disable=E0306
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern: str) -> Iterable[State]:
        """Finds a state by the provided pattern."""
        try:
            country = int(pattern)
        except ValueError:
            if len(pattern) == 2:
                return cls.select().where(cls.iso == pattern)

            return cls.select().where(cls.name ** f'%{pattern}%')

        return cls.select().where(cls.country == country)

    @property
    def iso3166(self) -> str:
        """Returns the full ISO 3166-2 compliant code."""
        return f'{self.country.iso}-{self.iso}'


class Address(MDBModel):
    """Address data."""

    street = CharField(64, null=True)
    house_number = CharField(8, null=True)
    zip_code = CharField(32, null=True)
    po_box = CharField(32, null=True)
    city = CharField(64)
    district = CharField(64, null=True)
    state = ForeignKeyField(State, column_name='state', null=True)

    def __str__(self):
        """Returns the oneliner or an empty string."""
        return self.oneliner or ''

    @classmethod
    def add_by_address(cls, address: AddressType, district: str = None,
                       state: Union[State, int] = None) -> Address:
        """Adds a new address by a complete address."""
        street, house_number, zip_code, city = address
        select = Address.city == city
        select &= Address.street == street
        select &= Address.house_number == house_number
        select &= Address.zip_code == zip_code

        if district is not None:
            select &= cls.district == district

        if state is not None:
            select &= cls.state == state

        try:
            return Address.get(select)
        except Address.DoesNotExist:
            return Address(
                city=city, street=street, house_number=house_number,
                zip_code=zip_code, district=district, state=state)

    @classmethod
    def add_by_po_box(cls, po_box: str, city: str, district: str = None,
                      state: Union[State, int] = None) -> Address:
        """Adds an address by a PO box."""
        select = True if state is None else cls.state == state
        select &= Address.po_box == po_box
        select &= Address.city == city

        if district is not None:
            select &= cls.district == district

        if state is not None:
            select &= cls.state == state

        try:
            return Address.get(select)
        except Address.DoesNotExist:
            return Address(
                po_box=po_box, city=city, district=district, state=state)

    @classmethod
    def add(    # pylint: disable=R0913
            cls, city: str, po_box: str = None, addr: AddrType = None,
            district: str = None, state: Union[State, int] = None) -> Address:
        """Adds an address record to the database.

        Usage:
            * Add address with either po_box or addr parameter.
            * addr must be a tuple: (<street>, <house_number>, <zip_code>).
        """
        po_box_addr_xor_err = ValueError('Must specify either po_box or addr')

        if po_box is None and addr is None:
            raise po_box_addr_xor_err

        if po_box is not None and addr is not None:
            raise po_box_addr_xor_err

        if addr is not None:
            try:
                street, house_number, zip_code = addr
            except ValueError:
                raise ValueError(f'addr must be of type {AddrType}') from None

            address = (street, house_number, zip_code, city)
            return cls.add_by_address(address, district=district, state=state)

        if po_box is not None:
            return cls.add_by_po_box(
                po_box, city, district=district, state=state)

        raise po_box_addr_xor_err

    @classmethod
    def find(cls, pattern: str) -> Iterable[Address]:
        """Finds an address."""
        return cls.select().where(
            (cls.street ** f'%{pattern}%')
            | (cls.house_number ** f'%{pattern}%')
            | (cls.zip_code ** f'%{pattern}%')
            | (cls.po_box ** f'%{pattern}%')
            | (cls.city ** f'%{pattern}%')
        )

    @classmethod
    def from_json(cls, json: dict) -> Address:
        """Returns an address from the respective dictionary."""
        state = json.pop('state', None)
        record = super().from_json(json)
        addr = (record.street, record.house_number, record.zip_code)

        if all(addr) and not record.po_box:
            pass
        elif not any(addr) and record.po_box:
            pass
        else:
            raise ValueError('Must specify either poBox or addr.')

        if state is not None:
            try:
                state, *ambiguous = State.find(state)
            except ValueError:
                raise State.DoesNotExist() from None

            if ambiguous:
                raise ValueError('Ambiguous state.')

        record.state = state
        return record

    @property
    def street_houseno(self) -> Union[str, None]:
        """Returns street and hounse number."""
        if self.street and self.house_number:
            return f'{self.street} {self.house_number}'

        if self.street:
            return self.street

        return None

    @property
    def city_district(self) -> Union[str, None]:
        """Returns the city and district."""
        if self.city and self.district:
            return f'{self.city} - {self.district}'

        if self.city:
            return self.city

        return None

    @property
    def zip_code_city(self) -> Union[str, None]:
        """Returns ZIP code and city."""
        city_district = self.city_district

        if self.zip_code and city_district:
            return f'{self.zip_code} {city_district}'

        return city_district

    @property
    def oneliner(self) -> Union[str, None]:
        """Returns a one-liner string."""
        if self.po_box:
            return f'{self.po_box} {self.city_district}'

        street_houseno = self.street_houseno
        zip_code_city = self.zip_code_city

        if street_houseno and zip_code_city:
            return f'{street_houseno}, {zip_code_city}'

        return zip_code_city or street_houseno

    @property
    def text(self) -> str:
        """Converts the Address to a multi-line string."""
        result = ''

        if self.po_box:
            result += f'Postfach {self.po_box}\n'
        elif self.street:
            if self.house_number:
                result += f'{self.street} {self.house_number}\n'
            else:
                result += f'{self.street}\n'

        if self.zip_code:
            result += f'{self.zip_code} {self.city}\n'

        state = self.state

        if state:
            country_name = str(self.state.country)

            if country_name not in {'Deutschland', 'Germany', 'DE'}:
                result += f'{country_name}\n'

        return result


class Company(MDBModel):
    """Represents companies HOMEINFO has relations to."""

    name = CharField(255)
    abbreviation = CharField(16, null=True, default=None)
    address = ForeignKeyField(Address, column_name='address', null=True)
    annotation = CharField(256, null=True)

    def __str__(self):  # pylint: disable=E0307
        """Returns the company's name."""
        return self.name

    @classmethod
    def add(cls, name: str, abbreviation: str = None,
            address: Union[Address, int] = None,
            annotation: str = None) -> Company:
        """Adds a new company."""
        try:
            company = cls.get(cls.name == name)
        except cls.DoesNotExist:
            return cls(
                name=name, abbreviation=abbreviation, address=address,
                annotation=annotation)

        raise AlreadyExists(company, name=name)

    @classmethod
    def find(cls, pattern: str) -> Iterable[Company]:
        """Finds companies by primary key or name."""
        return cls.select().where(
            (cls.name ** f'%{pattern}%')
            | (cls.abbreviation ** f'%{pattern}%')
            | (cls.annotation ** f'%{pattern}%')
        )

    @property
    def departments(self) -> Set[Department]:
        """Returns the company's departments."""
        departments = set()

        for employee in self.employees:
            departments.add(employee.department)

        return departments


class Department(MDBModel):
    """Departments of companies."""

    name = CharField(64)
    type = CharField(64, null=True)

    def __str__(self):  # pylint: disable=E0307
        """Returns the department's name."""
        return self.name

    @classmethod
    def find(cls, pattern: str) -> Iterable[Department]:
        """Finds a department."""
        return cls.select().where(
            (cls.name ** f'%{pattern}%') | (cls.type * f'%{pattern}%'))


class Employee(MDBModel):
    """Employees."""

    company = ForeignKeyField(
        Company, column_name='company', backref='employees')
    department = ForeignKeyField(
        Department, column_name='department', backref='staff')
    first_name = CharField(32, null=True)
    surname = CharField(32)
    phone = CharField(32, null=True)
    cellphone = CharField(32, null=True)
    email = CharField(64, null=True)
    phone_alt = CharField(32, null=True)
    fax = CharField(32, null=True)
    address = ForeignKeyField(Address, column_name='address', null=True)

    def __str__(self):
        """Returns the employee's name."""
        if self.first_name is not None:
            return f'{self.first_name} {self.surname}'

        return self.surname

    @classmethod
    def find(cls, pattern: str) -> Iterable[Employee]:
        """Finds an employee."""
        return cls.select().where(
            (cls.surname ** f'%{pattern}%')
            | (cls.first_name ** f'%{pattern}%')
        )


class Customer(MDBModel):
    """CRM's customer(s)."""

    id = IntegerField(primary_key=True)
    company = ForeignKeyField(
        Company, column_name='company', backref='customers')
    reseller = ForeignKeyField(
        'self', column_name='reseller', backref='resellees', null=True)
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Returns the customer's full name."""
        return self.name

    def __repr__(self):
        """Returns the customer's ID."""
        return str(self.id)

    @classmethod
    def find(cls, pattern: str) -> Iterable[Customer]:
        """Finds a customer by the provided pattern."""
        try:
            cid = int(pattern)
        except ValueError:
            condition = Company.abbreviation ** pattern
            condition |= Company.name ** f'%{pattern}%'
        else:
            condition = Customer.id == cid

        return cls.select().join(Company).where(condition)

    @property
    def name(self) -> str:
        """Returns the customer's name."""
        return self.company.name

    def to_json(self, *, company: bool = False, **kwargs) -> dict:
        """Converts the customer to a JSON-ish dict."""
        json = super().to_json(**kwargs)

        if company:
            json['company'] = self.company.to_json(**kwargs)

        return json


class Tenement(MDBModel):   # pylint: disable=R0903
    """A tenement."""

    customer = ForeignKeyField(Customer, column_name='customer')
    address = ForeignKeyField(Address, column_name='address')
    rental_unit = CharField(255, null=True)     # Mieteinheit / ME.
    living_unit = CharField(255, null=True)     # Wohneinheit / WE.
    annotation = CharField(255, null=True)

    @classmethod
    def from_json(  # pylint: disable=W0621
            cls, json: dict, customer: Union[Customer, int],
            address: Union[Address, int], **kwargs) -> Tenement:
        """Returns a new tenement from a JSON-ish
        dict for the specified customer.
        """
        tenement = super().from_json(json, **kwargs)
        tenement.customer = customer
        tenement.address = address
        return tenement


def customer(string: str) -> Customer:
    """Returns the first matched Customer."""

    try:
        first, *ambiguous = Customer.find(string)
    except ValueError:
        raise ValueError('No such customer.') from None

    for customer in ambiguous:  # pylint: disable=W0621
        LOGGER.warning('Found ambiguous customer: %s', customer)

    return first

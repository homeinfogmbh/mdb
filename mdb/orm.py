"""HOMEINFO's main data database."""

from __future__ import annotations
from typing import Iterator, Optional, Union

from peewee import JOIN
from peewee import CharField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import ModelSelect

from peeweeplus import JSONModel

from mdb.config import DATABASE
from mdb.exceptions import AlreadyExists

__all__ = [
    'Country',
    'State',
    'Address',
    'Company',
    'Department',
    'Employee',
    'Customer',
    'Tenement'
]


GERMANY = {'Deutschland', 'Germany', 'DE'}


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
    original_name = CharField(64, null=True)

    def __str__(self):  # pylint: disable=E0307
        """Converts the country to a string."""
        return self.name

    def __repr__(self):     # pylint: disable=E0306
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern: str) -> ModelSelect:
        """Finds countries by patterns."""
        return cls.select().where(
            (cls.iso ** (pattern := f'%{pattern}%'))
            | (cls.name ** pattern)
            | (cls.original_name ** pattern)
        )

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.iso, self.name, self.original_name)


class State(MDBModel):
    """States within countries."""

    country = ForeignKeyField(Country, column_name='country', lazy_load=False,
                              backref='states')
    iso = CharField(2)  # ISO 3166-2 state code
    name = CharField(64)

    def __str__(self):  # pylint: disable=E0307
        """Returns the country's name."""
        return self.name

    def __repr__(self):     # pylint: disable=E0306
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern: str) -> ModelSelect:
        """Finds a state by the provided pattern."""
        try:
            country = int(pattern)
        except ValueError:
            if len(pattern) == 2:
                return cls.select(cascade=True).where(cls.iso == pattern)

            return cls.select(cascade=True).where(cls.name ** f'%{pattern}%')

        return cls.select(cascade=True).where(cls.country == country)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects states."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Country, *args}
        return super().select(*args, **kwargs).join(Country)

    @property
    def iso3166(self) -> str:
        """Returns the full ISO 3166-2 compliant code."""
        return f'{self.country.iso}-{self.iso}'

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.country_id, self.iso, self.name)


class Address(MDBModel):
    """Address data."""

    street = CharField(64)
    house_number = CharField(8)
    zip_code = CharField(32)
    city = CharField(64)
    district = CharField(64, null=True)
    state = ForeignKeyField(State, column_name='state', null=True,
                            lazy_load=False)

    def __str__(self):
        """Returns the oneliner or an empty string."""
        return self.oneliner or ''

    @classmethod
    def add(cls, street: str, house_number: str, zip_code: str, city: str, *,
            state: Optional[Union[State, int]] = None,
            district: Optional[str] = None) -> Address:
        """Adds an address record to the database."""
        select = (
            (Address.street == street)
            & (Address.house_number == house_number)
            & (Address.zip_code == zip_code)
            & (Address.city == city)
        )

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
    def find(cls, pattern: str) -> ModelSelect:
        """Finds an address."""
        return cls.select(cascade=True).where(
            (cls.street ** (pattern := f'%{pattern}%'))
            | (cls.house_number ** pattern)
            | (cls.zip_code ** pattern)
            | (cls.city ** pattern)
        )

    @classmethod
    def from_json(cls, json: dict) -> Address:
        """Returns an address from the respective dictionary."""
        state = json.pop('state', None)
        record = super().from_json(json)

        if state is not None:
            try:
                record.state, *ambiguous = State.find(state)
            except ValueError:
                raise State.DoesNotExist() from None

            if ambiguous:
                raise ValueError('Ambiguous state.')

        return record

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects addresses."""
        if not cascade:
            return super().select(*args, **kwargs)

        return super().select(cls, State, Country, *args, **kwargs).join(
            State, join_type=JOIN.LEFT_OUTER).join(
            Country, join_type=JOIN.LEFT_OUTER)

    @property
    def street_houseno(self) -> str:
        """Returns street and hounse number."""
        return f'{self.street} {self.house_number}'

    @property
    def city_district(self) -> str:
        """Returns the city and district."""
        if self.district:
            return f'{self.city} - {self.district}'

        return self.city

    @property
    def zip_code_city(self) -> str:
        """Returns ZIP code and city."""
        return f'{self.zip_code} {self.city_district}'

    @property
    def oneliner(self) -> str:
        """Returns a one-liner string."""
        return f'{self.street_houseno}, {self.zip_code_city}'

    @property
    def lines(self) -> Iterator[str]:
        """Yields lines for multi-line representation."""
        yield self.street_houseno
        yield self.zip_code_city

        if not self.state:
            return

        if (country := self.state.country.name) not in GERMANY:
            yield country

    @property
    def text(self) -> str:
        """Converts the Address to a multi-line string."""
        return '\n'.join(self.lines)

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.street, self.house_number, self.zip_code,
                self.city, self.district, self.state_id)


class Company(MDBModel):
    """Represents companies HOMEINFO has relations to."""

    name = CharField(255)
    abbreviation = CharField(16, null=True)
    address = ForeignKeyField(Address, column_name='address', null=True,
                              lazy_load=False)
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
    def find(cls, pattern: str) -> ModelSelect:
        """Finds companies by primary key or name."""
        condition = cls.name ** f'%{pattern}%'
        condition |= cls.abbreviation ** f'%{pattern}%'
        condition |= cls.annotation ** f'%{pattern}%'
        return cls.select(cascade=True).where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects companies."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Address, State, Country, *args}
        return super().select(*args, **kwargs).join(
            Address, join_type=JOIN.LEFT_OUTER
        ).join(
            State, join_type=JOIN.LEFT_OUTER
        ).join(
            Country, join_type=JOIN.LEFT_OUTER
        )

    @property
    def departments(self) -> set[Department]:
        """Returns the company's departments."""
        departments = set()

        for employee in self.employees:
            departments.add(employee.department)

        return departments

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.name, self.abbreviation, self.address_id,
                self.annotation)


class Department(MDBModel):
    """Departments of companies."""

    name = CharField(64)
    type = CharField(64, null=True)

    def __str__(self):  # pylint: disable=E0307
        """Returns the department's name."""
        return self.name

    @classmethod
    def find(cls, pattern: str) -> ModelSelect:
        """Finds a department."""
        condition = cls.name ** f'%{pattern}%'
        condition |= cls.type * f'%{pattern}%'
        return cls.select().where(condition)

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.name, self.type)


class Employee(MDBModel):
    """Employees."""

    company = ForeignKeyField(Company, column_name='company',
                              backref='employees', lazy_load=False)
    department = ForeignKeyField(Department, column_name='department',
                                 backref='staff', lazy_load=False)
    first_name = CharField(32, null=True)
    surname = CharField(32)
    phone = CharField(32, null=True)
    cellphone = CharField(32, null=True)
    email = CharField(64, null=True)
    phone_alt = CharField(32, null=True)
    fax = CharField(32, null=True)
    address = ForeignKeyField(Address, column_name='address', null=True,
                              lazy_load=False)

    def __str__(self):
        """Returns the employee's name."""
        if self.first_name is not None:
            return f'{self.first_name} {self.surname}'

        return self.surname

    @classmethod
    def find(cls, pattern: str) -> ModelSelect:
        """Finds an employee."""
        condition = cls.surname ** f'%{pattern}%'
        condition |= cls.first_name ** f'%{pattern}%'
        return cls.select(cascade=True).where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects employees."""
        if not cascade:
            return super().select(*args, **kwargs)

        personal_address = Address.alias()
        args = {
            cls, Company, Address, State, Country, Department,
            personal_address, *args
        }
        return super().select(*args, **kwargs).join(
            Company).join(
            Address, join_type=JOIN.LEFT_OUTER).join(
            State, join_type=JOIN.LEFT_OUTER).join(
            Country, join_type=JOIN.LEFT_OUTER
        ).join_from(cls, Department).join_from(
            cls, personal_address, on=cls.address == personal_address.id,
            join_type=JOIN.LEFT_OUTER
        )

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.company_id, self.department_id, self.first_name,
                self.surname, self.phone, self.cellphone, self.email,
                self.phone_alt, self.fax, self.address_id)


class Customer(MDBModel):
    """CRM's customer(s)."""

    id = IntegerField(primary_key=True)
    company = ForeignKeyField(Company, column_name='company', lazy_load=False,
                              backref='customers')
    reseller = ForeignKeyField('self', column_name='reseller', lazy_load=False,
                               null=True, backref='resellees')
    annotation = CharField(255, null=True)

    def __str__(self):
        """Returns the customer's full name."""
        return self.name

    def __repr__(self):
        """Returns the customer's ID."""
        return str(self.id)

    @classmethod
    def find(cls, pattern: str) -> ModelSelect:
        """Finds a customer by the provided pattern."""
        try:
            cid = int(pattern)
        except ValueError:
            condition = Company.abbreviation ** pattern
            condition |= Company.name ** f'%{pattern}%'
        else:
            condition = Customer.id == cid

        return cls.select(cascade=True).where(condition)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects customers."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Company, Address, State, Country, *args}
        return super().select(*args, **kwargs).join(
            Company).join(
            Address, join_type=JOIN.LEFT_OUTER).join(
            State, join_type=JOIN.LEFT_OUTER).join(
            Country, join_type=JOIN.LEFT_OUTER
        )

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

    def to_csv(self) -> tuple[str]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.company.id, self.company.name, self.reseller_id,
                self.annotation)


class Tenement(MDBModel):   # pylint: disable=R0903
    """A tenement."""

    customer = ForeignKeyField(Customer, column_name='customer',
                               lazy_load=False)
    address = ForeignKeyField(Address, column_name='address', lazy_load=False)
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

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects tenements."""
        if not cascade:
            return super().select(*args, **kwargs)

        customer_address = Address.alias()
        customer_state = State.alias()
        customer_country = Country.alias()
        args = {
            cls, Customer, customer_address, customer_state, customer_country,
            Company, Address, State, Country, *args
        }
        return super().select(*args, **kwargs).join(
            Customer).join(Company).join_from(
            cls, customer_address, join_type=JOIN.LEFT_OUTER).join(
            customer_state, join_type=JOIN.LEFT_OUTER).join(
            customer_country, join_type=JOIN.LEFT_OUTER).join_from(
            cls, Address).join(State, join_type=JOIN.LEFT_OUTER).join(
            Country, join_type=JOIN.LEFT_OUTER)

    def to_csv(self) -> tuple[Union[int, str]]:
        """Returns a tuple of corresponsing values."""
        return (self.id, self.customer_id, self.address_id, self.rental_unit,
                self.living_unit, self.annotation)

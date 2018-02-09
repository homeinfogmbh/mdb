"""HOMEINFO's CRM database."""

from peewee import PrimaryKeyField, CharField, ForeignKeyField

from configlib import INIParser
from peeweeplus import MySQLDatabase, JSONModel
from strflib import l2lang

__all__ = [
    'AlreadyExists',
    'Country',
    'State',
    'Address',
    'Company',
    'Department',
    'Employee',
    'Customer',
    'Tenement']


CONFIG = INIParser('/etc/crm.conf')
DATABASE = MySQLDatabase(
    CONFIG['db']['db'], host=CONFIG['db']['host'], user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'], closing=True)


class AlreadyExists(Exception):
    """Indicates that a certainr record already exists."""

    def __init__(self, record, **keys):
        """Sets the record and key."""
        super().__init__((record, keys))
        self.record = record
        self.keys = keys

    def __str__(self):
        """Prints record and keys."""
        keys_string = self.keys_string

        if keys_string:
            return '{} already exists for {}.'.format(
                self.record.__class__.__name__, keys_string)

        return '{} already exists.'.format(self.record.__class__.__name__)

    @property
    def keys_string(self):
        """Returns the keys string."""
        return l2lang([
            '{}={}'.format(key, value) for key, value in self.keys.items()])


class CRMModel(JSONModel):
    """Generic HOMEINFO CRM Model."""

    class Meta:
        """Database and schema configuration."""
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()

    def __repr__(self):
        """Returns the model's ID as per default."""
        return str(self.id)


class Country(CRMModel):
    """Countries."""

    # An *exactly* two characters long ISO 3166-2 country code
    iso = CharField(2)
    name = CharField(64)
    original_name = CharField(64, null=True, default=None)

    def __str__(self):
        """Converts the country to a string."""
        return self.name

    def __repr__(self):
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern):
        """Finds countries by patterns."""
        pattern = pattern.lower()

        for country in cls:
            if pattern in country.iso.lower():
                yield country
            elif pattern in country.name.lower():
                yield country
            elif pattern in country.original_name.lower():
                yield country


class State(CRMModel):
    """States within countries."""

    country = ForeignKeyField(
        Country, db_column='country', related_name='states')
    # An *exactly* two characters long ISO 3166-2 state code.
    iso = CharField(2)
    name = CharField(64)

    def __str__(self):
        """Returns the country's name."""
        return self.name

    def __repr__(self):
        """Returns the ISO code."""
        return self.iso

    @classmethod
    def find(cls, pattern):
        """Finds a state by the provided pattern."""
        try:
            country = int(pattern)
        except ValueError:
            if len(pattern) == 2:
                for state in cls.select().where(cls.iso == pattern):
                    yield state
            else:
                pattern = pattern.lower()

                for state in cls:
                    if pattern in state.name.lower():
                        yield state
        else:
            for state in cls.select().where(cls.country == country):
                yield state

    @property
    def iso3166(self):
        """Returns the full ISO 3166-2 compliant code."""
        return '{}-{}'.format(self.country.iso, self.iso)


class Address(CRMModel):
    """Address data."""

    street = CharField(64, null=True)
    house_number = CharField(8, null=True)
    zip_code = CharField(32, null=True)
    po_box = CharField(32, null=True)
    city = CharField(64)
    state = ForeignKeyField(State, db_column='state', null=True)

    def __repr__(self):
        """Converts the Address to a one-line string."""
        if self.po_box:
            return '{} {}'.format(self.po_box, self.city)

        if self.street:
            street_houseno = self.street

            if self.house_number:
                street_houseno += ' ' + self.house_number
        else:
            street_houseno = None

        if self.zip_code:
            zip_code_city = ' '.join((self.zip_code, self.city))
        else:
            zip_code_city = self.city

        if street_houseno:
            return ', '.join((street_houseno, zip_code_city))

        return zip_code_city

    def __str__(self):
        """Converts the Address to a string."""
        result = ''

        if self.po_box:
            result += 'Postfach {}\n'.format(self.po_box)
        elif self.street:
            if self.house_number:
                result += '{} {}\n'.format(self.street, self.house_number)
            else:
                result += '{}\n'.format(self.street)

        if self.zip_code:
            result += '{} {}\n'.format(self.zip_code, self.city)

        state = self.state

        if state:
            country_name = str(self.state.country)

            if country_name not in ['Deutschland', 'Germany', 'DE']:
                result += '{}\n'.format(country_name)

        return result

    @classmethod
    def add_by_address(cls, address, state=None):
        """Adds a new address by a complete address."""
        street, house_number, zip_code, city = address
        state_expression = True if state is None else cls.state == state

        try:
            return Address.get(
                (Address.city == city) & (Address.street == street)
                & (Address.house_number == house_number)
                & (Address.zip_code == zip_code) & state_expression)
        except Address.DoesNotExist:
            address = Address()
            address.city = city
            address.street = street
            address.house_number = house_number
            address.zip_code = zip_code
            address.state = state
            address.save()
            return address

    @classmethod
    def add_by_po_box(cls, po_box, city, state=None):
        """Adds an address by a PO box."""
        state_expression = True if state is None else cls.state == state

        try:
            return Address.get(
                (Address.po_box == po_box) & (Address.city == city)
                & state_expression)
        except Address.DoesNotExist:
            address = Address()
            address.po_box = po_box
            address.city = city
            address.state = state
            address.save()
            return address

    @classmethod
    def add(cls, city, po_box=None, addr=None, state=None):
        """Adds an address record to the database.

        Usage:
            * Add address with either po_box or addr parameter.
            * addr must be a tuple: (<street>, <house_number>, <zip_code>).
        """
        po_box_addr_xor_err = ValueError('Must specify either po_box or addr')

        if po_box is None and addr is None:
            raise po_box_addr_xor_err
        elif po_box is not None and addr is not None:
            raise po_box_addr_xor_err
        elif addr is not None:
            try:
                street, house_number, zip_code = addr
            except ValueError:
                raise ValueError(
                    'addr must be (street, house_number, zip_code)')
            else:
                address = (street, house_number, zip_code, city)
                return cls.add_by_address(address, state=state)
        elif po_box is not None:
            return cls.add_by_po_box(po_box, city, state=state)

        raise po_box_addr_xor_err

    @classmethod
    def find(cls, pattern):
        """Finds an address."""
        pattern = pattern.lower()

        for address in cls:
            if address.street is not None:
                if pattern in address.street.lower():
                    yield address
                    continue

            if address.house_number is not None:
                if pattern in address.house_number.lower():
                    yield address
                    continue

            if address.zip_code is not None:
                if pattern in address.zip_code.lower():
                    yield address
                    continue

            if address.po_box is not None:
                if pattern in address.po_box.lower():
                    yield address
                    continue

            if pattern in address.city.lower():
                yield address


class Company(CRMModel):
    """Represents companies HOMEINFO has relations to."""

    name = CharField(255)
    abbreviation = CharField(16, null=True, default=None)
    address = ForeignKeyField(Address, db_column='address', null=True)
    annotation = CharField(256, null=True)

    def __str__(self):
        """Returns the company's name."""
        return self.name

    @classmethod
    def add(cls, name, abbreviation=None, address=None, annotation=None):
        """Adds a new company."""
        try:
            company = cls.get(cls.name == name)
        except cls.DoesNotExist:
            company = cls()
            company.name = name
            company.abbreviation = abbreviation
            company.address = address
            company.annotation = annotation
            company.save()
            return company

        raise AlreadyExists(company, name=name)

    @classmethod
    def find(cls, pattern):
        """Finds companies by primary key or name."""
        return cls.select().where(
            (cls.name ** '%{}%'.format(pattern))
            | (cls.abbreviation ** pattern)
            | (cls.annotation ** '%{}%'.format(pattern)))

    @property
    def departments(self):
        """Returns the company's departments."""
        departments = set()

        for employee in self.employees:
            departments.add(employee.department)

        return departments


class Department(CRMModel):
    """Departments of companies."""

    name = CharField(64)
    type = CharField(64, null=True)

    def __str__(self):
        """Returns the department's name."""
        return self.name

    @classmethod
    def find(cls, pattern):
        """Finds a department."""
        pattern = pattern.lower()

        for department in cls:
            if pattern in department.name.lower():
                yield department
            elif department.type is not None:
                if pattern in department.type.lower():
                    yield department


class Employee(CRMModel):
    """Employees."""

    company = ForeignKeyField(
        Company, db_column='company',
        related_name='employees')
    department = ForeignKeyField(
        Department, db_column='department',
        related_name='staff')
    first_name = CharField(32, null=True)
    surname = CharField(32)
    phone = CharField(32, null=True)
    cellphone = CharField(32, null=True)
    email = CharField(64, null=True)
    phone_alt = CharField(32, null=True)
    fax = CharField(32, null=True)
    address = ForeignKeyField(Address, db_column='address', null=True)

    def __str__(self):
        """Returns the employee's name."""
        if self.first_name is not None:
            return ' '.join([self.first_name, self.surname])

        return self.surname

    @classmethod
    def find(cls, pattern):
        """Finds an employee."""
        pattern = pattern.lower()

        for employee in cls:
            if pattern in employee.surname.lower():
                yield employee
            elif pattern in employee.first_name.lower():
                yield employee


class Customer(CRMModel):
    """CRM's customer(s)."""

    cid = CharField(255)
    company = ForeignKeyField(Company, db_column='company', null=True)
    reseller = ForeignKeyField('self', db_column='reseller', null=True)
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Returns the customer's full name."""
        return self.name

    def __repr__(self):
        """Returns the customer's ID."""
        return ':'.join(customer.cid for customer in self.reselling_chain)

    @classmethod
    def add(cls, cid, company=None, reseller=None, annotation=None):
        """Adds a new customer."""
        customer = cls()
        customer.cid = str(cid)
        customer.company = company
        customer.reseller = reseller
        customer.annotation = annotation
        customer.save()
        return customer

    @classmethod
    def find(cls, pattern):
        """Finds a customer by the provided pattern."""
        return cls.select().join(Company).where(
            (cls.cid == pattern) | (Company.abbreviation ** pattern)
            | (Company.name ** '%{}%'.format(pattern)))

    @classmethod
    def by_reseller(cls, reseller):
        """Yields customers by reseller."""
        if reseller is None:
            return cls.select().where(cls.reseller >> None)

        return cls.select().where(cls.reseller == reseller)

    @property
    def name(self):
        """Returns the customer's name."""
        return self.company.name

    @property
    def reselling_chain(self):
        """Returns the reselling chain."""
        yield self
        reseller = self

        for reseller in iter(lambda: reseller.reseller, None):
            yield reseller

    def to_dict(self, *args, company=True, cascade=False, **kwargs):
        """Converts the customer to a JSON-ish dictionary."""
        dictionary = super().to_dict(*args, **kwargs)

        if company and self.company is not None:
            dictionary['company'] = self.company.to_dict(*args, **kwargs)

        if cascade and self.reseller is not None:
            dictionary['reseller'] = self.reseller.to_dict(
                *args, company=company, cascade=cascade, **kwargs)

        return dictionary


class Tenement(CRMModel):
    """Stores tenements of the respective customers."""

    customer = ForeignKeyField(Customer, db_column='customer')
    address = ForeignKeyField(Address, db_column='address')

    @classmethod
    def add(cls, customer, address):
        """Adds a new tenement."""
        try:
            return cls.get(
                (cls.customer == customer) &
                (cls.address == address))
        except cls.DoesNotExist:
            tenement = cls()
            tenement.customer = customer
            tenement.address = address
            tenement.save()
            return tenement

    @classmethod
    def by_customer(cls, customer):
        """Yields tenements of the respective customer."""
        return cls.select().where(cls.customer == customer)

    def to_dict(self, *args, **kwargs):
        """Returns the tenement as a dictionary."""
        return {
            'customer': self.customer.to_dict(*args, **kwargs),
            'address': self.customer.to_dict(*args, **kwargs)}

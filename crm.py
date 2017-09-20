"""HOMEINFO's CRM DATABASE configuration and models."""

from contextlib import suppress

from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, \
    DoesNotExist

from configlib import INIParser
from peeweeplus import MySQLDatabase
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
    CONFIG['db']['db'],
    host=CONFIG['db']['host'],
    user=CONFIG['db']['user'],
    passwd=CONFIG['db']['passwd'],
    closing=True)


class AlreadyExists(Exception):
    """Indicates that a certainr record already exists"""

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


class CRMModel(Model):
    """Generic HOMEINFO CRM Model"""

    class Meta:
        database = DATABASE
        schema = database.database

    id = PrimaryKeyField()


class Country(CRMModel):
    """Country data"""

    # An *exactly* two characters long ISO 3166-2 state code
    _iso = CharField(2, db_column='iso')
    name = CharField(64)
    original_name = CharField(64, null=True, default=None)

    def __str__(self):
        """Converts the country to a string"""
        return self.name

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

    @property
    def iso(self):
        """Returns the ISO code"""
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the ISO code"""
        if len(iso) == 2:
            self._iso = iso
        else:
            raise ValueError('ISO code must be exactly two characters long')

    def to_dict(self):
        """Returns a JSON-like dictionary"""
        dictionary = {
            'iso': self.iso,
            'name': self.name}

        if self.original_name is not None:
            dictionary['original_name'] = self.original_name

        return dictionary


class State(CRMModel):
    """Country data"""

    country = ForeignKeyField(
        Country, db_column='country',
        related_name='states')
    # An *exactly* two characters long ISO 3166-2 state code
    _iso = CharField(2, db_column='iso')
    name = CharField(64)

    @classmethod
    def find(cls, pattern):
        """Finds a state by the provided pattern."""
        try:
            country = int(pattern)
        except ValueError:
            if len(pattern) == 2:
                for state in cls.select().where(cls._iso == pattern):
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
    def iso(self):
        """Returns the ISO code"""
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the ISO code"""
        if len(iso) == 2:
            self._iso = iso
        else:
            raise ValueError('ISO code must be exactly two characters long')

    @property
    def iso3166(self):
        """Returns the full ISO 3166-2 compliant code"""
        return '{}-{}'.format(self.country.iso, self.iso)

    def to_dict(self):
        """Returns a JSON-like dictionary"""
        return {
            'country': self.country.id,
            'iso': self.iso,
            'name': self.name}


class Address(CRMModel):
    """Address data"""

    street = CharField(64, null=True)
    house_number = CharField(8, null=True)
    zip_code = CharField(32, null=True)
    po_box = CharField(32, null=True)
    city = CharField(64)
    state = ForeignKeyField(State, db_column='state', null=True)

    def __repr__(self):
        """Converts the Address to a one-line string"""
        if self.po_box:
            return '{} {}'.format(self.po_box, self.city)

        return '{} {}, {} {}'.format(
            self.street, self.house_number, self.zip_code, self.city)

    def __str__(self):
        """Converts the Address to a string"""
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

        if state is None:
            try:
                return Address.get(
                    (Address.city == city) &
                    (Address.street == street) &
                    (Address.house_number == house_number) &
                    (Address.zip_code == zip_code))
            except DoesNotExist:
                address = Address()
                address.city = city
                address.street = street
                address.house_number = house_number
                address.zip_code = zip_code
                address.save()
                return address
        else:
            try:
                return Address.get(
                    (Address.city == city) &
                    (Address.street == street) &
                    (Address.house_number == house_number) &
                    (Address.zip_code == zip_code) &
                    (Address.state == state))
            except DoesNotExist:
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
        if state is None:
            try:
                return Address.get(
                    (Address.po_box == po_box) &
                    (Address.city == city))
            except DoesNotExist:
                address = Address()
                address.po_box = po_box
                address.city = city
                address.save()
                return address
        else:
            try:
                return Address.get(
                    (Address.po_box == po_box) &
                    (Address.city == city) &
                    (Address.state == state))
            except DoesNotExist:
                address = Address()
                address.po_box = po_box
                address.city = city
                address.state = state
                address.save()
                return address

    @classmethod
    def add(cls, city, po_box=None, addr=None, state=None):
        """Adds an address record to the DATABASE
        Usage:
            * Add address with either po_box or addr parameter
            * addr must be a tuple: (<street>, <house_number>, <zip_code>)
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
        else:
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

    def to_dict(self, cascade=False):
        """Returns a JSON-like dictionary"""
        dictionary = {'city': self.city}

        if self.street is not None:
            dictionary['street'] = self.street

        if self.house_number is not None:
            dictionary['house_number'] = self.house_number

        if self.zip_code is not None:
            dictionary['zip_code'] = self.zip_code

        if self.po_box is not None:
            dictionary['po_box'] = self.po_box

        if self.state is not None:
            if cascade:
                dictionary['state'] = self.state.to_dict()
            else:
                dictionary['state'] = self.state.iso

        return dictionary


class Company(CRMModel):
    """A company"""

    name = CharField(64)
    address = ForeignKeyField(Address, db_column='address', null=True)
    annotation = CharField(256, null=True)

    def __str__(self):
        """Returns the company's name"""
        return self.name

    @classmethod
    def add(cls, name, address=None, annotation=None):
        """Adds a new company"""
        try:
            company = cls.get(cls.name == name)
        except DoesNotExist:
            company = cls()
            company.name = name
            company.address = address
            company.annotation = annotation
            company.save()
            return company
        else:
            raise AlreadyExists(company, name=name) from None

    @classmethod
    def find(cls, pattern):
        """Finds companies by primary key or name"""
        try:
            ident = int(pattern)
        except ValueError:
            pattern = pattern.lower()

            for company in cls:
                if pattern in company.name.lower():
                    yield company
        else:
            with suppress(DoesNotExist):
                yield cls.get(cls.id == ident)

    @property
    def departments(self):
        """Returns the company's departments"""
        departments = set()

        for employee in self.employees:
            departments.add(employee.department)

        return departments

    @property
    def resales(self):
        """Yields customers this customer resells"""
        return Customer.select().where(Customer.reseller == self)

    def to_dict(self, cascade=False):
        """Returns a JSON-like dictionary"""
        dictionary = {'name': self.name}

        if self.address is not None:
            if cascade:
                dictionary['address'] = self.address.to_dict(cascade=cascade)
            else:
                dictionary['address'] = str(self.address)

        if self.address is not None:
            dictionary['annotation'] = self.annotation

        return dictionary


class Department(CRMModel):
    """Departments of companies"""

    name = CharField(64)
    type = CharField(64, null=True)

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

    def to_dict(self):
        """Returns a JSON-like dictionary"""
        dictionary = {'name': self.name}

        if self.type is not None:
            dictionary['type'] = self.type

        return dictionary


class Employee(CRMModel):
    """Employees"""

    company = ForeignKeyField(
        Company, db_column='company',
        related_name='employees')
    department = ForeignKeyField(
        Department, db_column='department',
        related_name='staff')
    first_name = CharField(32, null=True)
    surname = CharField(32)
    phone = CharField(32)
    cellphone = CharField(32, null=True)
    email = CharField(64, null=True)
    phone_alt = CharField(32, null=True)
    fax = CharField(32, null=True)
    address = ForeignKeyField(Address, db_column='address', null=True)

    @classmethod
    def find(cls, pattern):
        """Finds an employee."""
        pattern = pattern.lower()

        for employee in cls:
            if pattern in employee.surname.lower():
                yield employee
            elif pattern in employee.first_name.lower():
                yield employee

    def __str__(self):
        """Returns the employee's name"""
        if self.first_name is not None:
            return ' '.join([self.first_name, self.surname])

        return self.surname

    def to_dict(self):
        """Returns a JSON-like dictionary"""
        dictionary = {
            'surname': self.surname,
            'phone': self.phone}

        if self.company is not None:
            dictionary['company'] = self.company.id

        if self.department is not None:
            dictionary['department'] = self.department.id

        if self.first_name is not None:
            dictionary['first_name'] = self.first_name

        if self.cellphone is not None:
            dictionary['cellphone'] = self.cellphone

        if self.email is not None:
            dictionary['email'] = self.email

        if self.phone_alt is not None:
            dictionary['phone_alt'] = self.phone_alt

        if self.fax is not None:
            dictionary['fax'] = self.fax

        if self.address is not None:
            dictionary['address'] = self.address.id

        return dictionary


class Customer(CRMModel):
    """CRM's customer(s)"""

    company = ForeignKeyField(
        Company, db_column='company', related_name='customers')
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Returns the customer's full name"""
        return self.name

    def __repr__(self):
        """Returns the customer's ID"""
        return str(self.id)

    @classmethod
    def add(cls, cid, company, annotation=None):
        """Adds a new customer"""
        customer = cls()
        cls._meta.auto_increment = False

        try:
            customer.id = int(cid)
        except (ValueError, TypeError):
            cls._meta.auto_increment = True
            force_insert = False
        else:
            force_insert = True

        customer.company = company
        customer.annotation = annotation
        customer.save(force_insert=force_insert)
        return customer

    @classmethod
    def find(cls, pattern):
        """Finds a customer by the provided pattern."""
        try:
            cid = int(pattern)
        except ValueError:
            pattern = pattern.lower()

            for customer in Customer:
                if pattern in customer.name.lower():
                    yield customer
        else:
            with suppress(DoesNotExist):
                yield Customer.get(Customer.id == cid)

    @property
    def name(self):
        """Returns the customer's name."""
        return self.company.name

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'annotation': self.annotation}


class Tenement(CRMModel):
    """Stores tenements of the respective customers"""

    customer = ForeignKeyField(Customer, db_column='customer')
    address = ForeignKeyField(Address, db_column='address')

    @classmethod
    def add(cls, customer, address):
        """Adds a new tenement"""
        try:
            return cls.get(
                (cls.customer == customer) &
                (cls.address == address))
        except DoesNotExist:
            tenement = cls()
            tenement.customer = customer
            tenement.address = address
            tenement.save()
            return tenement

    @classmethod
    def by_customer(cls, customer):
        """Yields tenements of the respective customer"""
        return cls.select().where(cls.customer == customer)

    def to_dict(self):
        """Returns the tenement as a dictionary"""
        return self.address.to_dict()

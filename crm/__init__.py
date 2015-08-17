"""HOMEINFO's CRM database configuration and models"""

from hashlib import sha256
from configparser import ConfigParser
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField,\
    ForeignKeyField, DoesNotExist, create, IntegerField

__all__ = ['Country', 'State', 'Address', 'Company', 'Department',
           'CompanyDepartments', 'Employee', 'Customer']


class CRMModel(Model):
    """Generic HOMEINFO CRM Model"""

    class Meta:
        database = MySQLDatabase(
            'homeinfo_crm',
            host='localhost',
            user='homeinfo_crm',
            passwd='Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W',
            closing=True)
        schema = database.database

    id = PrimaryKeyField()
    """The table's primary key"""


@create
class Country(CRMModel):
    """Country data"""

    # An *exactly* two characters long ISO 3166-2 state code
    _iso = CharField(2, db_column='iso')
    name = CharField(64)
    original_name = CharField(64, null=True)

    def __str__(self):
        """Converts the country to a string"""
        return self.name

    @property
    def iso(self):
        """Returns the ISO code"""
        return self._iso

    @iso.setter
    def iso(self, iso):
        """Sets the ISO code"""
        if len(iso) is 2:
            self._iso = iso
        else:
            raise ValueError('ISO code must be exactly two characters long')


@create
class State(CRMModel):
    """Country data"""

    country = ForeignKeyField(
        Country, db_column='country',
        related_name='states')
    # An *exactly* two characters long ISO 3166-2 state code
    _iso = CharField(2, db_column='iso')
    name = CharField(64)

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
        return '{0}-{1}'.format(self.country.iso, self.iso)


@create
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
            return '{0} {1}'.format(self.po_box, self.city)
        else:
            return '{0} {1}, {2} {3}'.format(
                self.street, self.house_number,
                self.zip_code, self.city)

    def __str__(self):
        """Converts the Address to a string"""
        result = ''
        if self.po_box:
            result += 'Postfach {0}\n'.format(self.po_box)
        elif self.street:
            if self.house_number:
                result += '{0} {1}\n'.format(self.street, self.house_number)
            else:
                result += '{0}\n'.format(self.street)
        if self.zip_code:
            result += '{0} {1}\n'.format(self.zip_code, self.city)
        state = self.state
        if state:
            country_name = str(self.state.country)
            if country_name not in ['Deutschland', 'Germany', 'DE']:
                result += '{0}\n'.format(country_name)
        return result

    @classmethod
    def add(cls, city, po_box=None, addr=None, state=None):
        """Adds an address record to the database
        Usage:
            * Add address with either po_box or addr parameter
            * addr must be a tuple: (<street>, <house_number>, <zip_code>)
        """
        if po_box is None and addr is None:
            raise ValueError('Must specify either po_box or addr')
        elif po_box is not None and addr is not None:
            raise ValueError('Must specify either po_box or addr')
        elif addr is not None:
            street, house_number, zip_code = addr
            if state is None:
                try:
                    address = Address.get(
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
                    address = Address.get(
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
        elif po_box is not None:
            if state is None:
                try:
                    address = Address.get(Address.po_box == po_box)
                except DoesNotExist:
                    address = Address()
                    address.po_box = po_box
                    address.save()
                return address
            else:
                try:
                    address = Address.get(
                        (Address.po_box == po_box) &
                        (Address.state == state))
                except DoesNotExist:
                    address = Address()
                    address.po_box = po_box
                    address.state = state
                    address.save()
                return address
        else:
            raise ValueError('Must specify either po_box or addr')


@create
class Company(CRMModel):
    """A company"""

    name = CharField(64)
    address = ForeignKeyField(Address, db_column='address', null=True)
    annotation = CharField(256, null=True)

    @property
    def departments(self):
        """Yields the companie's departments"""
        for company_department in CompanyDepartments.select().where(True):
            yield company_department.department


@create
class Department(CRMModel):
    """Departments of companies"""

    name = CharField(64)
    type = CharField(64, null=True)


@create
class CompanyDepartments(CRMModel):
    """Department <-> Company mappings"""

    class Meta:
        db_table = 'company_departments'

    company = ForeignKeyField(
        Company, db_column='company',
        related_name='_departments')
    department = ForeignKeyField(
        Department, db_column='department',
        related_name='_companies')


@create
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

    def __str__(self):
        """Returns the employee's name"""
        if self.first_name is not None:
            return ' '.join([self.first_name, self.surname])
        else:
            return self.surname


@create
class Customer(CRMModel):
    """CRM's customer(s)"""

    company = ForeignKeyField(Company, related_name='customers')
    piwik_tracking_id = IntegerField(null=True)

    def __str__(self):
        """Returns the customer's full name"""
        return self.name

    def __repr__(self):
        """Returns the customer's ID"""
        return str(self.id)

    @property
    def sha256name(self):
        """Returns the SHA-256 encoded CID"""
        return str(sha256(str(self.id).encode()).hexdigest())

    @property
    def name(self):
        """Returns the customer's name"""
        return str(self.company.name) if self.company else ''

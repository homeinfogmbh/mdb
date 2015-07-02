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
            passwd='Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W')
        schema = database.database

    id = PrimaryKeyField()
    """The table's primary key"""


@create
class Country(CRMModel):
    """Country data"""

    _iso = CharField(2, db_column='iso')
    """An, *exactly* two characters long ISO 3166-2 country code
    example: 'DE'"""
    name = CharField(64)
    """The complete country's name"""
    original_name = CharField(64, null=True)
    """The countrie's name in its original language"""

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

    country = ForeignKeyField(Country, db_column='country',
                              related_name='states')
    """The country this state belongs to"""
    _iso = CharField(2, db_column='iso')
    """An *exactly* two characters long ISO 3166-2 state code
    examples: 'NI' or 'NW'"""
    name = CharField(64)
    """The complete state's name"""

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
        return '-'.join([self.country.iso, self.iso])


@create
class Address(CRMModel):
    """Address data"""

    street = CharField(64, null=True)
    """The street's name"""
    house_number = CharField(8, null=True)
    """The house number"""
    zip_code = CharField(32, null=True)
    """The zip code"""
    po_box = CharField(32, null=True)
    """The po box number"""
    city = CharField(64)
    """The name of the respective city"""
    state = ForeignKeyField(State, db_column='state', null=True)
    """The country of the address"""

    def __str__(self):
        """Converts the Address to a string"""
        result = ''
        if self.po_box:
            result += ''.join(['Postfach', ' ', self.po_box, '\n'])
        elif self.street:
            if self.house_number:
                result += ''.join([self.street, ' ', self.house_number, '\n'])
            else:
                result += ''.join([self.street, '\n'])
        if self.zip_code:
            result += ''.join([self.zip_code, ' ', self.city, '\n'])
        state = self.state
        if state:
            country_name = str(self.state.country)
            if country_name not in ['Deutschland', 'Germany', 'DE']:
                result += ''.join([country_name, '\n'])
        return result

    def __repr__(self):
        """Converts the Address to a one-line string"""
        if self.po_box:
            return ' '.join([self.po_box, self.city])
        else:
            return ', '.join([' '.join([self.street, self.house_number]),
                              ' '.join([self.zip_code, self.city])])

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
                    address = Address.get((Address.city == city) &
                                          (Address.street == street) &
                                          (Address.house_number
                                           == house_number) &
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
                    address = Address.get((Address.city == city) &
                                          (Address.street == street) &
                                          (Address.house_number
                                           == house_number) &
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
                    address = Address.get((Address.po_box == po_box) &
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
    """A representative name"""
    address = ForeignKeyField(Address, db_column='address', null=True)
    """The employee's address"""
    annotation = CharField(256, null=True)
    """Type like 'bank' or 'realtor', etc."""

    @property
    def departments(self):
        """Yields the companie's departments"""
        for company_department in CompanyDepartments.select().where(True):
            yield company_department.department


@create
class Department(CRMModel):
    """Departments of companies"""

    name = CharField(64)
    """A representative name"""
    type = CharField(64, null=True)
    """A type like 'IT', 'customer service', etc."""


@create
class CompanyDepartments(CRMModel):
    """Department <-> Company mappings"""

    class Meta:
        db_table = 'company_departments'

    company = ForeignKeyField(Company, db_column='company',
                              related_name='_departments')
    """The respective company"""
    department = ForeignKeyField(Department, db_column='department',
                                 related_name='_companies')
    """The respective department"""


@create
class Employee(CRMModel):
    """Employees"""

    company = ForeignKeyField(Company, db_column='company',
                              related_name='employees')
    """The company, the employee is working for"""
    department = ForeignKeyField(Department, db_column='department',
                                 related_name='staff')
    """The department this employee is working in"""
    first_name = CharField(32, null=True)
    """The employee's first name"""
    surname = CharField(32)
    """The employee's surname"""
    phone = CharField(32)
    """The employee's phone number"""
    cellphone = CharField(32, null=True)
    """The employee's cell phone number"""
    email = CharField(64, null=True)
    """The employee's email address"""
    phone_alt = CharField(32, null=True)
    """An alternative phone number"""
    fax = CharField(32, null=True)
    """The employee's fax number"""
    address = ForeignKeyField(Address, db_column='address', null=True)
    """The employee's address"""


@create
class Customer(CRMModel):
    """CRM's customer(s)"""

    company = ForeignKeyField(Company, related_name='customers')
    """A related company"""
    piwik_tracking_id = IntegerField(null=True)
    """Legacy tracking ID of the old PIWIK system"""

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

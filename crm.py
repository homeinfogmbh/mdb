"""HOMEINFO's CRM database configuration and models"""

from hashlib import sha256
from peewee import Model, PrimaryKeyField, CharField, ForeignKeyField, \
    DoesNotExist

from homeinfo.peewee import MySQLDatabase

__all__ = [
    'Country',
    'State',
    'Address',
    'Company',
    'Department',
    'Employee',
    'Customer']


class CRMModel(Model):
    """Generic HOMEINFO CRM Model"""

    class Meta:
        database = MySQLDatabase(
            'crm',
            host='localhost',
            user='crm',
            passwd='Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W',
            closing=True)
        schema = database.database

    id = PrimaryKeyField()


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
            result += 'Postfach {}\n'.format(self.po_box)
        elif self.street:
            if self.house_number:
                result += '{0} {1}\n'.format(self.street, self.house_number)
            else:
                result += '{}\n'.format(self.street)

        if self.zip_code:
            result += '{0} {1}\n'.format(self.zip_code, self.city)

        state = self.state

        if state:
            country_name = str(self.state.country)

            if country_name not in ['Deutschland', 'Germany', 'DE']:
                result += '{}\n'.format(country_name)

        return result

    @classmethod
    def add(cls, city, po_box=None, addr=None, state=None):
        """Adds an address record to the database
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
            raise po_box_addr_xor_err


class Company(CRMModel):
    """A company"""

    name = CharField(64)
    address = ForeignKeyField(Address, db_column='address', null=True)
    annotation = CharField(256, null=True)

    @classmethod
    def find(cls, id_or_name):
        """Finds companies by primary key or name"""
        try:
            ident = int(id_or_name)
        except ValueError:
            return cls.get(cls.name == id_or_name)
        else:
            return cls.get(cls.id == ident)

    @property
    def departments(self):
        """Returns the company's departments"""
        departments = set()
        for employee in self.employees:
            departments.add(employee.department)
        return departments


class Department(CRMModel):
    """Departments of companies"""

    name = CharField(64)
    type = CharField(64, null=True)


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
    def find(cls, id_or_company_name):
        """Finds customers by primary key or company name"""
        try:
            ident = int(id_or_company_name)
        except ValueError:
            return cls.get(cls.company == Company.find(id_or_company_name))
        else:
            return cls.get(cls.id == ident)

    @property
    def sha256name(self):
        """Returns the SHA-256 encoded CID"""
        return str(sha256(str(self.id).encode()).hexdigest())

    @property
    def name(self):
        """Returns the customer's name"""
        return str(self.company.name) if self.company else ''

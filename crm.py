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
    'Customer',
    'Tenement']


database = MySQLDatabase(
    'crm',
    host='localhost',
    user='crm',
    passwd='Z"XO;$2K+>XEo}jK>6-+}|U@,|E/6_&W',
    closing=True)


class CRMModel(Model):
    """Generic HOMEINFO CRM Model"""

    class Meta:
        database = database
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

    def __str__(self):
        """Returns the employee's name"""
        if self.first_name is not None:
            return ' '.join([self.first_name, self.surname])
        else:
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

    reseller = ForeignKeyField(Company, db_column='reseller')
    company = ForeignKeyField(
        Company, db_column='company', related_name='customers')
    # Customer ID assigned by reseller to customer
    cid = CharField(255)
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Returns the customer's full name"""
        return self.name

    def __repr__(self):
        """Returns the customer's ID"""
        return str(self.id)

    @classmethod
    def find(cls, key):
        """Finds customers by primary key or company name"""
        try:
            ident = int(key)
        except ValueError:
            try:
                return cls.get(cls.cid == key)
            except DoesNotExist:
                return cls.get(cls.company == Company.find(key))
        else:
            return cls.get(cls.id == ident)

    @property
    def sha256name(self):
        """Returns the SHA-256 encoded CID"""
        return sha256(self.cid.encode()).hexdigest()

    @property
    def name(self):
        """Returns the customer's name"""
        return str(self.company.name) if self.company else ''

    @property
    def resales(self):
        """Yields customers this customer resells"""
        return self.company.resales

    def to_dict(self, cascade=False):
        """Returns a JSON-like dictionary"""
        dictionary = {'cid': self.cid}

        if cascade:
            dictionary['reseller'] = self.reseller.to_dict(cascade=cascade)
            dictionary['company'] = self.company.to_dict(cascade=cascade)
        else:
            dictionary['reseller'] = self.reseller.id
            dictionary['company'] = self.company.id

        if self.annotation is not None:
            dictionary['annotation'] = self.annotation

        return dictionary


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

    def to_dict(self):
        """Returns the tenement as a dictionary"""
        return self.address.to_dict()

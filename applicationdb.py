"""Application database ORM models"""

from datetime import datetime
from peewee import DoesNotExist, Model, PrimaryKeyField, ForeignKeyField, \
    TextField, DateTimeField, BooleanField, IntegerField, CharField, \
    DateField

from configparserplus import ConfigParserPlus
from homeinfo.crm import Address, Customer
from homeinfo.terminals.orm import Terminal
from peeweeplus import MySQLDatabase


__all__ = [
    'Command',
    'Statistics',
    'CleaningUser',
    'CleaningDate',
    'TenantMessage',
    'DamageReport',
    'ProxyHost']

config = ConfigParserPlus('/etc/applicationdb.conf')
database = MySQLDatabase(
    config['db']['db'],
    host=config['db']['host'],
    user=config['db']['user'],
    passwd=config['db']['passwd'],
    closing=True)


class DuplicateUserError(Exception):
    """Indicates a duplicate user entry"""

    pass


class ApplicationModel(Model):
    """Abstract common model"""

    class Meta:
        database = database
        schema = database.database

    id = PrimaryKeyField()


class Command(ApplicationModel):
    """Command entries"""

    customer = ForeignKeyField(Customer, db_column='customer')
    vid = IntegerField()
    task = CharField(16)
    created = DateTimeField()
    completed = DateTimeField(null=True, default=None)

    @classmethod
    def add(cls, customer, vid, task):
        """Creates a new task"""
        try:
            return cls.get(
                (cls.customer == customer) & (cls.vid == vid) &
                (cls.task == task))
        except DoesNotExist:
            record = cls()
            record.customer = customer
            record.vid = vid
            record.task = task
            record.created = datetime.now()
            record.save()
            return record

    def complete(self, force=False):
        """Completes the command"""
        if force or self.completed is None:
            self.completed = datetime.now()
            self.save()


class Statistics(ApplicationModel):
    """Usage statistics entries"""

    customer = ForeignKeyField(Customer, db_column='customer')
    vid = IntegerField()
    tid = IntegerField(null=True, default=None)
    document = CharField(255)
    timestamp = DateTimeField()

    @classmethod
    def add(cls, customer, vid, tid, document):
        """Adds a new statistics entry"""
        record = cls()
        record.customer = customer
        record.vid = vid
        record.tid = tid
        record.document = document
        record.timestamp = datetime.now()
        record.save()
        return record

    @property
    def terminal(self):
        """Returns the appropriate terminal"""
        if self.tid is not None:
            return Terminal.by_ids(self.customer.id, self.tid)


class CleaningUser(ApplicationModel):
    """Cleaning users"""

    class Meta:
        db_table = 'cleaning_user'

    name = CharField(64)
    customer = ForeignKeyField(Customer, db_column='customer')
    pin = CharField(4)
    annotation = CharField(255, null=True, default=None)
    created = DateTimeField()
    enabled = BooleanField(default=False)

    @classmethod
    def add(cls, name, customer, pin, annotation=None, enabled=None):
        """Adds a new cleaning user"""
        try:
            cls.get((cls.name == name) & (cls.customer == customer))
        except DoesNotExist:
            record = cls()
            record.name = name
            record.customer = customer
            record.pin = pin
            record.annotation = annotation
            record.created = datetime.now()

            if enabled is not None:
                record.enabled = enabled

            record.save()
            return record
        else:
            raise DuplicateUserError()

    def to_dict(self):
        """Returns a JSON compliant dictionary"""
        return {'name': self.name, 'annotation': self.annotation}


class CleaningDate(ApplicationModel):
    """Cleaning chart entries"""

    class Meta:
        db_table = 'cleaning_date'

    user = ForeignKeyField(CleaningUser, db_column='user')
    address = ForeignKeyField(Address, db_column='address')
    timestamp = DateTimeField()

    @classmethod
    def add(cls, user, address):
        """Adds a new cleaning record"""
        record = cls()
        record.user = user
        record.address = address
        record.timestamp = datetime.now()
        record.save()
        return record

    @classmethod
    def of(cls, address, limit=None):
        """Returns a dictionary for the respective address"""
        cleanings = []

        for n, cleaning_date in enumerate(cls.select().where(
                cls.address == address).order_by(cls.timestamp.desc())):
            if limit is not None and n >= limit:
                break
            else:
                cleanings.append(cleaning_date.to_dict())

        return cleanings

    def to_dict(self, verbose=False):
        """Returns a JSON compliant dictionary"""
        dictionary = {
            'timestamp': self.timestamp.isoformat()}

        if verbose:
            dictionary['user'] = self.user.to_dict()
            dictionary['address'] = self.address.to_dict()
        else:
            dictionary['user'] = self.user.name

        return dictionary


class TenantMessage(ApplicationModel):
    """Tenant to tenant messages"""

    class Meta:
        db_table = 'tenant_message'

    terminal = ForeignKeyField(Terminal, db_column='terminal')
    message = TextField()
    created = DateTimeField()
    released = BooleanField(default=False)
    start_date = DateField(null=True, default=None)
    end_date = DateField(null=True, default=None)

    @classmethod
    def add(cls, terminal, message):
        """Creates a new entry for the respective terminal"""
        record = cls()
        record.terminal = terminal
        record.message = message
        record.created = datetime.now()
        record.save()
        return record


class DamageReport(ApplicationModel):
    """Damage reports"""

    class Meta:
        db_table = 'damage_report'

    terminal = ForeignKeyField(Terminal, db_column='terminal')
    message = TextField()
    name = CharField(255)
    contact = CharField(255, null=True, default=None)
    damage_type = CharField(255)
    timestamp = DateTimeField()

    @classmethod
    def add(cls, terminal, message, name, damage_type, contact=None):
        """Creates a new entry for the respective terminal"""
        record = cls()
        record.terminal = terminal
        record.message = message
        record.name = name
        record.damage_type = damage_type
        record.contact = contact
        record.timestamp = datetime.now()
        record.save()
        return record

    @classmethod
    def from_dict(cls, terminal, dictionary):
        """Creates a new entry from the respective dictionary"""
        return cls.add(
            terminal, dictionary['message'], dictionary['name'],
            dictionary['damage_type'], contact=dictionary.get('contact'))


class ProxyHost(ApplicationModel):
    """Valid proxy hosts"""

    class Meta:
        db_table = 'proxy_hosts'

    hostname = CharField(255)

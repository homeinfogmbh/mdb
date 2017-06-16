"""Application database ORM models"""

from datetime import datetime
from peewee import DoesNotExist, Model, PrimaryKeyField, ForeignKeyField, \
    TextField, DateTimeField, BooleanField, IntegerField, CharField, \
    SmallIntegerField

from homeinfo.crm import Address, Customer
from homeinfo.terminals.orm import Terminal
from peeweeplus import MySQLDatabase


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


class TenantMessage(ApplicationModel):
    """Tenant to tenant messages"""

    terminal = ForeignKeyField(Terminal, db_column='terminal')
    message = TextField()
    created = DateTimeField()
    released = BooleanField(default=False)
    start_date = DateTimeField(null=True, default=None)
    end_date = DateTimeField(null=True, default=None)

    @classmethod
    def add(cls, terminal, message):
        """Creates a new entry for the respective terminal"""
        record = cls()
        record.terminal = terminal
        record.message = message
        record.created = datetime.now()
        record.save()
        return record


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


class CleaningUser(ApplicationModel):
    """Cleaning users"""

    class Meta:
        db_table = 'cleaning_users'

    name = CharField(64)
    customer = ForeignKeyField(Customer, db_column='customer')
    pin = SmallIntegerField()
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


class Cleaning(ApplicationModel):
    """Cleaning chart entries"""

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

    def to_dict(self):
        """Returns a JSON compliant dictionary"""
        return {
            'user': self.user.to_dict(),
            'address': self.address.to_dict(),
            'timestamp': self.timestamp.isoformat()}

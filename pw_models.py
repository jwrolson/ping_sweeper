from peewee import *

database = MySQLDatabase('Discovery', 
                            **{ 'port': 3306,
                                'host': 'localhost', 
                                'user': 'root', 
                                'password': 'toor'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Sweep(BaseModel):
    ip_address = CharField(db_column='IP_Address', primary_key=True)
    timestamp = DateTimeField(db_column='Timestamp')
    hostname = CharField(db_column='Host_Name')

    class Meta:
        db_table = 'Sweep'

from peewee import ForeignKeyField

class Incasator:
    conect = ForeignKeyField(DefaultUser, related_name='Userhelp')
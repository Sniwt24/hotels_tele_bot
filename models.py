from peewee import SqliteDatabase, Model, PrimaryKeyField, BigIntegerField, DateTimeField, TextField


db = SqliteDatabase('history_log.db')


class BaseModel(Model):
    class Meta:
        database = db


class Req(BaseModel):
    request_id = PrimaryKeyField(BigIntegerField(column_name='request_id'))
    user_id = BigIntegerField(column_name='user_id')
    request_time = DateTimeField(column_name='request_time')
    command = TextField(column_name='command')
    city = TextField(column_name='city')
    hotels = TextField(column_name='hotels')

    class Meta:
        table_name = 'req'

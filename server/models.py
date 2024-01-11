from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id= db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    body= db.Column(db.Text, nullable=False)
    created_at= db.Column(db.DateTime, server_default= db.func.now(), nullable=False)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    

import sqlalchemy
from models.enums import RoleType

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255)),
    sqlalchemy.Column("first_name", sqlalchemy.String(150)),
    sqlalchemy.Column("last_name", sqlalchemy.String(150)),
    sqlalchemy.Column("phone", sqlalchemy.String(30)),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), nullable=False,
                      server_default=RoleType.complainer.name),
    sqlalchemy.Column("iban", sqlalchemy.String(200))

)
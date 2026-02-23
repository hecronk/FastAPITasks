import sqlalchemy as sa


class BaseModel(object):

    id =  sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=sa.func.now(), server_default=sa.func.now())

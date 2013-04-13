import database
from sqlalchemy import Column, Integer, String

class SystemConfiguration(database.Base):
    __tablename__ = 'config'

    setting = Column(String(50), primary_key=True)
    value = Column(String(50), nullable=False)

    def __init__(self, setting, value):
        self.setting = setting
        self.value = value

    def __repr__(self):
        return '<Config setting=%r value=%r>' % (
            self.setting,
            self.value
        )

    @classmethod
    def get_setting(cls, setting):
        config_obj = cls.__get(setting)
        return config_obj.value

    @classmethod
    def set_setting(cls, setting, value):
        if cls.__contains(setting):
            config_obj = cls.__get(setting)
            config_obj.value = value
        else:
            SystemConfiguration(setting, value)

    @classmethod
    def __get(cls, setting):
        return cls.query.filter_by(setting=setting).first()

    @classmethod
    def __contains(cls, setting):
        contains = False
        if cls.query.filter_by(setting=setting).first() is not None:
            contains = True
        return contains

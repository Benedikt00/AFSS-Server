
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

class Factory_p1(Base):
    __tablename__ = 'db_factory_p1'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Bauteilname = Column(String(30), nullable=False)
    Kategorisierungen = Column(JSON, nullable=False)
    Platz = Column(String(10), nullable=False)
    Bauteilanzahl = Column(Integer)
    Bauteilanzahl_min = Column(Integer)
    Gewicht_pro_teil_in_g = Column(Integer)
    eingelagert = Column(Integer, server_default="0")
    ausgelagert = Column(Integer, server_default="1")
    wird_eingelagert = Column(Integer, server_default="0")
    wird_ausgelagert = Column(Integer, server_default="0")
    anzahl_auslagerungen = Column(Integer, nullable=False, server_default="0")

    def __init__(self):
        self.max_db_rows = 100
        self.engine = create_engine('mysql://root:112358@localhost:3306/test_db_bauteile')
        Base.metadata.create_all(self.engine)
        
        # Creating a session
        self.session = Session(self.engine)

    @classmethod
    def get_db_keys(cls) -> list[str]:
        keys = [column.key for column in cls.__table__.columns]
        return keys
    
    

    def load_db_all(self) -> list[dict]:
        with Session(self.engine) as session:
            query = session.query(Factory_p1).limit(self.max_db_rows)
            results = query.all()
            return [dict(result.__dict__) for result in results]

# Example of using the SQLAlchemy model


# Example of using the get_db_keys function

_db = Factory_p1()

keys = _db.get_db_keys()
print(keys)

data = _db.load_db_all()
print(data)
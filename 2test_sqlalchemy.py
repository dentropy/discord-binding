import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from schema_sqlalchemy import Base 

# engine_path = "sqlite+pysqlite:///" + "/".join(os.getcwd().split("/")) + "/orm_test.db"
from dotenv import load_dotenv
load_dotenv()
engine_path = os.environ.get("db_url")
engine = create_engine(engine_path, echo=True)


Base.metadata.create_all(engine) 
session = Session(engine)

from schema_sqlalchemy import Guilds
session.add(Guilds("TEST", "TEST", "TEST", "TEST"))
session.add(Guilds("TEST2", "TEST", "TEST", "TEST"))
session.commit()
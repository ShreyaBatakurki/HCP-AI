from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:Root123@localhost/hcp_ai"

engine = create_engine(DATABASE_URL)
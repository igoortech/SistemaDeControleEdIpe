import pyodbc 

DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"

SERVER = "dbipe.database.windows.net"
DB = "ipdb"
USER = "ipeadmin"
PWD = "qwerty123!@#"


drivers = [item for item in pyodbc.drivers()]
driver = drivers[-1]
print("driver:{}".format(driver))

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver={driver}"
IP_PERMITIDO = "127.0.0.1"

#"mssql+pyodbc://dbipe.database.windows.net/ipdb?driver=SQL+Server?UID=ipeadmin;PWD=qwerty123!@#;Encrypt=True;TrustServerCertificate=False" 

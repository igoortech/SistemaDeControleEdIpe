DEBUG = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
CORS_HEADERS = 'Content-Type'
SECRET_KEY = "asdjkgasd$#43"

SERVER = "dbipe.database.windows.net"
DB = "ipdb"
USER = "ipeadmin"
PWD = "qwerty123!@#"

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{USER}:{PWD}@{SERVER}/{DB}?driver=SQL+Server"
IP_PERMITIDO = "200.159.129.201"

#"mssql+pyodbc://dbipe.database.windows.net/ipdb?driver=SQL+Server?UID=ipeadmin;PWD=qwerty123!@#;Encrypt=True;TrustServerCertificate=False" 

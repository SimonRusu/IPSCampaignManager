import os
import pathlib
import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

#Creación de directorios de base de datos si no existen
basedir = pathlib.Path(__file__).parent.resolve()
imagesDir = 'db/campaign_images'
imagesDirPath = os.path.join(basedir, imagesDir)

if not os.path.exists(imagesDirPath):
    os.makedirs(imagesDirPath)

#Configuración de la aplicación
connex_app = connexion.App(__name__, specification_dir=basedir)
app = connex_app.app

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'db' / 'IPSCM.sqlite3'}"
app.config["SQLALCHEMY_BINDS"] = {
    "auxDB": f"sqlite:///{basedir / 'db' /  'auxDB.sqlite3'}"
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

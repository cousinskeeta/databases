from project import create_app
from project import db

application = create_app()
db.create_all(app=application)

if __name__ == "__main__":
    application.run()
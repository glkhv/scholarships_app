from config import *
from models import *
from api import *
from views import *

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

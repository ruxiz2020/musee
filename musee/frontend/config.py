# This file should be included in .gitignore to not store sensitive data in version control
import os
SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


config = {
    "DATABASE_URL" : 'postgresql://zruxi@localhost:5432/musee',
}

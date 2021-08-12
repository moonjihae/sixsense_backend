from flask import Flask
from app.__init__ import create_app

app = create_app('dev')

if __name__ == '__main__':
    app.run()

from flask import Flask
from app.__init__ import create_app
import datetime
import os
app = create_app('dev')

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    serv_path = '/logs/'
    abs_path = os.getcwd()
    directory = abs_path + serv_path
    if not os.path.exists(directory):
        os.makedirs(directory)

    now = datetime.datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    nowDate += '_error.log'
    formatter = logging.Formatter(
        '%(asctime)s - LevelName : %(levelname)s in %(module)s [%(lineno)d]  Message : %(message)s')

    file_handler=RotatingFileHandler(
        directory+nowDate,maxBytes=10485760,backupCount=1)
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
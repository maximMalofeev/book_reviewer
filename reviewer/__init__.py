import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='postgres://btwllvfoiyvmgf:0c8b72031ade0229949bad8d53b7dd4370be1d32b980c097e2576e697c60f378@ec2-46-137-75-170.eu-west-1.compute.amazonaws.com:5432/d3luchuf6f5921'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello!'

    return app
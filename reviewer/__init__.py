import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #DATABASE='reviewer.sqlite'
        DATABASE='postgres://postgres:postgres@127.0.0.1:5432'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello!'

    from reviewer import reviewer, auth
    app.register_blueprint(reviewer.bp)
    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')

    return app
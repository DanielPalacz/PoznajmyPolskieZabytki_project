import os

from flask import Flask
from flask import jsonify

__all__ = ["db", "create_app"]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="templates")
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, 'zabytki.sqlite'),
        INPUT=os.path.join(app.instance_path, 'DANE_ZESTWIENIE_ZRN.csv'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello_b():
        return jsonify("Hello, World (json)!")

    from . import db
    db.init_app(app)

    from . import views
    app.register_blueprint(views.bp)

    return app

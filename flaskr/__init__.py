import os

from flask import Flask, render_template


def create_app(test_config=None):
    """ FACTORY FUNCTION """

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    posts = [
        {
            'author': 'Corey Schafer',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'April 20, 2018'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'April 21, 2018'
        }
    ]

    @app.route('/home')
    @app.route('/')
    def index():
        return render_template('home.html', posts=posts)

    @app.route('/about')
    def about():
        return render_template('about.html', title='ZDAROVA')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import db
    db.init_app(app)

    return app

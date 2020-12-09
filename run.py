from flaskapp import create_app


# if test_config is None:
#     # Load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # Load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass



# from flaskr import auth
# app.register_blueprint(auth.bp)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


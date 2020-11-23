# import os
# from flask import Flask, url_for, request, render_template, flash, redirect, send_from_directory, abort, session
# from werkzeug.utils import secure_filename
# from markupsafe import escape
# from werkzeug.middleware.proxy_fix import ProxyFix
#
# app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET_KEY')
#
# # Middleware
# app.wsgi_app = ProxyFix(app.wsgi_app)
#
# # Upload settings
# UPLOAD_FOLDER = "uploads"
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#
# # Logging
# app.logger.debug('A value for debugging')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @app.route('/')
# def index():
#     if 'username' in session:
#         return f"Logged in as {escape(session['username'])}"
#
#     else:
#         return render_template('index.html')
#
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     # resp = make_response(render_template(...))
#     # resp.set_cookie('username', 'the username')
#
#     username = request.cookies.get('username')
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
#
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
#
#
# @app.route('/hello')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)
#
#
# @app.route('/user/<username>')
# def profile(username):
#     # show the user profile for that user
#     return f"{escape(username)}'s profile"
#
#
# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     # show the post with the given id, the id is an integer
#     return f"Post {post_id}"
#
#
# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#     # show the subpath after /path/
#     return f"Subpath {escape(subpath)}"
#
#
# @app.route('/projects/')
# def projects():
#     return 'The project page'
#
#
# @app.route('/about')
# def about():
#     return 'The about page'
#
#
# # @app.route('/login')
# # def login():
# #     abort(401)
#
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] == '':
#             flash(u'Invalid password provided')
#             error = 'Invalid password provided'
#         else:
#             flash('You were successfully logged in')
#             session['username'] = request.form['username']
#             return redirect(url_for('index'))
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))
#
# # with app.test_request_context():
# #     print(url_for('login'))
# #     print(url_for('login', next='/'))
# #     print(url_for('profile', username='John Doe'))
# #     print(url_for('static', filename='style.css'))
# #     print(get_flashed_messages())

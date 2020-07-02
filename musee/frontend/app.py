import os
from flask import Flask, request, abort, jsonify
from flask import render_template, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from musee.frontend.model import setup_db, KeyWords, db
#from auth import AuthError, requires_auth, requires_signed_in
# from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from musee.frontend.config import config


#AUTH0_DOMAIN = auth0_config['AUTH0_DOMAIN']
#ALGORITHMS = auth0_config['ALGORITHMS']
#AUTH0_AUDIENCE = auth0_config['AUTH0_AUDIENCE']
#AUTH0_CALLBACK_URL = auth0_config['AUTH0_CALLBACK_URL']
#AUTH0_CLIENT_ID = auth0_config['AUTH0_CLIENT_ID']
#AUTH0_CLIENT_SECRET = auth0_config['AUTH0_CLIENT_SECRET']
#AUTH0_BASE_URL = 'https://' + auth0_config['AUTH0_DOMAIN']


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = "super secret key"
    setup_db(app)

    # setup cross origin
    CORS(app)

    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    # oauth = OAuth(app)

    # auth0 = oauth.register(
    #    'auth0',
    #    client_id=AUTH0_CLIENT_ID,
    #    client_secret=AUTH0_CLIENT_SECRET,
    #    api_base_url=AUTH0_BASE_URL,
    #    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    #    authorize_url=AUTH0_BASE_URL + '/authorize',
    #    client_kwargs={
    #        'scope': 'openid profile email',
    #    },
    #)

    # Setup home route

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/callback')
    def callback_handling():
        # Handles response from token endpoint

        # res=auth0.authorize_access_token()
        # token=res.get('access_token')

        # Store the user information in flask session.
        # session['jwt_token']=token

        return redirect('/dashboard')


    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')


    """Single File Keyword Routes"""

    # Route for getting all movies
    @app.route('/singleTexts')
    def get_single_text():
        """Get fingle text keywords route"""

        keywords=KeyWords.query.all()

        return jsonify({
            'success': True,
            'keywords': [keyword.format() for keyword in keywords],
        }), 200

    # Route for getting a specific movie
    @app.route('/singleTexts/<int:id>')
    def get_single_text_by_id(id):
        """Get a specific text route"""
        keyword=KeyWords.query.get(id)

        # return 404 if there is no movie with id
        if keyword is None:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'keyword': keyword.format(),
            }), 200

    @app.route('/singleTexts', methods = ['POST'])
    def post_single_text():
        """Create a single text route"""
        # Process request data
        data=request.get_json()
        url=data.get('url', None)
        keywords=data.get('keywords', None)

        # return 400 for empty title or release date
        if url is None or keywords is None:
            abort(400)

        keyword=KeyWords(url = url)

        try:
            movie.insert()
            return jsonify({
                'success': True,
                'keyword': keyword.format()
            }), 201
        except Exception:
            abort(500)

    @app.route('/singleTexts/<int:id>', methods = ['PATCH'])
    def patch_single_text(id):
        """Update a single text route"""

        data=request.get_json()
        url=data.get('url', None)
        keywords=data.get('keywords', None)

        keyword=KeyWords.query.get(id)

        if keyword is None:
            abort(404)

        if url is None or keywords is None:
            abort(400)

        keyword.url=url
        keyword.keywords=keywords

        try:
            keyword.update()
            return jsonify({
                'success': True,
                'keyword': keyword.format()
            }), 200
        except Exception:
            abort(500)

    @app.route('/singleTexts/<int:id>', methods = ['DELETE'])
    def delete_single_text(id):
        """Delete a single text route"""
        keyword=KeyWords.query.get(id)

        if keyword is None:
            abort(404)
        try:
            keyword.delete()
            return jsonify({
                'success': True,
                'message':
                f'keyword id {keyword.id}, titled {keyword.url} was deleted',
            })
        except Exception:
            db.session.rollback()
            abort(500)


    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500


    return app


APP=create_app()

if __name__ == '__main__':
    APP.run(host = '127.0.0.1', port = 5000, debug = True)

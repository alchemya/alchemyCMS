from flask import Flask,render_template
from apps.cms import bp as cms_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from apps.ueditor import bp as ueditor_bp
from exts import db
from config import DevConfig
from flask_wtf import CSRFProtect
from exts import mail
from utils.captcha import Captcha

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    print(app.config['DEBUG'])
    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)
    CSRFProtect(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('front/404.html'), 404

    return app



if __name__ == '__main__':
    app=create_app()
    app.run(port=8000)


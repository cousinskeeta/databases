from flask import render_template
from . import db
from .main import main as main_blueprint


@main_blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main_blueprint.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

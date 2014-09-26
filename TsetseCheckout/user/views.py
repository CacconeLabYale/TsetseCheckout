# -*- coding: utf-8 -*-
from flask import g
from flask import (Blueprint, request, render_template, flash, url_for, redirect, session, abort)
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from TsetseCheckout import upload_sets
from .models import User, Upload

blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")


@blueprint.before_request
def before_request():
    g.user = current_user


def render_template_or_404(url):
    """
    Wraps flask.render_template in a try: except: abort(404)
    :param url:
    :return:
    """
    try:
        return render_template(url)
    except TemplateNotFound:
        abort(404)


@blueprint.route("/members")
@login_required
def members():
    return render_template("users/members.html")


@blueprint.route("/checkout")
@login_required
def checkout():
    return render_template("users/checkout.html")


@blueprint.route("/checkout_excel/", methods=['GET', 'POST'])
@login_required
def checkout_excel():
    if request.method == 'POST' and 'spreadsheet' in request.files:
        filename = upload_sets.spreadsheets.save(request.files['spreadsheet'], folder=g.user.username)
        upload = Upload(filename=filename, user_id=g.user.id)
        upload.save()
        flash("Spreadsheet saved. You should receive a confirmation email soon.  If not, click the 'Contact' link at "
              "the bottom of this page and email the administrator.", 'success')
        return render_template('users/checkout.html')
    else:
        pass

    return render_template('users/checkout_excel.html')



# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST' and 'photo' in request.files:
#         filename = photos.save(request.files['photo'])
#         rec = Photo(filename=filename, user=g.user.id)
#         rec.store()
#         flash("Photo saved.")
#         return redirect(url_for('show', id=rec.id))
#     return render_template('upload.html')
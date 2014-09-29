# -*- coding: utf-8 -*-
from flask import g
from flask import (Blueprint, request, render_template, flash, url_for, redirect, session, abort)
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from TsetseCheckout import upload_sets
from TsetseCheckout.user.models import Upload
from TsetseCheckout.processing.checkouts.spreadsheets import process_requests
from TsetseCheckout import email

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
        upload = Upload(filename=filename, user=g.user)
        results, passed = process_requests(upload)
        if passed:
            upload.save()
            flash("Your requests have been logged. You should receive a confirmation email soon.  If not, click the "
                  "'Contact' link at the bottom of this page and email the administrator.", 'success')
        else:
            flash("There were errors in your submission and it can not be processed.  Please edit your file and try "
                  "again. You should receive a confirmation email detailing the errors soon.  If not, click the "
                  "'Contact' link at the bottom of this page and email the administrator.", 'danger')

        email.notify_spreadsheet_req_confirm(g.user, results, passed)
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
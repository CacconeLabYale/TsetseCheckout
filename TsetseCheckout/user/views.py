# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, abort
from flask.ext.login import login_required
from jinja2 import TemplateNotFound

blueprint = Blueprint("user", __name__, url_prefix='/users', static_folder="../static")


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
    return render_template_or_404("users/members.html")


@blueprint.route("/checkout")
@login_required
def checkout():
    return render_template_or_404("users/checkout.html")
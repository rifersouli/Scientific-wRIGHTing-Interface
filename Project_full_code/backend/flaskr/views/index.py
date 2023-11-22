import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def index():
    resumos = Resumo.query.all()
    return render_template('index.html', resumos=resumos)
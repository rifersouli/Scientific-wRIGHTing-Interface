import functools

from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def index():
    try:
        resumos = Resumo.query.all()
        return render_template('index.html', resumos=resumos)
    except OperationalError:
        # Database not available, return empty list
        return render_template('index.html', resumos=[])

@bp.route('/api/Resumos')
def get_abstracts():
    try:
        resumos = Resumo.query.all()
        dados_resumos = [{'id': resumo.id, 'titulo': resumo.titulo, 'resumo': resumo.resumo} for resumo in resumos]
        response = jsonify({'resumos': dados_resumos})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
    except OperationalError:
        # Database not available, return empty list
        response = jsonify({'resumos': []})
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        return response
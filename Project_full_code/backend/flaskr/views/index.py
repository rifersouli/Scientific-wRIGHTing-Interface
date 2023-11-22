import functools

from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('index', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def index():
    resumos = Resumo.query.all()
    return render_template('index.html', resumos=resumos)

@bp.route('/api/Resumos')
def get_abstracts():
    resumos = Resumo.query.all()
    dados_resumos = [{'id': Resumo.id, 'titulo': Resumo.titulo} for Resumo in resumos]
    return jsonify({'resumos': dados_resumos})
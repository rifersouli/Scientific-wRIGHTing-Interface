import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('resumo', __name__, url_prefix='/resumo')

@bp.route('/resumos/<int:resumo_id>', methods=['GET', 'POST'])
def resumo(resumo_id):
    try:
        # Try to get the resumo from database
        resumo = Resumo.query.get_or_404(resumo_id)
        return render_template('modal.html', resumo=resumo)
    except OperationalError:
        # Database not available, return template without data
        return render_template('modal.html', resumo=None)
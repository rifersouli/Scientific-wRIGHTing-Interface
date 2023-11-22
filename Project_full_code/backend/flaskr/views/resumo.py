import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('resumo', __name__, url_prefix='/resumo')

@bp.route('/resumos/<int:resumo_id>', methods=['GET', 'POST'])
def resumo(Resumo_id):

    return render_template('modal.html')
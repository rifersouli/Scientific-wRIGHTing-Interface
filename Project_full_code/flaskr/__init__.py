import os

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from . models import db, Resumo, Objetivo, Conclusao
from . views import index, resumo

def create_app(test_config=None):
    # cria e confirgura o app
    basedir = os.path.abspath(os.path.dirname(__file__))

    app_site = Flask(__name__, instance_relative_config=True)
    app_site.config.from_mapping(
        SECRET_KEY='dev',
    )
    app_site.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://root:123@localhost:3306/tcc_zilli'
    app_site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app_site)

    if test_config is None:
        # carrega a instância config, se ela existe, quando não se está testando
        app_site.config.from_pyfile('config.py', silent=True)
    else:
        # carrega a config de teste se ela foi passada
        app_site.config.from_mapping(test_config)

    # se assegura de que a pasta de instâncias existe
    try:
        os.makedirs(app_site.instance_path)
    except OSError:
        pass

    # uma página para testar a aplicação
    @app_site.route('/teste')
    def teste():
        return '<h1>Se você está lendo isso, está funcionando.</h1>' 
    
    app_site.register_blueprint(index.bp)
    app_site.register_blueprint(resumo.bp)

    return app_site
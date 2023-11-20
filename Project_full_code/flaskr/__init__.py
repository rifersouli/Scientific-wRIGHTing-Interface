import os

from flask import Flask

def create_app(test_config=None):
    # cria e confirgura o app
    basedir = os.path.abspath(os.path.dirname(__file__))

    app_site = Flask(__name__, instance_relative_config=True)
    app_site.config.from_mapping(
        SECRET_KEY='dev',
    )
    app_site.config()
    app_site.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:123@localhost:3306/tcc_zilli'
    app_site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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
        return 'Se você está lendo isso, está funcionando.'

    from . import db
    db.init_app(app_site)    

    return app_site
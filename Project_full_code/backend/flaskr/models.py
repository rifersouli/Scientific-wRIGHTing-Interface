from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resumo(db.Model):
    __tablename__ = 'RESUMOS'
    id = db.Column('RES_ID', db.Integer, primary_key=True)
    titulo = db.Column('RES_TITULO' ,db.String(100), nullable=False)
    resumo = db.Column('RES_RESUMO', db.Text, nullable=False)

class Objetivo(db.Model):
    __tablename__ = 'OBJETIVO'
    id = db.Column('OBJ_ID', db.Integer, primary_key=True)
    construcoes_linguisticas = db.Column('OBJ_CONSTRUCOES_LINGUISTICAS', db.String(500), nullable=False)
    categoria = db.Column('OBJ_CATEGORIA', db.String(3), nullable=False)
    justificativa = db.Column('OBJ_JUSTIFICATIVA', db.String(100), nullable=False)
    fk_resumo_id = db.Column('FK_RESUMOS_RES_ID', db.Integer, db.ForeignKey('RESUMOS.RES_ID', ondelete='CASCADE'), nullable=False)

class Conclusao(db.Model):
    __tablename__ = 'CONCLUSAO'
    id = db.Column('CON_ID', db.Integer, primary_key=True)
    construcoes_linguisticas = db.Column('CON_CONSTRUCOES_LINGUISTICAS', db.String(500), nullable=False)
    categoria = db.Column('CON_CATEGORIA', db.String(7), nullable=False)
    justificativa = db.Column('CON_JUSTIFICATIVA', db.String(100), nullable=False)
    fk_resumo_id = db.Column('FK_RESUMOS_RES_ID', db.Integer, db.ForeignKey('RESUMOS.RES_ID', ondelete='CASCADE'), nullable=False)
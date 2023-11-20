from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    resumo = db.Column(db.Text, unique=True, nullable=False)

class Objetivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    construcoes_linguisticas = db.Column(db.String(500), nullable=False)
    categoria = db.Column(db.String(3), nullable=False)
    justificativa = db.Column(db.String(100), nullable=False)
    fk_resumo_id = db.Column(db.Integer, db.ForeignKey('Resumo.id', ondelete='SET NULL'), nullable=False)

class Conclusao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    construcoes_linguisticas = db.Column(db.String(500), nullable=False)
    categoria = db.Column(db.String(7), nullable=False)
    justificativa = db.Column(db.String(100), nullable=False)
    fk_resumo_id = db.Column(db.Integer, db.ForeignKey('Resumo.id', ondelete='SET NULL'), nullable=False)
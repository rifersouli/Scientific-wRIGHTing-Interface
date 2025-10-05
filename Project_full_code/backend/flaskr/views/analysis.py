import functools
from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from .. models import db, Resumo, Objetivo, Conclusao

bp = Blueprint('analysis', __name__, url_prefix='/api')

def get_adjacency_matrix_position(resumo_id):
    """
    Calculate the position in the adjacency matrix based on the resumo ID.
    Following the logic from the original system:
    - Resumo 1 → position [0][1]
    - Resumo 2 → position [3][2] 
    - Resumo 3 → position [2][3]
    - Resumo 4 → position [5][4]
    - Resumo 5 → position [4][5]
    - Resumo 100 → position [99][99]
    """
    if resumo_id == 100:
        return (99, 99)
    elif resumo_id % 2 != 0:  # Odd numbers
        return (resumo_id - 1, resumo_id)
    else:  # Even numbers
        return (resumo_id + 1, resumo_id)

def get_annotated_phrase(resumo_id, phrase_type):
    """
    Get the annotated phrase (objective or conclusion) for a given resumo ID.
    Uses the adjacency matrix positioning logic.
    """
    try:
        if phrase_type == 'objetivo':
            obj = Objetivo.query.filter_by(id=resumo_id).first()
            return obj.construcoes_linguisticas if obj else ""
        elif phrase_type == 'conclusao':
            con = Conclusao.query.filter_by(id=resumo_id).first()
            return con.construcoes_linguisticas if con else ""
        return ""
    except OperationalError:
        return ""

def parse_sentences(text):
    """
    Parse text into sentences, removing annotation markers.
    """
    # Remove annotation markers
    clean_text = text.replace("--{", "").replace("}--", "").replace("--[", "").replace("]--", "")
    
    # Split by periods and clean up
    sentences = [s.strip() + "." for s in clean_text.split(".") if s.strip()]
    
    # Remove empty sentences
    sentences = [s for s in sentences if s.strip() and s != "."]
    
    return sentences

@bp.route('/analysis/objetivo/<int:resumo_id>')
def get_objetivo_analysis(resumo_id):
    """
    Get objective analysis data for a specific resumo.
    """
    try:
        # Get resumo data
        resumo = Resumo.query.get_or_404(resumo_id)
        
        # Get objective data
        objetivo = Objetivo.query.filter_by(id=resumo_id).first()
        
        if not objetivo:
            return jsonify({
                'error': 'No objective data found for this resumo',
                'resumo_id': resumo_id
            }), 404
        
        # Parse sentences from resumo
        sentences = parse_sentences(resumo.resumo)
        
        # Get annotated phrase
        annotated_phrase = objetivo.construcoes_linguisticas
        
        return jsonify({
            'resumo_id': resumo_id,
            'titulo': resumo.titulo,
            'sentences': sentences,
            'annotated_phrase': annotated_phrase,
            'categoria': objetivo.categoria,
            'justificativa': objetivo.justificativa
        })
        
    except OperationalError:
        return jsonify({'error': 'Database not available'}), 500

@bp.route('/analysis/conclusao/<int:resumo_id>')
def get_conclusao_analysis(resumo_id):
    """
    Get conclusion analysis data for a specific resumo.
    """
    try:
        # Get resumo data
        resumo = Resumo.query.get_or_404(resumo_id)
        
        # Get conclusion data
        conclusao = Conclusao.query.filter_by(id=resumo_id).first()
        
        if not conclusao:
            return jsonify({
                'error': 'No conclusion data found for this resumo',
                'resumo_id': resumo_id
            }), 404
        
        # Parse sentences from resumo
        sentences = parse_sentences(resumo.resumo)
        
        # Get annotated phrase
        annotated_phrase = conclusao.construcoes_linguisticas
        
        return jsonify({
            'resumo_id': resumo_id,
            'titulo': resumo.titulo,
            'sentences': sentences,
            'annotated_phrase': annotated_phrase,
            'categoria': conclusao.categoria,
            'justificativa': conclusao.justificativa
        })
        
    except OperationalError:
        return jsonify({'error': 'Database not available'}), 500

@bp.route('/analysis/match', methods=['POST'])
def check_match():
    """
    Check if user's selected phrase matches the annotated phrase.
    """
    try:
        data = request.get_json()
        user_phrase = data.get('user_phrase', '').strip()
        annotated_phrase = data.get('annotated_phrase', '').strip()
        phrase_type = data.get('phrase_type', 'objetivo')
        
        if not user_phrase or not annotated_phrase:
            return jsonify({
                'match': False,
                'message': 'Missing user phrase or annotated phrase'
            })
        
        # Perform matching logic similar to original system
        # Check if annotated phrase is contained in user phrase
        # Also check if user phrase is contained in annotated phrase for better matching
        match = (annotated_phrase in user_phrase) or (user_phrase in annotated_phrase)
        
        return jsonify({
            'match': match,
            'user_phrase': user_phrase,
            'annotated_phrase': annotated_phrase,
            'phrase_type': phrase_type
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'match': False
        }), 500

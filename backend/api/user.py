from flask import Blueprint, jsonify, request, get_flashed_messages
from flask_jwt_extended import jwt_required, get_jwt_identity
from tasks.export_tasks import generate_user_attempts_csv
from extensions import cache
from models.attempt import Attempt
import os

user_bp = Blueprint('user', __name__)

# existing list_attempts & export_attempts_csv & get_export_attempt

@user_bp.route('/<int:user_id>/attempts', methods=['GET'])
@jwt_required()
def list_attempts(user_id):
    if int(get_jwt_identity()) != int(user_id):
        return jsonify(msg='Forbidden'), 403
    attempts = Attempt.query.filter_by(user_id=user_id).all()
    return jsonify([
        {'id': a.id, 'quiz_id': a.quiz_id, 'score': a.score, 'submitted_at': a.submitted_at}
        for a in attempts
    ]), 200

@user_bp.route('/<int:user_id>/exports/attempts', methods=['POST'])
@jwt_required()
def export_attempts_csv(user_id):
    if int(get_jwt_identity()) != int(user_id):
        return jsonify(msg='Forbidden'), 403
    job = generate_user_attempts_csv.delay(user_id)
    return jsonify(job_id=job.id), 202


@user_bp.route('/<int:user_id>/reports', methods=['GET'])
@jwt_required()
def list_reports(user_id):
    if int(get_jwt_identity())!=int(user_id): return jsonify(msg='Forbidden'),403
    # list CSVs and HTML reports for this user
    exports = [f for f in os.listdir('exports') if f.startswith(f'attempts_{user_id}_')]
    reports = [f for f in os.listdir('reports') if f.startswith(f'report_{user_id}_')]
    return jsonify({
        'exports': exports,
        'reports': reports
    }),200
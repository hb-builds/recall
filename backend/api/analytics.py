from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func, desc
from extensions import db, timestamp_limiter
from models.attempt import Attempt
from models.user import User
from models.question import Question
from models.answer import Answer
from models.subject import Subject
from models.quiz import Quiz
from flask_jwt_extended import get_jwt_identity

analytics_bp = Blueprint('analytics', __name__)


# Leaderboard: top N users for a quiz
def limit_decorator(limit):
    return timestamp_limiter.limit(limit)


@analytics_bp.route('/leaderboard/quiz/<int:quiz_id>', methods=['GET'])
@jwt_required()
@timestamp_limiter.limit('10000 per minute')
def quiz_leaderboard(quiz_id):
    n = int(request.args.get('limit', 10))
    results = (db.session.query(
        Attempt.user_id, User.full_name,
        Attempt.score).join(User, User.id == Attempt.user_id).filter(
            Attempt.quiz_id == quiz_id).order_by(
                Attempt.score.desc(), Attempt.submitted_at).limit(n).all())
    data = [{
        'user_id': uid,
        'full_name': name,
        'score': score
    } for uid, name, score in results]
    return jsonify(data), 200


@analytics_bp.route('/leaderboard/user/<int:user_id>', methods=['GET'])
@jwt_required()
@timestamp_limiter.limit('10000 per minute')
def user_leaderboard(user_id):
    # Average score ranking across all users
    scores = (db.session.query(
        Attempt.user_id,
        func.avg(Attempt.score).label('avg_score')).group_by(
            Attempt.user_id).order_by(desc('avg_score')).all())
    ranking = next(
        (i + 1 for i, (uid, _) in enumerate(scores) if uid == user_id), None)
    return jsonify({
        'user_id': user_id,
        'ranking': ranking,
        'total_users': len(scores)
    }), 200


@analytics_bp.route('/analytics/user/<int:user_id>/monthly', methods=['GET'])
@jwt_required()
@timestamp_limiter.limit('10000 per minute')
def analytics_user_monthly(user_id):
    data = (db.session.query(
        func.strftime('%Y-%m', Attempt.submitted_at).label('period'),
        func.avg(Attempt.score).label('avg_score')).filter(
            Attempt.user_id == user_id).group_by('period').order_by(
                'period').all())
    return jsonify([{'period': p, 'avg_score': a} for p, a in data]), 200


@analytics_bp.route('/analytics/quiz/<int:quiz_id>/difficulty',
                    methods=['GET'])
@jwt_required()
@timestamp_limiter.limit('10000 per minute')
def analytics_quiz_difficulty(quiz_id):
    # For each question, compute total attempts and correct count
    subq = (db.session.query(
        Answer.question_id,
        func.count(Answer.id).label('total'),
        func.sum(
            func.case([(Answer.selected_option == Question.correct_option, 1)],
                      else_=0)).label('correct')).join(
                          Question, Answer.question_id == Question.id).filter(
                              Question.quiz_id == quiz_id).group_by(
                                  Answer.question_id).subquery())
    results = db.session.query(subq.c.question_id, subq.c.total,
                               subq.c.correct).all()
    data = []
    for qid, total, correct in results:
        percent = (correct / total * 100) if total else 0
        data.append({
            'question_id': qid,
            'total': total,
            'correct': correct,
            'percent_correct': percent
        })
    return jsonify(data), 200

@analytics_bp.route('/summary/admin', methods=['GET'])
@jwt_required()
def admin_summary():
    if get_jwt().get('role') != 'admin':
        return jsonify(msg='Admins only'), 403
    
    num_users = User.query.count()
    num_subjects = Subject.query.count()
    num_quizzes = Quiz.query.count()
    num_attempts = Attempt.query.count()

    return jsonify({
        'users': num_users,
        'subjects': num_subjects,
        'quizzes': num_quizzes,
        'attempts': num_attempts
    }), 200

@analytics_bp.route('/summary/user', methods=['GET'])
@jwt_required()
def user_summary():
    user_id = get_jwt_identity()
    
    total_attempts = Attempt.query.filter_by(user_id=user_id).count()
    
    avg_score_result = db.session.query(func.avg(Attempt.score)).filter_by(user_id=user_id).scalar()
    avg_score = float(avg_score_result) if avg_score_result else 0

    scores = (db.session.query(
        Attempt.user_id,
        func.avg(Attempt.score).label('avg_score')).group_by(
            Attempt.user_id).order_by(desc('avg_score')).all())
    ranking = next(
        (i + 1 for i, (uid, _) in enumerate(scores) if uid == user_id), None)

    return jsonify({
        'total_attempts': total_attempts,
        'average_score': avg_score,
        'ranking': ranking
    }), 200

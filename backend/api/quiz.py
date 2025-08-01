from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db, cache
from models.quiz import Quiz
from models.attempt import Attempt
from models.answer import Answer
from models.question import Question
import datetime
from sqlalchemy import func

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/subjects', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_subjects_public():
    from models.subject import Subject
    subjects = Subject.query.filter_by(deleted_at=None).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in subjects]), 200

@quiz_bp.route('/subjects/<int:subject_id>/chapters', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_chapters_public(subject_id):
    from models.chapter import Chapter
    chapters = Chapter.query.filter_by(subject_id=subject_id, deleted_at=None).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in chapters]), 200

@quiz_bp.route('/chapters/<int:chapter_id>/quizzes', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_quizzes_public(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id, deleted_at=None).all()
    return jsonify([
        {'id': q.id, 'title': q.title, 'duration_min': q.duration_min, 'scheduled_at': q.scheduled_at}
        for q in quizzes
    ]), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/full', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_full_quiz(quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, deleted_at=None).first_or_404()
    questions = quiz.questions
    payload = {
        'quiz_id': quiz.id,
        'title': quiz.title,
        'duration_min': quiz.duration_min,
        'questions': [
            {
                'question_id': q.id,
                'statement': q.statement,
                'options': [q.option1, q.option2, q.option3, q.option4]
            } for q in questions
        ]
    }
    return jsonify(payload), 200

@quiz_bp.route('/quizzes/<int:quiz_id>/start', methods=['POST'])
@jwt_required()
def start_attempt(quiz_id):
    user_id = get_jwt_identity()
    quiz = Quiz.query.filter_by(id=quiz_id, deleted_at=None).first_or_404()
    
    # Check for existing, unsubmitted attempts
    existing_attempt = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id, submitted_at=None).first()
    if existing_attempt:
        return jsonify(attempt_id=existing_attempt.id, started_at=existing_attempt.started_at.isoformat()), 200

    attempt = Attempt(
        quiz_id=quiz_id,
        user_id=user_id,
        started_at=datetime.datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()
    return jsonify(attempt_id=attempt.id, started_at=attempt.started_at.isoformat()), 201

@quiz_bp.route('/attempts/<int:attempt_id>/submit', methods=['POST'])
@jwt_required()
def submit_attempt(attempt_id):
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    answers = data.get('answers', [])

    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id).first_or_404()
    if attempt.submitted_at:
        return jsonify(msg='Attempt already submitted'), 400

    quiz = attempt.quiz
    time_limit = datetime.timedelta(minutes=quiz.duration_min)
    if datetime.datetime.utcnow() > attempt.started_at + time_limit:
        return jsonify(msg='Time limit exceeded'), 400

    attempt.submitted_at = datetime.datetime.utcnow()
    
    score = 0
    for ans in answers:
        q = Answer(
            attempt_id=attempt.id,
            question_id=ans['question_id'],
            selected_option=ans['selected_option']
        )
        db.session.add(q)
        # grading logic: compare with correct_option
        correct = next((x for x in attempt.quiz.questions if x.id==ans['question_id']), None)
        if correct and correct.correct_option == ans['selected_option']:
            score += 1
    attempt.score = score
    db.session.commit()
    return jsonify(attempt_id=attempt.id, score=score), 200

@quiz_bp.route('/attempts/<int:attempt_id>', methods=['GET'])
@jwt_required()
def get_attempt_detail(attempt_id):
    attempt = Attempt.query.filter_by(id=attempt_id).first_or_404()
    if attempt.user_id != int(get_jwt_identity()):
        return jsonify(msg='Forbidden'),403
    details = [
        {
            'question_id': a.question_id,
            'selected': a.selected_option,
            'correct': a.question.correct_option
        } for a in attempt.answers
    ]
    return jsonify({
        'attempt_id': attempt.id,
        'quiz_id': attempt.quiz_id,
        'score': attempt.score,
        'submitted_at': attempt.submitted_at,
        'details': details
    }), 200

@quiz_bp.route('/analytics/quizzes/hardest', methods=['GET'])
@jwt_required()
def get_hardest_quizzes():
    # Subquery to get the number of questions for each quiz.
    questions_count = db.session.query(
        Question.quiz_id,
        func.count(Question.id).label('num_questions')
    ).group_by(Question.quiz_id).subquery()
    
    quiz_avg_scores = db.session.query(
        Attempt.quiz_id,
        func.avg(Attempt.score / questions_count.c.num_questions).label('avg_score')
    ).join(questions_count, Attempt.quiz_id == questions_count.c.quiz_id) \
     .group_by(Attempt.quiz_id) \
     .subquery()
    
    hardest_quizzes_query = db.session.query(
        Quiz.id,
        Quiz.title,
        quiz_avg_scores.c.avg_score
    ).join(quiz_avg_scores, Quiz.id == quiz_avg_scores.c.quiz_id) \
     .order_by(quiz_avg_scores.c.avg_score.asc()) \
     .limit(5)

    results = hardest_quizzes_query.all()

    # Formating the final payload.
    payload = [{
        'quiz_id': q.id,
        'title': q.title,
        'average_score': q.avg_score * 100 if q.avg_score is not None else 0
    } for q in results]
    
    return jsonify(payload), 200

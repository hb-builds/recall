from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from extensions import db
from models.subject import Subject
from models.user import User
from models.quiz import Quiz
from models.question import Question
from sqlalchemy import or_
import datetime
from tasks.export_tasks import generate_admin_quizzes_csv
from schemas.admin import SubjectSchema, ChapterSchema, QuizSchema, QuestionSchema
from marshmallow import ValidationError

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        if get_jwt().get('role') != 'admin':
            return jsonify(msg='Admins only'), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

# --- Subjects CRUD ---
@admin_bp.route('/subjects', methods=['GET'])
@admin_required
def get_subjects():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    search = request.args.get('search', '')
    query = Subject.query.filter(Subject.deleted_at==None)
    if search:
        query = query.filter(Subject.name.ilike(f"%{search}%"))
    total = query.count()
    subjects = query.offset((page-1)*limit).limit(limit).all()
    return jsonify({
        'items': [{'id': s.id,'name': s.name,'description': s.description} for s in subjects],
        'page': page, 'limit': limit, 'total': total
    }),200
# apply similar pagination & search to chapters and quizzes endpoints

@admin_bp.route('/subjects', methods=['POST'])
@admin_required
def create_subject():
    try:
        data = SubjectSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    subject = Subject(name=data['name'], description=data.get('description'))
    db.session.add(subject)
    db.session.commit()
    return jsonify(id=subject.id), 201

@admin_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    data = request.get_json() or {}
    subject.name = data.get('name', subject.name)
    subject.description = data.get('description', subject.description)
    db.session.commit()
    return jsonify(msg='Updated'), 200

@admin_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    subject.deleted_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(msg='Deleted'), 200

# --- Chapters CRUD ---
@admin_bp.route('/chapters', methods=['POST'])
@admin_required
def create_chapter():
    try:
        data = ChapterSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    chapter = Chapter(
        subject_id=data['subject_id'],
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(chapter)
    db.session.commit()
    return jsonify(id=chapter.id), 201

@admin_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
@admin_required
def update_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    data = request.get_json() or {}
    chapter.name = data.get('name', chapter.name)
    chapter.description = data.get('description', chapter.description)
    db.session.commit()
    return jsonify(msg='Updated'), 200

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    chapter.deleted_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(msg='Deleted'), 200

# --- Quizzes CRUD ---
@admin_bp.route('/quizzes', methods=['POST'])
@admin_required
def create_quiz():
    try:
        data = QuizSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    quiz = Quiz(
        chapter_id=data['chapter_id'],
        title=data['title'],
        scheduled_at=data.get('scheduled_at'),
        duration_min=data['duration_min']
    )
    db.session.add(quiz)
    db.session.commit()
    return jsonify(id=quiz.id), 201

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    data = request.get_json() or {}
    quiz.title = data.get('title', quiz.title)
    quiz.scheduled_at = data.get('scheduled_at', quiz.scheduled_at)
    quiz.duration_min = data.get('duration_min', quiz.duration_min)
    db.session.commit()
    return jsonify(msg='Updated'), 200

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.deleted_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(msg='Deleted'), 200

# --- Questions CRUD ---
@admin_bp.route('/questions', methods=['POST'])
@admin_required
def create_question():
    try:
        data = QuestionSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    question = Question(
        quiz_id=data['quiz_id'],
        statement=data['statement'],
        option1=data['option1'],
        option2=data['option2'],
        option3=data['option3'],
        option4=data['option4'],
        correct_option=data['correct_option']
    )
    db.session.add(question)
    db.session.commit()
    return jsonify(id=question.id), 201

@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    data = request.get_json() or {}
    for field in ('statement','option1','option2','option3','option4','correct_option'):
        if data.get(field) is not None:
            setattr(question, field, data[field])
    db.session.commit()
    return jsonify(msg='Updated'), 200

@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    question.deleted_at = datetime.datetime.utcnow()
    db.session.commit()
    return jsonify(msg='Deleted'), 200

# --- Search ---

@admin_bp.route('/search', methods=['GET'])
@admin_required
def search_admin():
    entity = request.args.get('entity')  # users, subjects, quizzes, questions
    q = request.args.get('q', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    model_map = {
        'subjects': (Subject, ['name', 'description']),
        'users': (User, ['full_name', 'email']),
        'quizzes': (Quiz, ['title']),
        'questions': (Question, ['statement']),
    }
    if entity not in model_map:
        return jsonify(msg='Invalid entity'), 400

    Model, search_fields = model_map[entity]
    
    query = Model.query
    if hasattr(Model, 'deleted_at'):
        query = query.filter(Model.deleted_at == None)

    if q:
        search_filters = [getattr(Model, field).ilike(f"%{q}%") for field in search_fields]
        query = query.filter(or_(*search_filters))

    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    def serialize(item):
        if isinstance(item, User):
            return {'id': item.id, 'full_name': item.full_name, 'email': item.email, 'role': item.role}
        elif isinstance(item, Subject):
            return {'id': item.id, 'name': item.name, 'description': item.description}
        elif isinstance(item, Quiz):
            return {'id': item.id, 'title': item.title, 'duration_min': item.duration_min}
        elif isinstance(item, Question):
            return {'id': item.id, 'statement': item.statement}
        return {}

    data = [serialize(item) for item in items]
    return jsonify({'items': data, 'page': page, 'limit': limit, 'total': total}), 200

@admin_bp.route('/exports/quizzes', methods=['POST'])
@admin_required
def export_quizzes_csv():
    job = generate_admin_quizzes_csv.delay()
    return jsonify(job_id=job.id), 202
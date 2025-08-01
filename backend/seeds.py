import os
import json
import click
from extensions import db
from models.user import User
from models.subject import Subject
from models.chapter import Chapter
from models.quiz import Quiz
from models.question import Question
from models.attempt import Attempt
from models.answer import Answer
import random
import datetime

@click.command()
def seed():
    # 1) Admin account
    users_to_seed = [
        {'email': 'admin@iitm.ac.in', 'password': 'adminpassword', 'full_name': 'Quiz Master Admin', 'role': 'admin'},
        {'email': 'user1@iitm.ac.in', 'password': 'password', 'full_name': 'Test User 1', 'role': 'user'},
        {'email': 'user2@iitm.ac.in', 'password': 'password', 'full_name': 'Test User 2', 'role': 'user'},
    ]
    
    users = {}
    for user_data in users_to_seed:
        user = User.query.filter_by(email=user_data['email']).first()
        if not user:
            user = User(email=user_data['email'], full_name=user_data['full_name'], role=user_data['role'])
            user.set_password(user_data['password'])
            db.session.add(user)
        users[user_data['email']] = user
    db.session.flush()

    # 3) Load seed data from JSON
    data_path = os.path.join(os.path.dirname(__file__), 'seed_data.json')
    with open(data_path, 'r') as f:
        subjects = json.load(f)

    # 4) Loop to insert all data
    all_quizzes = []
    for subj in subjects:
        subject = Subject(name=subj['name'], description=subj.get('description'))
        db.session.add(subject)
        db.session.flush()
        for chap in subj.get('chapters', []):
            chapter = Chapter(
                subject_id=subject.id,
                name=chap.get('name'),
                description=chap.get('description')
            )
            db.session.add(chapter)
            db.session.flush()
            for quiz_data in chap.get('quizzes', []):
                quiz = Quiz(
                    chapter_id=chapter.id,
                    title=quiz_data.get('title'),
                    scheduled_at=quiz_data.get('scheduled_at'),
                    duration_min=quiz_data.get('duration_min')
                )
                db.session.add(quiz)
                db.session.flush()
                all_quizzes.append(quiz)
                for q in quiz_data.get('questions', []):
                    question = Question(
                        quiz_id=quiz.id,
                        statement=q.get('statement'),
                        option1=q['options'][0],
                        option2=q['options'][1],
                        option3=q['options'][2],
                        option4=q['options'][3],
                        correct_option=q.get('correct_option')
                    )
                    db.session.add(question)
    
    # 5) Create attempts for users
    for i, quiz in enumerate(all_quizzes):
        if i % 2 == 0: # user1 attempts even numbered quizzes
            user = users['user1@iitm.ac.in']
        else: # user2 attempts odd numbered quizzes
            user = users['user2@iitm.ac.in']
        
        attempt = Attempt(
            quiz_id=quiz.id,
            user_id=user.id,
            started_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(10, 30)),
            submitted_at=datetime.datetime.utcnow() - datetime.timedelta(minutes=random.randint(1, 9))
        )
        db.session.add(attempt)
        db.session.flush()

        score = 0
        for question in quiz.questions:
            selected_option = random.randint(1, 4)
            if selected_option == question.correct_option:
                score += 1
            answer = Answer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_option=selected_option
            )
            db.session.add(answer)
        attempt.score = score

    db.session.commit()
    click.echo("Seed data created")
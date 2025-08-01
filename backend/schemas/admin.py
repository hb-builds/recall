from marshmallow import Schema, fields, validate

class SubjectSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()

class ChapterSchema(Schema):
    subject_id = fields.Int(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    description = fields.Str()

class QuizSchema(Schema):
    chapter_id = fields.Int(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    duration_min = fields.Int(required=True, validate=validate.Range(min=1))
    scheduled_at = fields.DateTime()

class QuestionSchema(Schema):
    quiz_id = fields.Int(required=True)
    statement = fields.Str(required=True, validate=validate.Length(min=1))
    option1 = fields.Str(required=True)
    option2 = fields.Str(required=True)
    option3 = fields.Str(required=True)
    option4 = fields.Str(required=True)
    correct_option = fields.Int(required=True, validate=validate.Range(min=1, max=4))

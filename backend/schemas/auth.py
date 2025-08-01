from marshmallow import Schema, fields, validate

class RegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    full_name = fields.Str(required=True, validate=validate.Length(min=1))
    qualification = fields.Str()
    dob = fields.Date()

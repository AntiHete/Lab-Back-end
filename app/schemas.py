from marshmallow import Schema, fields, validate

# Schema for user details
class UserSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the user")
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=50),
        description="Username (3-50 characters)"
    )
    password = fields.Str(
        required=True, 
        load_only=True, 
        validate=validate.Length(min=8),
        description="Password (minimum 8 characters)"
    )

# Schema for categories
class CategorySchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the category")
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        description="Name of the category (1-100 characters)"
    )

# Schema for expense records
class RecordSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the record")
    user_id = fields.Int(required=True, description="ID of the user who created the record")
    category_id = fields.Int(required=True, description="ID of the expense category")
    money_spent = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Amount of money spent (must be non-negative)"
    )

# Schema for user accounts
class AccountSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the account")
    user_id = fields.Int(required=True, description="ID of the user associated with the account")
    balance = fields.Float(
        default=0.0,
        validate=validate.Range(min=0),
        description="Account balance (must be non-negative)"
    )

# Schema for funds transfer
class FundsSchema(Schema):
    user_id = fields.Int(required=True, description="ID of the user making the transaction")
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Amount of funds to add or withdraw (must be non-negative)"
    )

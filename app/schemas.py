from marshmallow import Schema, fields, validate

# Schema for user transactions
class TransactionSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the transaction")
    account_id = fields.Int(required=True, description="Associated account ID")
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Transaction amount (must be non-negative)"
    )
    timestamp = fields.DateTime(dump_only=True, description="Transaction timestamp")

# Schema for user accounts
class AccountSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the account")
    user_id = fields.Int(required=True, description="ID of the user associated with the account")
    balance = fields.Float(
        default=0.0,
        validate=validate.Range(min=0),
        description="Account balance (must be non-negative)"
    )

# Schema for user details
class UserSchema(Schema):
    id = fields.Int(dump_only=True, description="Unique identifier for the user")
    username = fields.Str(
        required=True,
        validate=validate.Length(min=3, max=50),
        description="Username (3-50 characters)"
    )
    email = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        description="Valid email address"
    )
    password = fields.Str(
        required=True,
        load_only=True,
        validate=validate.Length(min=8),
        description="Password (minimum 8 characters)"
    )

# Schema for transferring funds
class FundsTransferSchema(Schema):
    source_account_id = fields.Int(required=True, description="Source account ID")
    target_account_id = fields.Int(required=True, description="Target account ID")
    amount = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        description="Amount to transfer (must be non-negative)"
    )

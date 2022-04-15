from cerberus import Validator


def config_is_valid(config):
    schema = {
        "email": {
            "type": "dict",
            "schema": {
                "email": {
                    "type": "string"
                },
                "password": {
                    "type": "string"
                },
                "receiver": {
                    "type": "string"
                }
            }
        },
        "twitter": {
            "type": "dict",
            "schema": {
                "api_key": {
                    "type": "string"
                },
                "api_key_secret": {
                    "type": "string"
                },
                "access_token": {
                    "type": "string"
                },
                "access_token_secret": {
                    "type": "string"
                },
                "followed_users": {
                    "type": "list"
                }
            }
        }
    }

    v = Validator(schema, require_all=True)
    if not v.validate(config):
        raise ValueError(v.errors)



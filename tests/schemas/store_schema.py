STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer",
        },
        "delivered": {
            "type": "integer",
        },
        "placed": {
            "type": "integer",
        }
    }
}

ORDER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "shipDate": {
            "type": "string"
        },
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered"]
        },
        "complete": {
            "type": "boolean"
        }
    },
    "required": ["id", "petId", "quantity"],
    "additionalProperties": False
}
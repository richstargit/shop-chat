def individual_data(todo) -> dict:
    return{
        "id": str(todo["_id"]),
        "title": todo["name"],
        "description": todo["description"],
        "complete": todo["complete"]
    }

def list_data(todos) -> list:
    return[individual_data(todo) for todo in todos]
def paginate_dynamodb_response(response: dict, model_class, limit: int) -> dict:
    """
    Converts DynamoDB scan/query response to paginated API response.
    Args:
        response: DynamoDB response dict
        model_class: Pydantic model class to parse items
        limit: page size
    Returns:
        dict with items, last_evaluated_key, and limit
    """
    items = [model_class(**item) for item in response['items']]
    return {
        "items": items,
        "last_evaluated_key": response['last_evaluated_key'],
        "limit": limit
    }
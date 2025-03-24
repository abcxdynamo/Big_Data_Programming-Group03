def to_dict_list(model_list):
    """
    Converts a list of SQLAlchemy model instances to a list of dictionaries.

    :param model_list: List of SQLAlchemy model instances.
    :return: List of dictionaries.
    """
    return [model.dict() for model in model_list]

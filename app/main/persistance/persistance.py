from app.main.config import db


def data_to_object(response, object_class):
    # convert to object
    return object_class(**vars(response))


def add_prefix_to_dict_keys(dictionary, prefix):
    return {prefix + "_" + key: value for key, value in dictionary.items()}
# -*- coding: utf-8 -*-
"""
Deserializer json to help for data migrations.
"""

import json


def load_json(file):
    """
    Load a json object from a file and return it.
    """
    data = open(file).read()
    matrix_data = json.loads(data)
    return matrix_data


def json_to_model(text, model_class):
    """
    Deserialize json string into model instances:
    - text: json source as a string
    - model_class: the model class
    Return: a model instance
    """
    fields = json.loads(text)
    return model_class.objects.create(**fields)

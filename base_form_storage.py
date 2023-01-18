import os
import pickle

import base_form

FILE_FORMAT = ".pickle"


def save_form(form: base_form, file: str):
    try:
        with open(file + FILE_FORMAT, "wb") as f:
            pickle.dump(form, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)


def load_form(file: str):
    try:
        with open(file + FILE_FORMAT, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


def list_forms(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if file.endswith(FILE_FORMAT):
            form = load_form(os.path.join(path, file))
            result.append(form)
    return result

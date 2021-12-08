# TODO jezeli jest MinID i MaxID, musi być placeholder w postaci str "<x>";
#  parameters muszą mieć osobne pozycje, więc trzeba będize każdy obiekt "zapisac do osobnej zmiennej"
#  aby później generować plik hpp dla każdego osobnego parametru z indywidualnym ID
import json
from jsonschema import validate  # , Draft7Validator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="input JSON filename with extension")
parser.add_argument("schema", type=str, help="input JSON filename with schema")
args = parser.parse_args()


def convert_json_to_python(file1, file2):
    # Convert json to python object.
    with open(file1) as to_check:
        _json = json.load(to_check)
    with open(file2) as to_schema:
        my_schema = json.load(to_schema)
    # Validate will raise exception if given json is not
    # what is described in schema.
    validate(instance=_json, schema=my_schema)
    return _json


class Checker:
    json_object = {}

    def __init__(self, json_file, jsonschema):
        Checker.json_object = convert_json_to_python(json_file, jsonschema)

    def check_placeholder(self, m_json):
        for i in range(len(m_json['Parameters'])):
            if 'ID' not in m_json['Parameters'][i]:
                if m_json['Parameters'][i]["Name"].endswith("<x>"):
                    print("correct")
                else:
                    print('not correct')

    def not_double_name(self, m_json):
        name_board = []
        name_parameters = []
        for i in range(len(m_json["Boards"])):
            name_board.append(m_json["Boards"][i]["Name"])
        for i in range(len(m_json["Parameters"])):
            name_parameters.append(m_json["Parameters"][i]["Name"])
        name_board.sort()
        name_parameters.sort()
        for i in range(len(name_board)):
            if i < len(name_board) - 1:
                if name_board[i] == name_board[i + 1]:
                    print("boards name error")
        for i in range(len(name_parameters)):
            if i < len(name_parameters) - 1:
                if name_parameters[i] == name_parameters[i + 1]:
                    print("parameters name error")

    # check weather MinID is smaller than MaxID
    def compare_min_and_max(self, first, last):
        if int(first, 16) >> int(last, 16):
            print("Wrong MinID and MaxID input")

    def compare_loop(self, my_json):
        for j in range(len(my_json)):
            if 'ID' not in my_json['Parameters'][j]:
                Checker.compare_min_and_max(self, my_json['Parameters'][j]['MinID'], my_json['Parameters'][j]["MaxID"])

    def run_checks(self, ob):
        Checker.check_placeholder(self, ob)
        Checker.not_double_name(self, ob)
        Checker.compare_loop(self, ob)


jsonf = Checker(args.json_file, args.schema)
jsonf.run_checks(jsonf.json_object)

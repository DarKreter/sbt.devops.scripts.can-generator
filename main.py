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


# check weather MinID is smaller than MaxID
def compare_min_and_max(mi, ma):
    if int(mi, 16) >> int(ma, 16):
        print("Wrong MinID and MaxID input")


for j in range(len(my_json)):
    if 'ID' not in my_json['Parameters'][j]:
        compare_min_and_max(my_json['Parameters'][j]['MinID'], my_json['Parameters'][j]["MaxID"])
# TODO jezeli jest MinID i MaxID, musi być placeholder w postaci str "<x>";
#  zapakować w klasę checker(json, json_schema) -> checker.runChecks()
#  parameters muszą mieć osobne pozycje, więc trzeba będize każdy obiekt "zapisac do osobnej zmiennej"
#  aby później generować plik hpp dla każdego osobnego parametru z indywidualnym ID


class Checker:
    def __init__(self):
        print("new object")

    def check_placeholder(self, m_json):
        for i in range(len(m_json)):
            if 'ID' not in m_json['Parameters'][i]:
                if "(<x>)$" in m_json['Parameters'][i]:
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

    def run_checks(self):
        # validate
        ob = convert_json_to_python(args.json_file, args.schema)
        Checker.check_placeholder(ob)
        Checker.not_double_name(ob)


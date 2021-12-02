import json
from jsonschema import validate  # , Draft7Validator
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="input JSON filename with extension")
parser.add_argument("schema", type=str, help="input JSON filename with schema")
args = parser.parse_args()

# Convert json to python object.
with open(args.json_file) as to_check:
    my_json = json.load(to_check)
with open(args.schema) as to_schema:
    my_schema = json.load(to_schema)
# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=my_schema)


def check_parameters():
    # PARAMETERS CHECKING
    # looking for name in Parameters
    for i in range(len(my_json['Parameters'])):
        print("Parameters_Name:", my_json['Parameters'][i]["Name"])
        print("Type:", my_json['Parameters'][i]["Type"])


# check weather MinID is smaller than MaxID
def compare_min_and_max(Min, Max):
    if int(Min, 16) >> int(Max, 16):
        print("Wrong MinID and MaxID input")


for j in range(len(my_json)):
    if 'ID' not in my_json['Parameters'][j]:
        compare_min_and_max(my_json['Parameters'][j]['MinID'], my_json['Parameters'][j]["MaxID"])


def not_double_name():
    name_board = []
    name_parameters = []
    for i in range(len(my_json["Boards"])):
        name_board.append(my_json["Boards"][i]["Name"])
    for i in range(len(my_json["Parameters"])):
        name_parameters.append(my_json["Parameters"][i]["Name"])
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


not_double_name()


# parameters muszą mieć osobne pozycje, więc trzeba będize każdy obiekt "zapisac do osobnej zmiennej"
# aby później generować plik hpp dla każdego osobnego parametru z indywidualnym ID


# TODO
# jezeli jest MinID i MaxID, musi być placeholder w postaci str "<x>"
# zapakować w klasę checker(json, json_schema) -> checker.runChecks()

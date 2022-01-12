# TODO  parameters muszą mieć osobne pozycje, więc trzeba będize każdy obiekt "zapisac do osobnej zmiennej"
#  aby później generować plik hpp dla każdego osobnego parametru z indywidualnym ID
import argparse
import jsonschema
import json  # , Draft7Validator
from checker_class import Checker
from headerGen import HGenerate

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="input JSON filename with extension")
parser.add_argument("schema", type=str, help="input JSON filename with schema")
parser.add_argument("header_name", type=str, help="input new file name")
args = parser.parse_args()

def convert_json_to_python(file1, file2):
    # Convert json to python object.
    with open(file1) as to_check:
        _json = json.load(to_check)
    with open(file2) as to_schema:
        my_schema = json.load(to_schema)
    # Validate will raise exception if given json is not
    # what is described in schema.
    return _json, my_schema


python_json, python_schema = convert_json_to_python(args.json_file, args.schema)
check = Checker(python_json, python_schema)
check.run_checks(check.json_object)
objects = []
genFile = HGenerate(args.header_name[0:args.header_name.index('.')])
genFile.write_to_file(args.header_name, python_json)

import argparse
import json
from checker_class import Checker
from SDK_gen import SDK_gen
from python_gen import python_gen
from visualiseGen import VGenerate

parser = argparse.ArgumentParser()
parser.add_argument("--json_file", type=str, help="input JSON filename with extension")
parser.add_argument("--dbc_file", type=str, help="input DBC filename with extension")
parser.add_argument("--schema", type=str, help="input JSON filename with schema")
parser.add_argument("--SDK_header", type=str, help="Input header file name for SBT-SDK", required=False)
parser.add_argument("--python_header", type=str, help="Input file name for header in python", required=False)
parser.add_argument("--visualisation_header", type=str, help="Input header file name for visualisation app", required=False)
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

check = Checker(python_json, python_schema, args.json_file)
if check.run_checks(check.json_object, args.dbc_file):
    if args.SDK_header is not None:
        genFile = SDK_gen(args.SDK_header)
        genFile.write_to_file(python_json)
    if args.python_header is not None:
        genFile = python_gen(args.python_header)
        genFile.write_to_file(python_json)
    # if args.visual_name is not None:
    #     visual = VGenerate(args.visual_name)
    #     visual.write_to_file(python_json)
    exit(0)
else:
    exit(1)

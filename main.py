import json
from jsonschema import validate, draft7_format_checker
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("json_file", type=str, help="input JSON filename with extention")
args = parser.parse_args()

canIDsSchema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "Boards": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ID": {"type": "string"},
          "Name": {"type": "string"}
        },
        "required": [
          "ID",
          "Name"
        ]
      }
    },
    "Parameters": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "ID": {"type": "string"},
          "Name": {"type": "string"},
          "MinID": {"type": "string"},
          "MaxID": {"type": "string"},
          "Type": dict(type="string", enum=[
              "uint32",
              "bool",
              "float"
          ])
        },
        "required": [
          "Name",
          "Type"
        ]
      }
    }
  },
  "required": [
    "Boards",
    "Parameters"
  ]
}


def isnumericbase(s, base):
    try:
        int(s, base)
        return True
    except ValueError:
        return False


def ishexadecimalstring(s):
    return isnumericbase(s, 16)


# Convert json to python object.
my_json = json.load(open(args.json_file))
# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=canIDsSchema)

# BOARDS CHECKING
# checking id_number type
for i in range(len(my_json['Boards'])):
    id_number = my_json['Boards'][i]['ID']
    if ishexadecimalstring(id_number):
        continue
        # print(id_number, "- is hexadecimal")
    else:
        print("error", my_json['Boards'][i]['ID'])
        # print(id_number, "- is not")


# checking name type in Boards
for i in range(len(my_json['Boards'])):
    name_n = my_json['Boards'][i]['Name']
    if isinstance(name_n, str):
        continue
        # print("Boards_Name:", my_json['Boards'][i]['Name'], "- is correct")
    else:
        print("error", my_json['Boards'][i]['Name'])
        # print("Boards_Name:", my_json['Boards'][i]['Name'], "- is not correct")


print("\n")


# PARAMETERS CHECKING
# looking for name in Parameters
for i in range(len(my_json['Parameters'])):
    print("Parameters_Name:", my_json['Parameters'][i]["Name"])
    # print("ID:", my_json['Parameters'][i]['ID'])
    # if na sprawdzenie czy min i max są
    # print("MinID:", my_json['Parameters'][i]['MinID'])
    # print("MaxID:", my_json['Parameters'][i]['MaxID'])
    print("Type:", my_json['Parameters'][i]["Type"])

validate(
    instance="2.3.5.6",
    schema={"format": "ipv4"},
    format_checker=draft7_format_checker,
)

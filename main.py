import json
from jsonschema import validate
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
          "ID": {
            "type": "string",
            "pattern": "^(0[xX])[A-Fa-f0-9]+$"
          },
          "Name": {
            "type": "string"
          }
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
          "ID": {
            "type": "string",
            "pattern": "^(0[xX])[A-Fa-f0-9]+$"
          },
          "Name": {
            "type": "string"
          },
          "Type": {
            "type": "string",
            "enum": [
              "uint32",
              "bool",
              "float"
            ]
          },
          "MinID": {
            "type": "string",
            "pattern": "^(0[xX])[A-Fa-f0-9]+$"
          },
          "MaxID": {
            "type": "string",
            "pattern": "^(0[xX])[A-Fa-f0-9]+$"
          }
        },
        "oneOf": [
          {
            "required": [
              "ID",
              "Name",
              "Type"
            ]
          },
          {
            "required": [
              "MinID",
              "MaxID",
              "Name",
              "Type"
            ]
          }
        ],
      }
    }
  },
  "required": [
    "Boards",
    "Parameters"
  ]
}


# Convert json to python object.
my_json = json.load(open(args.json_file))
# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=canIDsSchema)
# PARAMETERS CHECKING
# looking for name in Parameters
for i in range(len(my_json['Parameters'])):
    print("Parameters_Name:", my_json['Parameters'][i]["Name"])
    # if not print("ID:", my_json['Parameters'][i]['ID']):
    # if na sprawdzenie czy min i max są
    # print("MinID:", my_json['Parameters'][i]['MinID'])
    # print("MaxID:", my_json['Parameters'][i]['MaxID'])
    print("Type:", my_json['Parameters'][i]["Type"])

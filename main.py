import json
from jsonschema import validate

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
            "type": "string"
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
          "ID": {"type": "string"},
          "Name": {"type": "string"},
          "Type": dict(type="string", enum=[
              "uint32",
              "bool",
              "float"
          ]),
          "MinID": {
            "type": "string"
          },
          "MaxID": {
            "type": "string"
          }
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
my_json = json.load(open('canIDs.json', ))
# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=canIDsSchema)

# BOARDS CHECKING
# checking id_number type
for i in range(len(my_json['Boards'])):
    id_number = my_json['Boards'][i]['ID']
    if ishexadecimalstring(id_number):
        print(id_number, "- is hexadecimal")
    else:
        print(id_number, "- is not")


# checking name type in Boards
for i in range(len(my_json['Boards'])):
    name_n = my_json['Boards'][i]['Name']
    if isinstance(name_n, str):
        print("Boards_Name:", my_json['Boards'][i]['Name'], "- is correct")
    else:
        print("Boards_Name:", my_json['Boards'][i]['Name'], "- is not correct")


# PARAMETERS CHECKING
# looking for name in Parameters
for i in range(len(my_json['Parameters'])):
    if not my_json['Parameters'][i]["Name"]:
        i += 1
    print("Parameters_Name:", my_json['Parameters'][i]["Name"])






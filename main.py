import json
from jsonschema import validate

canIDsSchema = {
    "Boards": [
        {
            "ID": "0x01",
            "Name": "PiBox"
        },
        {
            "ID": "0x02",
            "Name": "Steering wheel"
        },
        {
            "ID": "0x10",
            "Name": "Battery 1"
        },
        {
            "ID": "0x11",
            "Name": "Battery 2"
        }
    ],
}


def isnumericbase(s, base):
    try:
        v = int(s, base)
        # print("true")
        return True
    except ValueError:
        return False


def ishexadecimalstring(s):
    return isnumericbase(s, 16)


# Convert json to python object.
my_json = json.load(open('canIDs.json',))

# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=canIDsSchema)

# print for debug
# print(my_json)
# print(my_json['Boards'][0]['ID'])

for i in range(len(my_json['Boards'])):
    id_number = my_json['Boards'][i]['ID']
    if ishexadecimalstring(id_number):
        print(id_number, "is hexadecimal")

for i in range(len(my_json['Parameters'])):
    print(my_json['Parameters'][i])

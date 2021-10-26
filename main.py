import json
from jsonschema import validate

canIDsSchema = {
    "ID": "0x",

}


def checkhex(string):
    for ch in string:
        if (ch < '0' or ch > '9') and (ch < 'A' or ch > 'F'):
            print(1)
            return
    print(0)


def IsNumericBase(s, base):
    try:
        v = int(s, base)
        print("true")
        return True
    except ValueError:
        return False


def IsHexadecimalString(s):
    return IsNumericBase(s, 16)


IsHexadecimalString("0x34")

# Convert json to python object.
f = open('canIDs.json',)
my_json = json.load(f)

# Validate will raise exception if given json is not
# what is described in schema.
validate(instance=my_json, schema=canIDsSchema)

# print for debug
# print(my_json)

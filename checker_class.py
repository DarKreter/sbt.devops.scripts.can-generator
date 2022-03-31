import jsonschema


class Checker:
    json_object = {}
    json_schema = {}

    def __init__(self, python_json_ob, python_json_schema, json_file_arg):
        self.json_object = python_json_ob
        self.json_schema = python_json_schema
        self.json_path = json_file_arg

    @staticmethod
    def check_placeholder(m_json):
        for i in range(len(m_json['ParamIDs'])):
            if 'ID' not in m_json['ParamIDs'][i]:
                if str(m_json['ParamIDs'][i]['Name']).find("<x>") != -1:
                    continue
                else:
                    print("Couldn't find placeholder (<x>) in ID {} with defined MinID and MaxID.\n".format(str(m_json['ParamIDs'][i]['Name'])))
                    raise
                    
        for i in range(len(m_json['SourceIDs'])):
            if 'ID' not in m_json['SourceIDs'][i]:
                if str(m_json['SourceIDs'][i]['Name']).find("<x>") != -1:
                    continue
                else:
                    print("Couldn't find placeholder (<x>) in ID {} with defined MinID and MaxID.\n".format(str(m_json['SourceIDs'][i]['Name'])))
                    raise

    @staticmethod
    def not_double_name(m_json):
        SubID_Types = ['SourceIDs', 'ParamIDs', 'GroupIDs']
        names = []
        
        for IDtype in SubID_Types:
            for singleID in m_json[IDtype]:
                names.append(singleID["Name"])

            names.sort()

            for i in range(len(names)):
                if i < len(names) - 1:
                    if names[i] == names[i + 1]:
                        print("Name {} in {} occurs more than once.\n".format(names[i], IDtype))
                        raise
            names.clear()

    # check weather MinID is smaller than MaxID
    @staticmethod
    def compare_min_and_max(first, last, name):
        if int(first, 16) >= int(last, 16):
            print("Wrong MinID and MaxID in {}\n".format(name))
            raise


    @staticmethod
    def compare_loop(my_json):
        for j in range(len(my_json['ParamIDs'])):
            if 'ID' not in my_json['ParamIDs'][j]:
                Checker.compare_min_and_max(my_json['ParamIDs'][j]['MinID'], my_json['ParamIDs'][j]["MaxID"], my_json['ParamIDs'][j]["Name"])
        for j in range(len(my_json['SourceIDs'])):
            if 'ID' not in my_json['SourceIDs'][j]:
                Checker.compare_min_and_max(my_json['SourceIDs'][j]['MinID'], my_json['SourceIDs'][j]["MaxID"], my_json['SourceIDs'][j]["Name"])

    @staticmethod
    def id_range_loop(json_object, i, rng):
        max_id = int(json_object[rng][i]['MaxID'], 16)
        curr_id = int(json_object[rng][i]['MinID'], 16)
        addresses = []
        while max_id >= curr_id:
            addresses.append(hex(curr_id))
            curr_id = curr_id + 1
        for address in addresses:
            yield address

    @staticmethod
    def check_for_address_collision(self, json_object):
        table_of_addresses_boards = []
        table_of_addresses_parameters = []
        for i in range(len(json_object["SourceIDs"])):
            if 'ID' not in json_object['SourceIDs'][i]:
                generator = self.id_range_loop(json_object, i, "SourceIDs")
                for j in generator:
                    table_of_addresses_boards.append(j)
            else:
                table_of_addresses_boards.append(hex(int(json_object["SourceIDs"][i]['ID'], 16)))
        for i in range(len(json_object["ParamIDs"])):
            if 'ID' not in json_object['ParamIDs'][i]:
                generator = self.id_range_loop(json_object, i, "ParamIDs")
                for j in generator:
                    table_of_addresses_parameters.append(j)
            else:
                table_of_addresses_parameters.append(hex(int(json_object["ParamIDs"][i]['ID'], 16)))
        if len(table_of_addresses_boards) == len(set(table_of_addresses_boards)):
            if len(table_of_addresses_parameters) == len(set(table_of_addresses_parameters)):
                return 1
            else:
                return 0
        else:
            return 0

    # errors
    def validate(self, json_object, json_schema):
        try:
            jsonschema.validate(instance=json_object, schema=json_schema)
            return 1
        except jsonschema.exceptions.ValidationError as ex:
            print(ex.instance)
            lookup = str(ex.instance)
            if lookup[0] == '{':
                lookup = lookup[1:lookup.find(',')]
                lookup = lookup.replace('\'', '\"')
            with open(self.json_path) as myFile:
                for (num, line) in enumerate(myFile, 1):
                    if lookup in line:
                        print('found at line:', num)
                        raise
            return 0

    def run_checks(self, ob):
        if Checker.validate(self, self.json_object, self.json_schema):
            Checker.check_placeholder(ob)
            Checker.not_double_name(ob)
            Checker.compare_loop(ob)
            if Checker.check_for_address_collision(self, self.json_object):
                return 1
            else:
                return 0
        else:
            return 0

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
        if int(first, 16) == 0:
            print("ID of {} can't be equal to 0.\n".format(name))
            raise

    @staticmethod
    def check_if_group_is_valid(my_json, object):
        if object["Group"] == "DEFAULT":
            return
            
        for groups in my_json['GroupIDs']:
            if groups["Name"] == object["Group"]:
                return
            
        print("{} group in ParamID {} doesn't exist in GroupIDs.\n".format(object["Group"], object["Name"]))
        raise


    @staticmethod
    def check_if_all_groups_are_valid(my_json):
        for object in my_json['ParamIDs']:
            Checker.check_if_group_is_valid(my_json, object)


    @staticmethod
    def compare_params_with_dbc(my_json, dbc_path):
        jsonParam = []
        for object in my_json['ParamIDs']:
            if "ID" in object:
                jsonParam.append( (str(int(object["ID"],16)), object["Name"])  )
            else:
                max_id = int(object['MaxID'], 16)
                curr_id = int(object['MinID'], 16)
                x = 1
                while max_id >= curr_id:
                    jsonParam.append( (str(curr_id), object["Name"].replace("<x>", str(x))) )             
                    curr_id += 1
                    x += 1

                
        # Using readlines() 
        dbc = open(dbc_path, 'r')
        Lines = dbc.readlines()
        
        dbcParam = []
        # Strips the newline character
        for line in Lines:
            if line.find("BO_") != -1:
                dbcParam.append( (line.split()[1], line.split()[2][:-1]) ) 
        
        if len(dbcParam) != len(jsonParam):
            print("List of ParamIDs is not equal to list of DBC frame names\n")
            raise

        jsonParam.sort()
        dbcParam.sort()

        # for i in range(len(dbcParam)):
        #     print("'{}' - '{}'".format(jsonParam[i][0], jsonParam[i][1]))
        #     print("'{}' - '{}'".format(dbcParam[i][0], dbcParam[i][1]))

        for i in range(len(dbcParam)):
            if jsonParam[i][0] != dbcParam[i][0] or jsonParam[i][1] != dbcParam[i][1]:
                print("List of ParamIDs is not equal to list of DBC frame names\n")
                raise


    @staticmethod
    def compare_loop(my_json):
        SubID_Types = ['SourceIDs', 'ParamIDs', 'GroupIDs']
        for subID_type in SubID_Types:
            for j in range(len(my_json[subID_type])):
                if 'ID' not in my_json[subID_type][j]:
                    Checker.compare_min_and_max(my_json[subID_type][j]['MinID'], my_json[subID_type][j]["MaxID"], my_json[subID_type][j]["Name"])
                else:
                    if int(my_json[subID_type][j]['ID'], 16) == 0:
                        print("ID of {} can't be equal to 0.\n".format(my_json[subID_type][j]["Name"]))
                        raise
           
           
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
        table_of_addresses_sources = []
        table_of_addresses_params = []
        for i in range(len(json_object["SourceIDs"])):
            if 'ID' not in json_object['SourceIDs'][i]:
                generator = self.id_range_loop(json_object, i, "SourceIDs")
                for j in generator:
                    table_of_addresses_sources.append(j)
            else:
                table_of_addresses_sources.append(hex(int(json_object["SourceIDs"][i]['ID'], 16)))
        for i in range(len(json_object["ParamIDs"])):
            if 'ID' not in json_object['ParamIDs'][i]:
                generator = self.id_range_loop(json_object, i, "ParamIDs")
                for j in generator:
                    table_of_addresses_params.append(j)
            else:
                table_of_addresses_params.append(hex(int(json_object["ParamIDs"][i]['ID'], 16)))
        if len(table_of_addresses_sources) == len(set(table_of_addresses_sources)):
            if len(table_of_addresses_params) == len(set(table_of_addresses_params)):
                return
            else:
                print("There is address collision in ParamIDs.\n")
                raise
        else:
            print("There is address collision in SourceIDs.\n")
            raise

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

    def run_checks(self, ob, dbc_path):
        if Checker.validate(self, self.json_object, self.json_schema):
            Checker.check_placeholder(ob)
            Checker.not_double_name(ob)
            Checker.compare_loop(ob)
            Checker.check_if_all_groups_are_valid(ob)
            Checker.compare_params_with_dbc(ob, dbc_path)
            Checker.check_for_address_collision(self, self.json_object)
            return 1
        else:
            return 0

from jsonschema import validate


class Checker:
    json_object = {}
    json_schema = {}

    def __init__(self, python_json_ob, python_json_schema):
        self.json_object = python_json_ob
        self.json_schema = python_json_schema

    def check_placeholder(self, m_json):
        for i in range(len(m_json['Parameters'])):
            if 'ID' not in m_json['Parameters'][i]:
                if str(m_json['Parameters'][i]['Name']).find("<x>") != -1:
                    continue
                else:
                    print("error, placeholder")

    def not_double_name(self, m_json):
        name_board = []
        name_parameters = []
        for i in range(len(m_json["Boards"])):
            name_board.append(m_json["Boards"][i]["Name"])
        for i in range(len(m_json["Parameters"])):
            name_parameters.append(m_json["Parameters"][i]["Name"])
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

    # check weather MinID is smaller than MaxID
    def compare_min_and_max(self, first, last):
        if int(first, 16) >> int(last, 16):
            print("Wrong MinID and MaxID input")

    def compare_loop(self, my_json):
        for j in range(len(my_json)):
            if 'ID' not in my_json['Parameters'][j]:
                Checker.compare_min_and_max(self, my_json['Parameters'][j]['MinID'], my_json['Parameters'][j]["MaxID"])

    def validate_schema(self, python_json_object, python_json_schema):
        validate(python_json_object, python_json_schema)
        
    def detect_collisions(self, json_object):
        pass


    def run_checks(self, ob):
        Checker.validate_schema(self, self.json_object, self.json_schema)
        Checker.check_placeholder(self, ob)
        Checker.not_double_name(self, ob)
        Checker.compare_loop(self, ob)

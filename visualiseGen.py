# pattern
# #include "ParametersDict.h"
#
# QMap<quint8, QString> ParametersDict::_boardsDict = {
#         {0x01, "Ground Station"},
#         {0x02, "Pi Box"},
#         {0x03, "MPPT 1"}
# };
#
# QMap<quint16, QString> ParametersDict::_paramsDict = {
#         {0x0001, "Heartbeat"},
#         {0x0002, "MCU Temp"},
#         {0x0010, "MPPT Voltage 1"},
#         {0x0011, "MPPT Voltage 2"}
# };
QMAP_QUINT8_QSTRING_PARAMETERSDICT_BOARD = "QMap<quint8, QString> ParametersDict::_boardsDict = {\n"
QMAP_QUINT16_QSTRING_PARAMETERSDICT_PARAMETERS = "QMap<quint16, QString> ParametersDict::_paramsDict = {\n"
INCLUDE = "#include \"ParametersDict.h\"\n"


class VGenerate:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def id_range_loop(json_object, i, rng):
        max_id = int(json_object[rng][i]['MaxID'], 16)
        curr_id = int(json_object[rng][i]['MinID'], 16)
        addresses = []
        while max_id >= curr_id:
            addresses.append(hex(curr_id))
            curr_id = curr_id + 1
        yield 

    def write_to_file(self, json_object):
        self.name.write(INCLUDE)
        self.name.write(QMAP_QUINT8_QSTRING_PARAMETERSDICT_BOARD)
        # dict loop
        for i in range(len(json_object["Boards"])):
            if 'ID' not in json_object['Boards'][i]:
                generator = self.id_range_loop(json_object, i, "Boards")
                for j in generator:
                    self.name.write(j)
            else:
                self.name.write(json_object['Boards'][i]["Name"] + " = ")
                self.name.write(json_object["Boards"][i]['ID'] + '\n  ')
        self.name.write("};")
        self.name.write(QMAP_QUINT16_QSTRING_PARAMETERSDICT_PARAMETERS)
        # dict loop
        self.name.write("};")
        pass

IF_N_DEF_STRING= "#ifndef F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{}_H\n"
DEFINE_STRING = "#define F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{}_H\n\n"
INCLUDE_STRING = "#include <cstdint>\nnamespace SBT {\nnamespace System {\nnamespace Communication {\n\n"
ENUM_CLASS_UNIT8 = "enum class CANBoardID : unit8_t {\n  "
ENUM_CLASS_UNIT16 = "enum class CANParameterID : unit16_t {\n  "

class HGenerate:
	
	def __init__(self, name):
		self.name = name

	def id_range_loop(self, json_object, i, rng):
		max_id = int(json_object[rng][i]['MaxID'], 16)
		curr_id = int(json_object[rng][i]['MinID'], 16)
		adresses = []
		while(max_id >= curr_id):
			adresses.append(hex(curr_id))
			curr_id = curr_id + 1
		x = 0
		for j in range(len(adresses)):
			x += 1
			yield(json_object[rng][i]["Name"].replace("<x>", str(x)) + " = " + str(adresses[j]) + '\n  ')
			

	def write_to_file(self, json_object):
		# check if file allready exist

		with open(f"{self.name}", "w") as file:
			file.write(IF_N_DEF_STRING.format(self.name[0:self.name.index('.')]))
			file.write(DEFINE_STRING.format(self.name[0:self.name.index('.')]))
			file.write(INCLUDE_STRING)
			file.write(ENUM_CLASS_UNIT8)
			# for loop
			for i in range(len(json_object["Boards"])):
				if 'ID' not in json_object['Boards'][i]:
					generator = self.id_range_loop(json_object, i, "Boards")
					for j in generator:
						file.write(j)
				else:
					file.write(json_object['Boards'][i]["Name"] + " = ")
					file.write(json_object["Boards"][i]['ID'] + '\n  ')
			file.write("} // enum CanBoardsID\n\n")
			file.write(ENUM_CLASS_UNIT16)
			for i in range(len(json_object["Parameters"])):
				if 'ID' not in json_object['Parameters'][i]:
					generator = self.id_range_loop(json_object, i, "Parameters")
					for j in generator:
						file.write(j)
				else:
					file.write(json_object['Parameters'][i]["Name"] + " = ")
					file.write(json_object["Parameters"][i]['ID'] + '\n  ')
			file.write("} // enum CanParameterID\n} //namespace SBT\n} // namespace System\n} // namespace Communication")



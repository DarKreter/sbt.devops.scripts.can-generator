class HGenerate:
	name = ""
	indef = ""
	include = ""
	enum8 = ""
	enum16 = ""
	def __init__(self, indef_name):
		self.name = indef_name
		self.indef = f"#ifndef F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{self.name[0:self.name.index('.')]}_H\n#define F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{self.name[0:self.name.index('.')]}_H\n\n"
		self.include = "#include <cstdint>\nnamespace SBT {\nnamespace System {\nnamespace Communication {\n\n"
		self.enum8 = "enum class CANBoardID : unit8_t {\n  "
		self.enum16 = "enum class CANParameterID : unit16_t {\n  "

	def id_range_loop(self, json_object, i, file, rng):
		max_id = int(json_object[rng][i]['MaxID'], 16)
		curr_id = int(json_object[rng][i]['MinID'], 16)
		adresses = []
		while(max_id >= curr_id):
			adresses.append(hex(curr_id))
			curr_id = curr_id + 1
		x = 1
		for j in range(len(adresses)):
			file.write(json_object[rng][i]["Name"].replace("<x>", str(x)) + " = " + str(adresses[j]) + '\n  ')
			x += 1
			
	def write_to_file(self, json_object):
		# check if file allready exist

		with open(f"{self.name}", "w") as file:
			file.write(self.indef)
			file.write(self.include)
			file.write(self.enum8)
			# for loop
			for i in range(len(json_object["Boards"])):
				if 'ID' not in json_object['Boards'][i]:
					self.id_range_loop(json_object, i, file, "Boards")
				else:
					file.write(json_object['Boards'][i]["Name"] + " = ")
					file.write(json_object["Boards"][i]['ID'] + '\n  ')
			file.write("} // enum CanBoardsID\n\n")
			file.write(self.enum16)
			for i in range(len(json_object["Parameters"])):
				if 'ID' not in json_object['Parameters'][i]:
					self.id_range_loop(json_object, i, file, "Parameters")
				else:
					file.write(json_object['Parameters'][i]["Name"] + " = ")
					file.write(json_object["Parameters"][i]['ID'] + '\n  ')
			file.write("} // enum CanParameterID\n} //namespace SBT\n} // namespace System\n} // namespace Communication")



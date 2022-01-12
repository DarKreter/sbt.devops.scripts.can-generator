class HGenerate:
	name = ""
	indef = ""
	include = ""
	enum8 = ""
	enum16 = ""
	def __init__(self, indef_name):
			self.name = indef_name
			self.indef = f"#ifndef F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{self.name}_H\n#define F1XX_PROJECT_TEMPLATE_LIB_SBT_SDK_F1XX_SBT_SDK_SYSTEM_{self.name}_H"
			self.include = "\n\n#include <cstdint>\nnamespace SBT {\nnamespace System {\nnamespace Communication {"
			self.enum8 = f"\n\nenum class CANBoardID : unit8_t"
			self.enum16 = f"\n\nenum class CANParameterID : unit16_t"

	

	def write_to_file(self, file_name, json_object):
		with open(f"{file_name}", "w") as file:
			file.write(self.indef)
			file.write(self.include)
			file.write(self.enum8)
			# for loop
			file.write("\n    }")
			file.write(self.enum16)
			# for loop
			file.write("\n    }")



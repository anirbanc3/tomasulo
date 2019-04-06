#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:35:21 2019

@author: anirban
"""

def register_to_value(argument): 
	switcher = { 
		0: "r0", 
		1: "r1", 
		2: "r2", 
		3: "r3", 
		4: "r4", 
		5: "r5", 
		6: "r6", 
		7: "r7"
	} 
	return switcher.get(argument, " ") 

def update_register(reg, reg_val):
	global r0, r1, r2, r3, r4, r5, r6, r7
	if reg == 'r0':
		r0 = reg_val
	if reg == 'r1':
		r1 = reg_val
	if reg == 'r2':
		r2 = reg_val
	if reg == 'r3':
		r3 = reg_val
	if reg == 'r4':
		r4 = reg_val
	if reg == 'r5':
		r5 = reg_val
	if reg == 'r6':
		r6 = reg_val
	if reg == 'r7':
		r7 = reg_val


def issue():
	global instruction_queue
	global rs0, rs1, rs2, rs3, rs4;
	current_inst = list(map(lambda each:each.strip("\s"), instruction_queue[0]))
	opcode = int(current_inst[0])
	dest = int(current_inst[2])
	src1 = int(current_inst[4])
	src2 = int(current_inst[6])
	if ((opcode == 0) or (opcode == 1)):
		if (rs0[0] == 0):
			rs0 = [1,opcode,dest,src1,src2]
			del instruction_queue[0]
		elif (rs1[0] == 0):
			rs1 = [1,opcode,dest,src1,src2]
			del instruction_queue[0]
		elif (rs2[0] == 0):
			rs2 = [1,opcode,dest,src1,src2]
			del instruction_queue[0]
		else:
			pass
	else:
		if (rs3[0] == 0):
			rs3 = [1,opcode,dest,src1,src2]
			del instruction_queue[0]
		elif (rs4[0] == 0):
			rs4 = [1,opcode,dest,src1,src2]
			del instruction_queue[0]
		else:
			pass

def dispatch():
	global instruction_queue
	global rs0, rs1, rs2, rs3, rs4;
	if (rs0[0] == 1):
		reg1_val = eval(register_to_value(rs0[3]))
		reg2_val = eval(register_to_value(rs0[4]))
		if (rs0[1] == 0):
			update_register(register_to_value(rs0[2]), reg1_val + reg2_val)
		if (rs0[1] == 1):
			update_register(register_to_value(rs0[2]), reg1_val - reg2_val)
		rs0[0] = 0
	elif (rs1[0] == 1):
		reg1_val = eval(register_to_value(rs1[3]))
		reg2_val = eval(register_to_value(rs1[4]))
		if (rs1[1] == 0):
			update_register(register_to_value(rs1[2]), reg1_val + reg2_val)
		if (rs1[1] == 1):
			update_register(register_to_value(rs1[2]), reg1_val - reg2_val)
		rs1[0] = 0
	elif (rs2[0] == 1):
		reg1_val = eval(register_to_value(rs2[3]))
		reg2_val = eval(register_to_value(rs2[4]))
		if (rs2[1] == 0):
			update_register(register_to_value(rs2[2]), reg1_val + reg2_val)
		if (rs2[1] == 1):
			update_register(register_to_value(rs2[2]), reg1_val - reg2_val)
		rs2[0] = 0
	else:
		pass
	if (rs3[0] == 1):
		reg1_val = eval(register_to_value(rs3[3]))
		reg2_val = eval(register_to_value(rs3[4]))
		if (rs3[1] == 2):
			update_register(register_to_value(rs3[2]), reg1_val * reg2_val)
		if (rs3[1] == 3):
			update_register(register_to_value(rs3[2]), reg1_val / reg2_val)
		rs3[0] = 0
	elif (rs4[0] == 1):
		reg1_val = eval(register_to_value(rs4[3]))
		reg2_val = eval(register_to_value(rs4[4]))
		if (rs4[1] == 2):
			update_register(register_to_value(rs4[2]), reg1_val * reg2_val)
		if (rs4[1] == 3):
			update_register(register_to_value(rs4[2]), reg1_val / reg2_val)
		rs4[0] = 0
	else:
		pass
		
			
	
	
	
	
	
def main():
	with open('input.txt', 'r') as f1:
		data = f1.readlines()
	
	data = list(map(lambda each:each.strip("\n"), data))
	arglen = len(data)
	global instruction_queue
	global r0, r1, r2, r3, r4, r5, r6, r7
	global r_0, r_1, r_2, r_3, r_4, r_5, r_6, r_7
	if (arglen < 12):
		print("not enough arguments")
	else:
		number_of_instruction = int(data[0])
		cycles_of_simulation  = int(data[1])
		if (number_of_instruction > 10):
			print("only first 10 instructions will be processed")
			number_of_instruction = 10
			
		#instruction queue
		for i in range (0,number_of_instruction):
			instruction_queue.append(data[2 + i])
			
		#register file
		r0 = int(data[2 + number_of_instruction + 0])
		r1 = int(data[2 + number_of_instruction + 1])
		r2 = int(data[2 + number_of_instruction + 2])
		r3 = int(data[2 + number_of_instruction + 3])
		r4 = int(data[2 + number_of_instruction + 4])
		r5 = int(data[2 + number_of_instruction + 5])
		r6 = int(data[2 + number_of_instruction + 6])
		r7 = int(data[2 + number_of_instruction + 7])
		
		#register alias table
		r_0 = r0; r_1 = r1; r_2 = r2; r_3 = r3; r_4 = r4; r_5 = r5; r_6 = r6; r_7 = r7
		
		counter = 0
		while (counter < cycles_of_simulation):
			if (instruction_queue != []):
				issue()
#				counter += 1
			dispatch()
			counter += 1			 
		
				
if __name__ == "__main__":
	r0 = 0; r1 = 0; r2 = 0; r3 = 0; r4 = 0; r5 = 0; r6 = 0; r7 = 0 				#register file
	r_0 = 0; r_1 = 0; r_2 = 0; r_3 = 0; r_4 = 0; r_5 = 0; r_6 = 0; r_7 = 0 		#register alias table
	instruction_queue = []						#instruction queue
	
	#reservation stations
	rs0 = [0,'null','null','null','null']
	rs1 = [0,'null','null','null','null'] 
	rs2 = [0,'null','null','null','null'] 
	rs3 = [0,'null','null','null','null']
	rs4 = [0,'null','null','null','null']
	
	main()
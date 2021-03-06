#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 17:35:21 2019

@author: anirban
"""

def register_file(argument): 
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

def register_alias_table(argument): 
	switcher = { 
		0: "r_0", 
		1: "r_1", 
		2: "r_2", 
		3: "r_3", 
		4: "r_4", 
		5: "r_5", 
		6: "r_6", 
		7: "r_7"
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
        
def update_rat(reg, reg_val):
	global r_0, r_1, r_2, r_3, r_4, r_5, r_6, r_7
	if reg == 'r_0':
		r_0 = reg_val
	if reg == 'r_1':
		r_1 = reg_val
	if reg == 'r_2':
		r_2 = reg_val
	if reg == 'r_3':
		r_3 = reg_val
	if reg == 'r_4':
		r_4 = reg_val
	if reg == 'r_5':
		r_5 = reg_val
	if reg == 'r_6':
		r_6 = reg_val
	if reg == 'r_7':
		r_7 = reg_val

def fillUp(opcode,reg1,reg2,rat1,rat2,clk):
    if ((rat1 == '-') and (rat2 == '-')):
        rst = [1,opcode,reg1,reg2,'-','-',0,clk,0,0]
    elif ((rat1 == '-') and (rat2 != '-')):
        rst = [1,opcode,reg1,'-','-',rat2,0,clk,0,0]
    elif ((rat1 != '-') and (rat2 == '-')):
        rst = [1,opcode,'-',reg2,rat1,'-',0,clk,0,0]
    else:
        rst = [1,opcode,'-','-',rat1,rat2,0,clk,0,0]
    return rst

def issue():
    global instruction_queue, counter
    global rs0, rs1, rs2, rs3, rs4, r_0, r_1, r_2, r_3, r_4, r_5, r_6, r_7
    current_inst = list(map(lambda each:each.strip("\s"), instruction_queue[0]))
    opcode = int(current_inst[0])
    dest = register_alias_table(int(current_inst[2]))
    rat1 = eval(register_alias_table(int(current_inst[4])))
    rat2 = eval(register_alias_table(int(current_inst[6])))
    reg1 = eval(register_file(int(current_inst[4])))
    reg2 = eval(register_file(int(current_inst[6])))
    counter = counter+1
    if ((opcode == 0) or (opcode == 1)):
        if (rs0[0] == 0):
            rs0 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            update_rat(dest,'rs0')
            del instruction_queue[0]
        elif (rs1[0] == 0):
            rs1 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            update_rat(dest,'rs1')
            del instruction_queue[0]
        elif (rs2[0] == 0):
            rs2 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            update_rat(dest,'rs2')
            del instruction_queue[0]
        else:
            pass
    else:
        if (rs3[0] == 0):
            rs3 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            update_rat(dest,'rs3')
            del instruction_queue[0]
        elif (rs4[0] == 0):
            rs4 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            update_rat(dest,'rs4')
            del instruction_queue[0]
        else:
            pass

def dispatch():
    global instruction_queue, counter, inst_end
    global rs0, rs1, rs2, rs3, rs4;
    result1 = None; result2 = None; flag1 = None; flag2 = None;
    exct = None; excl = None;
    if (inst_end == True):
        counter = counter + 1
    if ((rs0[0] == 1) and (counter > rs0[7]) and (rs0[6] == 0)):
        if ((rs0[2] != '-') and (rs0[3] != '-')):
            if (rs0[1] == 0):
                result1 = rs0[2] + rs0[3] 
            else:
                result1 = rs0[2] - rs0[3] 
            rs0[6] = 1; flag1 = 0; exct = counter + 2
            rs0[8] = result1; rs0[9] = exct
        else:
            pass
    elif ((rs1[0] == 1) and (counter > rs1[7]) and (rs1[6] == 0)):
        if ((rs1[2] != '-') and (rs1[3] != '-')):
            if (rs1[1] == 0):
                result1 = rs1[2] + rs1[3] 
            else:
                result1 = rs1[2] - rs1[3] 
            rs1[6] = 1; flag1 = 1; exct = counter + 2
            rs1[8] = result1; rs1[9] = exct
        else:
            pass
    elif ((rs2[0] == 1) and (counter > rs2[7]) and (rs2[6] == 0)):
        if ((rs2[2] != '-') and (rs2[3] != '-')):
            if (rs2[1] == 0):
                result1 = rs2[2] + rs2[3] 
            else:
                result1 = rs2[2] - rs2[3] 
            rs2[6] = 1; flag1 = 2; exct = counter + 2
            rs2[8] = result1; rs2[9] = exct
        else:
            pass
    else:
        pass
    
    if ((rs3[0] == 1) and (counter > rs3[7]) and (rs3[6] == 0)):
        if ((rs3[2] != '-') and (rs3[3] != '-')):
            if (rs3[1] == 2):
                result2 = rs3[2] * rs3[3] 
                excl = counter + 10
                rs3[8] = result2; rs3[9] = excl
            else:
                result2 = rs3[2] / rs3[3] 
                excl = counter + 40
                rs3[8] = result2; rs3[9] = excl
            rs3[6] = 1; flag2 = 3
        else:
            pass
    elif ((rs4[0] == 1) and (counter > rs4[7]) and (rs4[6] == 0)):
        if ((rs4[2] != '-') and (rs4[3] != '-')):
            if (rs4[1] == 2):
                result2 = rs4[2] * rs4[3] 
                excl = counter + 10
                rs4[8] = result2; rs4[9] = excl
            else:
                result2 = rs4[2] / rs4[3] 
                excl = counter + 40
                rs4[8] = result2; rs4[9] = excl
            rs4[6] = 1; flag2 = 4
        else:
            pass
    else:
        pass

	
def broadcast(flag, result):
    global rs0, rs1, rs2, rs3, rs4;
    global counter
    counter = counter + 1
    if (flag == 0):
        if(rs1[4] == 'rs0'):
            rs1[2] = result
            rs1[4] = '-'
        if(rs2[4] == 'rs0'):
            rs2[2] = result
            rs2[4] = '-'
        if(rs3[4] == 'rs0'):
            rs3[2] = result
            rs3[4] = '-'
        if(rs4[4] == 'rs0'):
            rs4[2] = result
            rs4[4] = '-'
    if (flag == 1):
        if(rs0[4] == 'rs1'):
            rs0[2] = result
            rs0[4] = '-'
        if(rs2[4] == 'rs1'):
            rs2[2] = result
            rs2[4] = '-'
        if(rs3[4] == 'rs1'):
            rs3[2] = result
            rs3[4] = '-'
        if(rs4[4] == 'rs1'):
            rs4[2] = result
            rs4[4] = '-'
    if (flag == 2):
        if(rs0[4] == 'rs2'):
            rs0[2] = result
            rs0[4] = '-'
        if(rs1[4] == 'rs2'):
            rs1[2] = result
            rs1[4] = '-'
        if(rs3[4] == 'rs2'):
            rs3[2] = result
            rs3[4] = '-'
        if(rs4[4] == 'rs2'):
            rs4[2] = result
            rs4[4] = '-'
    if (flag == 3):
        if(rs1[4] == 'rs3'):
            rs1[2] = result
            rs1[4] = '-'
        if(rs2[4] == 'rs3'):
            rs2[2] = result
            rs2[4] = '-'
        if(rs0[4] == 'rs3'):
            rs0[2] = result
            rs0[4] = '-'
        if(rs4[4] == 'rs3'):
            rs4[2] = result
            rs4[4] = '-'
    if (flag == 4):
        if(rs1[4] == 'rs4'):
            rs1[2] = result
            rs1[4] = '-'
        if(rs2[4] == 'rs4'):
            rs2[2] = result
            rs2[4] = '-'
        if(rs3[4] == 'rs4'):
            rs3[2] = result
            rs3[4] = '-'
        if(rs0[4] == 'rs4'):
            rs0[2] = result
            rs0[4] = '-'
    writeback(flag, result)
    
def getRat(resstn):
    global r_0, r_1, r_2, r_3, r_4, r_5, r_6, r_7
    if (r_0 == resstn):
        r_0 = '-'
        return 'r0'
    if (r_1 == resstn):
        r_1 = '-'
        return 'r1'
    if (r_2 == resstn):
        r_2 = '-'
        return 'r2'
    if (r_3 == resstn):
        r_3 = '-'
        return 'r3'
    if (r_4 == resstn):
        r_4 = '-'
        return 'r4'
    if (r_5 == resstn):
        r_5 = '-'
        return 'r5'
    if (r_6 == resstn):
        r_6 = '-'
        return 'r6'
    if (r_7 == resstn):
        r_7 = '-'
        return 'r7'
    
def writeback(flag, result):
    global rs0, rs1, rs2, rs3, rs4;
    global r0, r1, r2, r3, r4, r5, r6, r7
    
    if (flag == 0):
        reg = getRat('rs0')
        update_register(reg, result)
        rs0[0] = 0; rs0[6] = 0
    if (flag == 1):
        reg = getRat('rs1')
        update_register(reg, result)
        rs1[0] = 0; rs1[6] = 0
    if (flag == 2):
        reg = getRat('rs2')
        update_register(reg, result)
        rs2[0] = 0; rs2[6] = 0
    if (flag == 3):
        reg = getRat('rs3')
        update_register(reg, result)
        rs3[0] = 0; rs3[6] = 0
    if (flag == 4):
        reg = getRat('rs4')
        update_register(reg, result)
        rs4[0] = 0; rs4[6] = 0
        
def readyToBroadcast():
    global counter
    contender = [0,0,0,0,0]
    if ((rs0[9] <= counter) and (rs0[6] == 1)):
        contender[0] = 1
    if ((rs1[9] <= counter) and (rs1[6] == 1)):
        contender[1] = 1
    if ((rs2[9] <= counter) and (rs2[6] == 1)):
        contender[2] = 1
    if ((rs3[9] <= counter) and (rs3[6] == 1)):
        contender[3] = 1
    if ((rs4[9] <= counter) and (rs4[6] == 1)):
        contender[4] = 1
    
    if ((contender[3] == 1) or (contender[4] == 1)):
        if (contender[3] == 1):
            return 3, rs3[8]
        else:
            return 4, rs4[8]
    else:
        if (contender[0] == 1):
            return 0, rs0[8]
        if (contender[1] == 1):
            return 1, rs1[8]
        if (contender[2] == 1):
            return 2, rs2[8]
        else:
            return None, None
            
    
    
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
        
        global counter, inst_end
        while (counter < cycles_of_simulation):
            if (instruction_queue != []):
                issue()
            else:
                inst_end = True
            if (counter > 1):
                dispatch()
            fl , res = readyToBroadcast()
            if (fl != None):
                broadcast(fl, res)
        print(rs0)
        print(rs1)
        print(rs2)
        print(rs3)
        print(rs4)
        print(instruction_queue)
        
       		
if __name__ == "__main__":
    r0 = 0; r1 = 0; r2 = 0; r3 = 0; r4 = 0; r5 = 0; r6 = 0; r7 = 0 				#register file
    r_0 = '-'; r_1 = '-'; r_2 = '-'; r_3 = '-'; r_4 = '-'; r_5 = '-'; r_6 = '-'; r_7 = '-'; 		#register alias table
    instruction_queue = []						#instruction queue
    counter = 0; 
    inst_end = False
	#reservation stations
    rs0 = [0,'null','null','null','null','null','null',0,0,0]
    rs1 = [0,'null','null','null','null','null','null',0,0,0]
    rs2 = [0,'null','null','null','null','null','null',0,0,0]
    rs3 = [0,'null','null','null','null','null','null',0,0,0]
    rs4 = [0,'null','null','null','null','null','null',0,0,0]
    
    main()
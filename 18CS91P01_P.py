#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 23:50:07 2019

@author: anirban727
"""


def fillUp(opcode,reg1,reg2,rat1,rat2,clk):
    if ((rat1 == None) and (rat2 == None)):
        rst = [1,opcode,reg1,reg2,None,None,0,clk,0,0]
    elif ((rat1 == None) and (rat2 != None)):
        rst = [1,opcode,reg1,None,None,rat2,0,clk,0,0]
    elif ((rat1 != None) and (rat2 == None)):
        rst = [1,opcode,None,reg2,rat1,None,0,clk,0,0]
    else:
        rst = [1,opcode,None,None,rat1,rat2,0,clk,0,0]
    return rst

def issue():
    global instruction_queue, counter
    global rs0, rs1, rs2, rs3, rs4;
    global regalias, register
    current_inst = list(map(lambda each:each.strip("\s"), instruction_queue[0]))
    opcode = int(current_inst[0])
    dest = int(current_inst[2])
    rat1 = regalias[int(current_inst[4])]
    rat2 = regalias[int(current_inst[6])]
    reg1 = register[int(current_inst[4])]
    reg2 = register[int(current_inst[6])]
    counter = counter+1

    if ((opcode == 0) or (opcode == 1)):
        if (rs0[0] == 0):
            rs0 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            regalias[dest] = 0
            del instruction_queue[0]
        elif (rs1[0] == 0):
            rs1 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            regalias[dest] = 1
            del instruction_queue[0]
        elif (rs2[0] == 0):
            rs2 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            regalias[dest] = 2
            del instruction_queue[0]
        else:
            pass
    else:
        if (rs3[0] == 0):
            rs3 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            regalias[dest] = 3
            del instruction_queue[0]
        elif (rs4[0] == 0):
            rs4 = fillUp(opcode,reg1,reg2,rat1,rat2,counter)
            regalias[dest] = 4
            del instruction_queue[0]
        else:
            pass

def dispatch():
    global instruction_queue, counter, inst_end
    global rs0, rs1, rs2, rs3, rs4;

    if (inst_end == True):
        counter = counter + 1
    if ((rs0[0] == 1) and (counter > rs0[7]) and (rs0[6] == 0)):
        if ((rs0[2] != None) and (rs0[3] != None)):
            if (rs0[1] == 0):
                rs0[8] = rs0[2] + rs0[3] 
            else:
                rs0[8] = rs0[2] - rs0[3] 
            rs0[6] = 1; rs0[9] = counter + 2
        else:
            pass
    elif ((rs1[0] == 1) and (counter > rs1[7]) and (rs1[6] == 0)):
        if ((rs1[2] != None) and (rs1[3] != None)):
            if (rs1[1] == 0):
                rs1[8] = rs1[2] + rs1[3] 
            else:
                rs1[8] = rs1[2] - rs1[3] 
            rs1[6] = 1; rs1[9] = counter + 2
        else:
            pass
    elif ((rs2[0] == 1) and (counter > rs2[7]) and (rs2[6] == 0)):
        if ((rs2[2] != None) and (rs2[3] != None)):
            if (rs2[1] == 0):
                rs2[8] = rs2[2] + rs2[3] 
            else:
                rs2[8] = rs2[2] - rs2[3] 
            rs2[6] = 1; rs2[9] = counter + 2
        else:
            pass
    else:
        pass
    
    if ((rs3[0] == 1) and (counter > rs3[7]) and (rs3[6] == 0)):
        if ((rs3[2] != None) and (rs3[3] != None)):
            if (rs3[1] == 2):
                rs3[8] = rs3[2] * rs3[3] 
                rs3[9] = counter + 10
            else:
                rs3[8] = rs3[2] / rs3[3] 
                rs3[9] = counter + 40
            rs3[6] = 1
        else:
            pass
    elif ((rs4[0] == 1) and (counter > rs4[7]) and (rs4[6] == 0)):
        if ((rs4[2] != None) and (rs4[3] != None)):
            if (rs4[1] == 2):
                rs4[8] = rs4[2] * rs4[3] 
                rs4[9] = counter + 10
            else:
                rs4[8] = rs4[2] / rs4[3] 
                rs4[9] = counter + 40
            rs4[6] = 1
        else:
            pass
    else:
        pass

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

def broadcast(flag, result):
    global rs0, rs1, rs2, rs3, rs4;
    global counter
    counter = counter + 1
    if(rs0[4] == flag):
        rs0[2] = result
        rs0[4] = None
    if(rs1[4] == flag):
        rs1[2] = result
        rs1[4] = None
    if(rs2[4] == flag):
        rs2[2] = result
        rs2[4] = None
    if(rs3[4] == flag):
        rs3[2] = result
        rs3[4] = None
    if(rs4[4] == flag):
        rs4[2] = result
        rs4[4] = None
    writeback(flag, result)
    
def writeback(flag, result):
    global rs0, rs1, rs2, rs3, rs4;
    global register, regalias
    for i in range(0,8):
        if regalias[i] == flag:
            regalias[i] = None
            register[i] = result
    if (flag == 0):
        rs0[0] = 0; rs0[6] = 0
    if (flag == 1):
        rs1[0] = 0; rs1[6] = 0
    if (flag == 2):
        rs2[0] = 0; rs2[6] = 0
    if (flag == 3):
        rs3[0] = 0; rs3[6] = 0
    if (flag == 4):
        rs4[0] = 0; rs4[6] = 0

def main():
    with open('input.txt', 'r') as f1:
        data = f1.readlines()
    
    data = list(map(lambda each:each.strip("\n"), data))
    arglen = len(data)
    global instruction_queue
    global register
    global regalias
    global reservation_table
    if (arglen < 12):
        print("not enough arguments")
    else:
        number_of_instruction = int(data[0])
        cycles_of_simulation  = int(data[1])
        if (number_of_instruction > 10):
            print("only first 10 instructions will be processed")
            number_of_instruction = 10
			
		#fill up the instruction queue
        for i in range (0,number_of_instruction):
            instruction_queue.append(data[2 + i])
			
		#update register file with initial values
        for i in range(0,8):
            register[i] = int(data[2 + number_of_instruction + i])
        
        global counter, inst_end
        while (counter < cycles_of_simulation):
            if (instruction_queue != []):
                issue()
            else:
                inst_end = True
            if (counter > 1):
                dispatch()
            fl , res = readyToBroadcast()
#            print(fl, res)
            if (fl != None):
                broadcast(fl, res)
            
            reservation_table = [['RS0'] + rs0[:7], ['RS1'] + rs1[:7], ['RS2'] + rs2[:7],  ['RS3'] + rs3[:7], ['RS4'] + rs4[:7]]
#            print(reservation_table)
#            print(register)
#            print(regalias)
#            print(' ')
        
        with open('output.txt','w') as f2:
            f2.write("             Busy      Op          Vj      Vk        Qj         Qk      Disp \n")
            f2.write("--------------------------------------------------------------------------------------\n")
            for index, item in enumerate(reservation_table):
				for k, l in enumerate(item):
					if (l == None):
						f2.write("    ")
					else:
						if (k == 2):
							if (l == 0):
								f2.write("Add")
							if (l == 1):
								f2.write("Sub")
							if (l == 2):
								f2.write("Mul")
							if (l == 3):
								f2.write("Div")
							else:
								f2.write("   ")
						if ((k == 5) or (k == 6)):
							if (l == 0):
								f2.write("RS0")
							if (l == 1):
								f2.write("RS1")
							if (l == 2):
								f2.write("RS2")
							if (l == 3):
								f2.write("RS3")
							if (l == 3):
								f2.write("RS4")
							else:
								f2.write("   ")
						if (k == 0 or k == 1 or k == 3 or k == 4 or k == 7):
							f2.write(str(l))
					if (k == 0):
						f2.write("    ")
					f2.write("       ")
				f2.write("\n")

            f2.write("___________________________________________________________________________________________\n\n")
            f2.write("             RF          RAT     \n")       
            f2.write("--------------------------------------------------------------------------------------\n")
            for i in range(0,8):
				f2.write(str(i)+":           ")
				f2.write(str(register[i])+"           ")
				if (regalias[i] == 0):
					f2.write("RS0")
				elif (regalias[i] == 1):
					f2.write("RS1")
				elif (regalias[i] == 2):
					f2.write("RS2")
				elif (regalias[i] == 3):
					f2.write("RS3")
				elif (regalias[i] == 3):
					f2.write("RS4")
				else:
					f2.write("   ")

				f2.write("\n")

            f2.write("___________________________________________________________________________________________\n\n")
            f2.write("      Instruction Queue    \n")       
            f2.write("--------------------------------------------------------------------------------------\n")
            if (inst_end == False):
                for instruction in instruction_queue:
                    for index, item in enumerate(instruction):
						if (index == 0):
							if (item == '0'):
								f2.write("Add    ")
							elif (item == '1'):
								f2.write("Sub    ")
							elif (item == '2'):
								f2.write("Mul    ")
							elif (item == '3'):
								f2.write("Div    ")
						else:
							if (item == '0'):
								f2.write("R0   ")
							elif (item == '1'):
								f2.write("R1   ")
							elif (item == '2'):
								f2.write("R2   ")
							elif (item == '3'):
								f2.write("R3   ")
							elif (item == '4'):
								f2.write("R4   ")
							elif (item == '5'):
								f2.write("R5   ")
							elif (item == '6'):
								f2.write("R6   ")
							elif (item == '7'):
								f2.write("R7   ")
                    f2.write("\n")
            else:
				f2.write("All instructions processed. Queue empty!\n")

            f2.write("___________________________________________________________________________________________\n\n")



if __name__ == "__main__":
    register = [0, 0, 0, 0, 0, 0, 0, 0] 			#register file
    regalias = [None, None, None, None, None, None, None, None]         #register alias table
    instruction_queue = []						#instruction queue
    counter = 0; 
    inst_end = False
	#reservation stations
    rs0 = [0,None,None,None,None,None,None,0,0,0]
    rs1 = [0,None,None,None,None,None,None,0,0,0]
    rs2 = [0,None,None,None,None,None,None,0,0,0]
    rs3 = [0,None,None,None,None,None,None,0,0,0]
    rs4 = [0,None,None,None,None,None,None,0,0,0]
    reservation_table = []
    
    main()

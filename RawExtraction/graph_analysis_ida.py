#coding=utf-8
from idautils import *
from idaapi import *
from idc import *

def getfunc_consts(func):
	strings = []
	consts = []
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	for bl in blocks:
		strs, conts = getBBconsts(bl)
		strings += strs
		consts += conts
	return strings, consts
	

def getConst(ea, offset):
	strings = []
	consts = []
	optype1 = GetOpType(ea, offset)
	if optype1 == idaapi.o_imm:
		imm_value = GetOperandValue(ea, offset)
		if 0<= imm_value <= 10:
			consts.append(imm_value)
		else:
			if idaapi.isLoaded(imm_value) and idaapi.getseg(imm_value):
				str_value = GetString(imm_value)
				if str_value is None:
					str_value = GetString(imm_value+0x40000)
					if str_value is None:
						consts.append(imm_value)
					else:
						re = all(40 <= ord(c) < 128 for c in str_value)
						if re:
							strings.append(str_value)
						else:
							consts.append(imm_value)
				else:
					re = all(40 <= ord(c) < 128 for c in str_value)
					if re:
						strings.append(str_value)
					else:
						consts.append(imm_value)
			else:
				consts.append(imm_value)
	return strings, consts

def getBBconsts(bl):
	strings = []
	consts = []
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		if opcode in ['la','jalr','call', 'jal']:
			inst_addr = NextHead(inst_addr)
			continue
		strings_src, consts_src = getConst(inst_addr, 0)
		strings_dst, consts_dst = getConst(inst_addr, 1)
		strings += strings_src
		strings += strings_dst
		consts += consts_src
		consts += consts_dst
		try:
			strings_dst, consts_dst = getConst(inst_addr, 2)
			consts += consts_dst
			strings += strings_dst
		except:
			pass

		inst_addr = NextHead(inst_addr)
	return strings, consts

def getFuncCalls(func):
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	sumcalls = 0
	for bl in blocks:
		callnum = calCalls(bl)
		sumcalls += callnum
	return sumcalls

def getcodesquence(bl):
	sequence=[]
	#print("EEEEEEEEEEEEEEEEEEEEEEEE")
	x86_AI = {'add':1, 'sub':1, 'div':1, 'imul':1, 'idiv':1, 'mul':1, 'shl':1, 'dec':1, 'inc':1}
	mips_AI = {'add':1, 'addu':1, 'addi':1, 'addiu':1, 'mult':1, 'multu':1, 'div':1, 'divu':1}
	x86_TI = {'jmp': 1, 'jz': 1, 'jnz': 1, 'js': 1, 'je': 1, 'jne': 1, 'jg': 1, 'jle': 1, 'jge': 1, 'ja': 1, 'jnc': 1,
			  'call': 1}
	mips_TI = {'beq': 1, 'bne': 1, 'bgtz': 1, "bltz": 1, "bgez": 1, "blez": 1, 'j': 1, 'jal': 1, 'jr': 1, 'jalr': 1}
	arm_TI = {'MVN': 1, "MOV": 1}
	# in each opcode, there are three lines, one is the arm, one is the x86, and the other is mips.
	GDTI={'MVN':2, "MOV":1,'LDR':3,'LDRB':4,'LDRH':5,'STR':6,'STRB':7,'STRH':8,'LDM':9,'STM':9,'SWP':10,'SWPB':11,
		  'mov':1,'movsx':2,'movzx':3,'push':4,'pop':5,'push':6,'pusha':7,'pope':8,'pushed':9,'popad':10,'bswap':11,'xchg':12,'cmpxchg':13,'xadd':14,'xlat':15,'mvn':16,'cmp':17,'tst':18,'tea':19,
		  'lui':1,'lw':2,'sw':3}

	IOPTI={'in':1,'out':2,}
	DATI={'lea':1,'lds':2,'les':3,'lfs':4,'lgs':5,'les':6}
	FTI={'lahf':1,'sahf':2,'push':3,'popf':4,'pushd':5,'popd':6}
	ADO={'add':1,'adc':2,'inc':3,'aaa':4,'daa':5,'sub':6,'sbb':7,'dec':8,'nec':9,'cmp':10,
		 'ADD':1, 'ADC':2,'SUB':3,'C':4,'R':5,'RSC':6,'TEQ':8, 'TST':9,'CMP':10,'MUL':13,'MLA':12,'SMULL':11,'SMLAL':14,'UMULL':15,'UMLAL':16,
		 'aas':11,'das':12,'mul':13,'imul':14,'aam':15,'div':16,'idiv':17,'aad':18,'cbw':19,
		 'cwd':20,'cwde':21,'cdq':22,'c':23,'r':24,'rsc':25,'mla':13,'smull':14,'umull':15,'umlal':16,
		 'add':1,'addu':2,'sub':6,'subu':7,'addi':1,'addiu':2}
	LDO={'and':1,'or':2,'xor':3,'not':4,'test':5,'shl':6,'sal':7,'shr':8,'sar':9,'rol':10,'ror':11,'rcl':12,'rcr':13,
		 'orr':14,'eor':15,'bic':16,
		 'and':1,'or':2,'xor':3,'nor':4,'andi':5,'ori':6,'xori':7,
		 'AND':1,'ORR':2,'EOR':3,'BIC':4,'LSL':5,'LSR':6,}
	SI={'movs':1,'cmps':2,'scas':3,'lods':4,'stos':5,'rep':6,'repe':7,'repen':8,'repc':9,'repnc':10}
	UBI={'jump':1,'call':2,'ret':3,
		 'j':1,'jal':2,'jr':3}
	CBI={'ja':1,'jnz':15,'jnbe':14,'jae':2,'jnb':10,'jb':3,'jbe':4,'jg':5,'jge':6,'jl':7,'jle':8,'je':9,'jne':11,'jc':12,'jnc':13,'jno':14,'jnp':15,'jns':16,'jo':17,'jp':18,'js':19,
		 'slt':1,'sltu':2,'sll':3,'srl':4,'sra':5,'sllv':6,'srlv':7,'srav':8,"beq":9, "bne":10,'slti':11,'sltiu':12,
		 #"beqz":1 "bgez":4, "b":5, "bnez":6, "bgtz":7, "bltz":8, "blez":9, "bgt":10, "bge":11, "blt":12, "ble":13, "bgtu":14, "bgeu":15, "bltu":16, "bleu":17,
		 "B":1, "BAL":2, "BNE":3, "BEQ":4, "BPL":5, "BMI":6, "BCC":7, "BLO":8, "BCS":9, "BHS":10, "BVC":11, "BVS":12, "BGT":13, "BGE":14, "BLT":15, "BLE":16, "BHI":17 ,"BLS":18,'BL':19,'BLX':20}
	LCI={'loop':1,'loope':2,'loopne':3,'jcxz':4,'jecxz':5}
	II={'int':1,'into':2,'iret':3,
		'SWI':1,'BKPT':2,}
	PCI={'hlt':1,'wait':2,'esc':3,'lock':4,'nop':5,'stc':6,'clc':7,'cmc':8,'std':9,'cld':10,'sti':11,'cli':12,
		 'CDP':1,'LDC':2,'STC':3,'MCR':4,'MRC':5,'MRS':6,'MSR':7}
	PI={'dw':1,'proc':2,'ends':3,'segment':4,'assume':5,'ends':6,'end':7,
		'GBLA':1,'GBLL':2,'GBLS':3,'LCLA':4,'LCLL':5,'LCLS':6,'SETA':7,'SETL':8,'SETS':9,'RLIST':10,'DCB':11,'DCW':12,'DCD':13,'DCFD':14,
		'DCFS':15,'DCQ':16,'SPACE':17,'MAP':18,'FILED':19}
	opcodenum=0
	#blocks=[(v.startEA, v.endEA) for v in FlowChart(func)]

	start = bl[0]
	end = bl[1]

	inst_addr = start
	while inst_addr < end:

		opcode = GetMnem(inst_addr)

		if opcode in GDTI:
			opcodenum=GDTI.get(opcode)
			sequence.append(1)
		if opcode in IOPTI:
			opcodenum=IOPTI.get(opcode)
			sequence.append(2)
		if opcode in DATI:
			opcodenum=DATI.get(opcode)
			sequence.append(3)
		if opcode in PI:
			opcodenum=PI.get(opcode)
			sequence.append(4)
		if opcode in FTI:
			opcodenum=FTI.get(opcode)
			sequence.append(5)
		if opcode in ADO:
			opcodenum=ADO.get(opcode)
			sequence.append(6)
		if opcode in LDO:
			opcodenum=LDO.get(opcode)
			sequence.append(7)
		if opcode in SI:
			opcodenum=SI.get(opcode)
			sequence.append(8)
		if opcode in UBI:
			opcodenum=UBI.get(opcode)
			sequence.append(9)
		if opcode in CBI:
			opcodenum=CBI.get(opcode)
			sequence.append(10)
		if opcode in LCI:
			opcodenum=LCI.get(opcode)
			sequence.append(11)
		if opcode in II:
			opcodenum=II.get(opcode)
			sequence.append(12)
		if opcode in PCI:

			opcodenum=PCI.get(opcode)
			#print("CCCCCCCCCCCCCCCCCCCC")
			sequence.append(13)

		sequence.append(opcodenum)
		print sequence
		inst_addr = NextHead(inst_addr)
	return sequence


def getLogicInsts(func):
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	sumcalls = 0
	for bl in blocks:
		callnum = calLogicInstructions(bl)
		sumcalls += callnum
	return sumcalls

def getTransferInsts(func):
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	sumcalls = 0
	for bl in blocks:
		callnum = calTransferIns(bl)
		sumcalls += callnum
	return sumcalls

def getIntrs(func):
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	sumcalls = 0
	for bl in blocks:
		callnum = calInsts(bl)
		sumcalls += callnum
	return sumcalls	


	
	
def getLocalVariables(func):
	args_num = get_stackVariables(func.startEA)
	return args_num

def getBasicBlocks(func):
	blocks = [(v.startEA, v.endEA) for v in FlowChart(func)]
	return len(blocks)

def getIncommingCalls(func):
	refs = CodeRefsTo(func.startEA, 0)
	re = len([v for v in refs])
	return re


def get_stackVariables(func_addr):
	#print func_addr
	args = []
	stack = GetFrame(func_addr)
	if not stack:
			return 0
	firstM = GetFirstMember(stack)
	lastM = GetLastMember(stack)
	i = firstM
	while i <=lastM:
		mName = GetMemberName(stack,i)
		mSize = GetMemberSize(stack,i)
		if mSize:
				i = i + mSize
		else:
				i = i+4
		if mName not in args and mName and 'var_' in mName:
			args.append(mName)
	return len(args)



def calArithmeticIns(bl):
	x86_AI = {'add':1, 'sub':1, 'div':1, 'imul':1, 'idiv':1, 'mul':1, 'shl':1, 'dec':1, 'inc':1}
	mips_AI = {'add':1, 'addu':1, 'addi':1, 'addiu':1, 'mult':1, 'multu':1, 'div':1, 'divu':1}
	calls = {}
	calls.update(x86_AI)
	calls.update(mips_AI)
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		if opcode in calls:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num

def calCalls(bl):
	calls = {'call':1, 'jal':1, 'jalr':1}
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		if opcode in calls:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num

def calInsts(bl):
	start = bl[0]
	end = bl[1]
	ea = start
	num = 0
	while ea < end:
		num += 1
		ea = NextHead(ea)
	return num

def calLogicInstructions(bl):
	x86_LI = {'and':1, 'andn':1, 'andnpd':1, 'andpd':1, 'andps':1, 'andnps':1, 'test':1, 'xor':1, 'xorpd':1, 'pslld':1}
	mips_LI = {'and':1, 'andi':1, 'or':1, 'ori':1, 'xor':1, 'nor':1, 'slt':1, 'slti':1, 'sltu':1}
	calls = {}
	calls.update(x86_LI)
	calls.update(mips_LI)
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		if opcode in calls:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num

def calSconstants(bl):
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		if opcode in calls:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num


def calNconstants(bl):
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		optype1 = GetOpType(inst_addr, 0)
		optype2 = GetOpType(inst_addr, 1)
		if optype1 == 5 or optype2 == 5:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num

def retrieveExterns(bl, ea_externs):
	externs = []
	start = bl[0]
	end = bl[1]
	inst_addr = start
	while inst_addr < end:
		refs = CodeRefsFrom(inst_addr, 1)
		try:
			ea = [v for v in refs if v in ea_externs][0]
			externs.append(ea_externs[ea])
		except:
			pass
		inst_addr = NextHead(inst_addr)
	return externs

def calTransferIns(bl):
	x86_TI = {'jmp':1, 'jz':1, 'jnz':1, 'js':1, 'je':1, 'jne':1, 'jg':1, 'jle':1, 'jge':1, 'ja':1, 'jnc':1, 'call':1}
	mips_TI = {'beq':1, 'bne':1, 'bgtz':1, "bltz":1, "bgez":1, "blez":1, 'j':1, 'jal':1, 'jr':1, 'jalr':1}
	arm_TI = {'MVN':1, "MOV":1}
	calls = {}
	calls.update(x86_TI)
	calls.update(mips_TI)
	start = bl[0]
	end = bl[1]
	invoke_num = 0
	inst_addr = start
	while inst_addr < end:
		opcode = GetMnem(inst_addr)
		re = [v for v in calls if opcode in v]
		if len(re) > 0:
			invoke_num += 1
		inst_addr = NextHead(inst_addr)
	return invoke_num
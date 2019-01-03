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

def getcodesquence(func):
	sequence=[]
	GDTI={‘mov’:1,’movsx’:2,’movzx’:3,’push’:4,’pop’:5,’push’:6,’pusha’:7,’pope’:8,’pushed’:9,’popad’:10,’bswap’:11,’xchg’:12,’cmpxchg’:13,’xadd’:14,’xlat’:15,’mvn’:16,’cmp’:17,’tst’:18,’tea’:19}
　　
	IOPTI={‘in’:1,’out’:2}
	DATI={‘lea’:1,’lds’:2,’les’:3,’lfs’:4,’lgs’:5,’les’:6}
	FTI={‘lahf’:1,’sahf’:2,’push’:3,’popf’:4,’pushd’:5,’popd’:6}　　
	ADO={‘add’:1,’adc’:2,’inc’:3,’aaa’:4,’daa’:5,’sub’:6,’sbb’:7,’dec’:8,’nec’:9,’cmp’:10,’aas’:11,’das’:12,’mul’:13,’imul’:14,’aam’:15,’div’:16,’idiv’:17,’aad’:18,’cbw’:19,’cwd’:20,’cwde’:21,’cdq’:22,’c’:23,’r’:24,’rsc’:25,’mla‘：13，’smull’:14,’umull’:15,’umlal’:16,’addu’:1,’subu’:6,’addi’:1,’addiu’:2}　
	LDO={‘and’:1,’or’:2,’xor’:3,’not’:4,’test’:5,’shl’:6,’sal’:7,’shr’:8,’sar’:9,’rol’:10,’ror’:11,’rcl’:12,’rcr’:13,’orr’:2,’eor’:3,’bic’:16,’andi’:1,’ori’:2,’xori’:3}
	SI={‘movs’:1,’cmps’:2,’scas’:3,’lods’:4,’stos’:5,’rep’:6,’repe’:7,’repen’:8,’repc’:9,’repnc’:10}
	UBI={‘jump’:1,’call’:2,’ret’:3,’j’:1,’cal’:2}　
	CBI={‘ja’:1,’jnbe’:1,’jae’:2,’jnb’:10,’jb’:3,’jbe’:4,’jg’:5,’jge’:6,’jl’:7,’jle’:8,’je’:9,’jne’:11,’jc’:12,’jnc’:13,’jno’:14,’jnp’:15,’jns’:16,’jo’:17,’jp’:18,’js’:19,’slt’:20,’sltu’:21,’sll’:13,’srl’:14,’sra’:15,’sllv’:16,’srlv’:17,’jr’:18,’beq’:1,’bne’:2,’slti’:3.’sltiu’:4}    
	LCI={‘loop’:1,’loope’:2,’loopne’:3,’jcxz’:4,’jecxz’:5}
	II={‘int’:1,’into’:2,’iret’:3}
	PCI={‘hlt’:1,’wait’:2,’esc’:3,’lock’:4,’nop’:5,’stc’:6,’clc’:7,’cmc’:8,’std’:9,’cld’:10,’sti’:11,’cli’:12,’msr’:1,’mrs’:2,’lw’:1,’sw’:2}
	PI={‘dw’:1,’proc’:2,’ends’:3,’segment’:4,’assume’:5,’ends’:6,’end’:7}
	
	arm_L1={}
	blocks=[(v.startEA, v.endEA) for v in FlowChart(func)]
	for bl in blocks:
		start = bl[0]
		end = bl[1]
		invoke_num = 0
		inst_addr = start
		while inst_addr < end:
			opcode = GetMnem(inst_addr)
			if opcode in GDTI:
				opcodenum=GDTI.getvalue(opcode)
				sequence.append(1)
			if opcode in IOPTI:
				opcodenum=IOPTI.getvalue(opcode)
				sequence.append(2)
			if opcode in DATI:
				opcodenum=DATI.getvalue(opcode)
				sequence.append(3)
			if opcode in PI:
				opcodenum=PI.getvalue(opcode)
				sequence.append(4)
			if opcode in FTI:
				opcodenum=FTI.getvalue(opcode)
				sequence.append(5)
			if opcode in ADO:
				opcodenum=ADO.getvalue(opcode)
				sequence.append(6)
			if opcode in LDO:
				opcodenum=LDO.getvalue(opcode)
				sequence.append(7)
			if opcode in SI:
				opcodenum=SI.getvalue(opcode)
				sequence.append(8)
			if opcode in UBI:
				opcodenum=UBI.getvalue(opcode)
				sequence.append(9)
			if opcode in CBI:
				opcodenum=CBI.getvalue(opcode)
				sequence.append(10)
			if opcode in LCI:
				opcodenum=LCI.getvalue(opcode)
				sequence.append(11)
			if opcode in II:
				opcodenum=II.getvalue(opcode)
				sequence.append(12)
			if opcode in PCI:
				opcodenum=PCI.getvalue(opcode)
				sequence.append(13)
			sequence.append(opcodenum)

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

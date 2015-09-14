import codecs, sys, getopt

debug_m = False;


#
#            0   1 
#            a   b 
#    1  q0  +2  +1 
#    2  q1  +1  +3
#    3  q2  -4  +3
#    4  q3  -4  -1
#
# A linha representa o estado inicial, a coluna o simbolo 
# e o valor a direcao (+ = R, - = L)
# O exemplo é o mesmo da entrada exemplo

def Log(message, name = ""):
	if name is "":
		name = "Unnamed Log #" + str(Log.TotalUnnamed)
		Log.TotalUnnamed += 1
	print("*" * (len(name) + 2))
	print("*" + name + "*")
	print("*" * (len(name) + 2) + "\n")
	print(message)
	print("\n------------------------------------------")
Log.TotalUnnamed = 0

def DebugLog(message, name = ""):
	if DebugLog.active is True:
		Log(message, name)
DebugLog.active = False

# Esse metodo serve para buscar os # no arquivo de entrada
def GetElementsBetweenMarker(marker, text):
	retList = []
	endPos = 0
	while True:
		startPos = text.find(marker, endPos + 1)
		endPos = text.find(marker, startPos + 1)
		if(startPos < 0 or endPos < 0): return retList
		DebugLog("Start: " + str(startPos) + " End: " + str(endPos) + " = " + text[startPos + 1 :endPos])
		retList.append(text[startPos + 1:endPos])

# Esse metodo serve para montar a matriz como descrita inicialmente
def GetStates(toStatesText, directionsText, alphabet, states):
	retMatrix = [[0 for x in range(len(alphabet))] for y in range(len(states))]
	toStatesLines = [x for x in toStatesText.split("\n") if x != '']
	directionsLines = [x for x in directionsText.split("\n") if x != '']
	for j in range(len(states) - 1):
		toStatesList = toStatesLines[j].split()
		directionsList = directionsLines[j].split()
		for i in range(len(alphabet)):
			mult = (-1 if directionsList[i] is "L" else +1)
			retMatrix[j + 1][i] = mult * NameToNumber(states, toStatesList[i])
 			
	return retMatrix

# Essa funcao pega o indice do estado passado
def NameToNumber(states, state):
	return states.index(state)

def NumberToName(states, number):
	return states[number]

def SymbolToNumber(alphabet, symbol):
	return alphabet.index(symbol)

def Sign(number):
	return -1 if number < 0 else +1

def IsValid(inputString, statesMatrix, alphabet, finalStates, states):
	if inputString == []:
		return True, "Cadeia aceita. Motivo: Cadeia vazia"

	for s in inputString:
		if s not in alphabet:
			return False, "Cadeia nao aceita. Motivo: Simbolo '"+ s + "' nao pertencente ao alfabeto"
			

	printTape = [" " for x in range(len(inputString))]

	transitionHistory = []
	currentPosition = 0
	currentState = 1

	# Saber qual o numero equivalente aquele simbolo do alfabeto
	while True:	
		# Logica para printar a logica da fita
		tapeLog = ""
		printTape[currentPosition] = "^"
		tapeLog += "CurrentState: "  + str(currentState) + "\n"
		tapeLog += str(inputString) + "\n"
		tapeLog += str(printTape) + "\n"
		DebugLog(tapeLog, "Tape Status")
		printTape[currentPosition] = " "

		# Logica para armazenar os estados ja passados
		transitionHistory.append((currentPosition, currentState))

		currentSymbolNum = SymbolToNumber(alphabet, inputString[currentPosition])
		
		#Proximos estado e posicao
		transition = statesMatrix[currentState][currentSymbolNum]
		currentState = abs(transition)
		currentPosition += Sign(transition)

		# Condicoes de parada
		if currentPosition > len(inputString) - 1 or currentPosition < 0: 
			DebugLog(NumberToName(states, currentState), "Estado Final")
			DebugLog(currentPosition, "Posicao Final")
			if currentState not in finalStates:
				return False, "Cadeia nao aceita. Motivo: Estado final nao valido"
			return True, "Cadeia aceita. Motivo: Cadeia valida"


		if (currentPosition, currentState) in transitionHistory:
			DebugLog(NumberToName(states, currentState), "Estado Final")
			DebugLog(currentPosition, "Posicao Final")
			return False, "Cadeia nao aceita. Motivo: Loop Infinito"

def afd2(arg):
	TotalUnnamed = 0
	# Leitura inicial do arquivo
	semiparsed = []
	with open(arg, "r") as f:
		textStr = f.read()
		semiparsed = GetElementsBetweenMarker("#", textStr)

	# Leitura do alfabeto
	alphabet = semiparsed[0].split()
	DebugLog(str(alphabet), "Alphabet")

	# Leitura dos estados
	states = semiparsed[1].split()
	# Inserimos um estado proibido inicial para todo estado ter valor
	# diferente de 0 (para satisfazer o explicado inicialmente)
	states.insert(0, "ESTADO PROIBIDO")
	DebugLog(str(states), "States")

 	# Leitura dos estados finais
	finalStates = [NameToNumber(states, x) for x in semiparsed[2].split()]
	DebugLog(str(finalStates), "Final States")

	# Leitura das transicoes de estados
	strToStates = semiparsed[3]
	strDirections = semiparsed[4]
	statesMatrix = GetStates(strToStates, strDirections, alphabet, states)
	logMatrix = ""
	for l in statesMatrix:
		logMatrix += str(l)
		logMatrix += "\n"
	DebugLog(logMatrix, "Transitions")

	inputString = [x for x in semiparsed[5].strip()]
	DebugLog(str(inputString),"Input String")

	b, message = IsValid(inputString, statesMatrix, alphabet, finalStates, states)

	Log(message, "Aceitacao:")


def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hd:b:", ["help"])
	except Exception as e:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt == "-d":
			DebugLog.active = True
			afd2(arg)
		elif opt == "-b":
			afd2(arg)      


usageString = """usage: 2afd [--help] [-h] [-d <path>] [-b <path>]

The commands are:
-d \t\t Debug mode
-b \t\t Normal mode
<path> \t\t Input File
-h, --help \t Show available commands
"""


def usage():
    print(usageString)

if __name__ == '__main__':
    main(sys.argv[1:])

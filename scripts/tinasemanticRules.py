
# -*- coding: utf-8 -*-

import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry
import sys
sys.path.insert(0,'/mit/6.863/spring2018/cgw/teams/pistachio-conkers/final_project/scratchNLP/scripts')
from text2num import text2int

####################################################################

def translate(data):
    pass

def translateModifier(data):
    pass

####################################################################

identity = lambda x: x

sem = SemanticRuleSet()
global_variables = {}
global_lists = {}

####################################################################
# Speech Actions
def processSentence(data):
    if len(data) > 0:
        data = [thing for thing in data if thing != None]
        return {'scripts': data, 'variables': global_variables, 'lists': global_lists}

def singleCommand(commandName, value):
    print("commandName, value", commandName, value)
    return [commandName, value]

def singleCommandNoValue(commandName):
    return [commandName]

def ifCommand(if_cond, if_body):
    return ["doIf", if_cond, [if_body]]

def ifElseCommand(if_cond, if_body, else_body):
    return ["doIfElse", if_cond, [if_body],[else_body]]

def repeat(num_times, repeat_body):
    return ["doRepeat", int(num_times), [repeat_body]]
def until(until_condition, repeat_body):
    return ["doUntil", until_condition, [repeat_body]]
def doForever(forever_body):
    return ["doForever", [forever_body]]
def deleteClone():
    return ["deleteClone"]

def wait(wait_time):
    return ["wait:elapsed:from:", wait_time]
def waitUntil(until_condition):
    return ["doWaitUntil", until_condition]

def getNumber(unk):
	try:
		num = int(unk)
	except:
		num = text2int(unk)
	return num

def setVariable(var_name, value):
    global_variables[var_name] = value
    return ["setVar:to:",var_name, value]

def deleteVariable(variable_name):
    del global_variables[variable_name]

def createVariable(variable_list):
    for var in variable_list:
        global_variables[var] = 0
        # TODO: somehow prevent returning the variable name in response of processSentence.
        return None

def createSingleList(name):
    global_lists[name] = []

def createClone():
    return ["createCloneOf:", "myself"]

def itemInList(unk, name):
    return ["list:contains:", name, unk]

def resetTimer():
    return ["timerReset"]

# OPERATORS
def add(n1, n2):
    return ['+', n1, n2]

def subtract(n1, n2):
    return ['-', n1, n2]

def getProduct(num, num2):
    return ["*", num, num2]

def getQuotient(num, num2):
    return ["/", num, num2]

def getValue(var):
    return ["readVariable", var]

def getRandomNumberBetween(unk1, unk2):
    return ['randomFrom:to:', unk1, unk2]

def lessThan(a,b):
    return ["<", a, b]

def greaterThan(a,b):
    return [">", a, b]

def equalTo(a,b):
    return ["=", a, b]

def GEQ(a,b):
    return ["|", [">", a, b], ["=", a, b]]

def LEQ(a,b):
    return ["|", ["<", a, b], ["=", a, b]]

def logicOr(b1, b2):
    return ["|", b1, b2]

def logicAnd(b1, b2):
    return ["&", b1, b2]

def waitTillTimer(x):
    return ["doWaitUntil", x]

def changeVarBy(var_name, unk, opt_negate=False):
    if opt_negate:
        return ["changeVar:by:", var_name, ["*", unk, -1]]
    return ["changeVar:by:",var_name, unk]

def changeVarbyVar(var1, var2,opt_negate=False):
    if opt_negate:
        return ["setVar:to:", var1, ["*", getValue(var2), -1]]
    return ["changeVar:by:", var1, getValue(var2)]

def ynQuestion(data):
    if sem.learned.yesno_query(data):
        return "Yes."
    else:
        return "No."

def whenGreenFlag():
    return ["whenGreenFlag"]

def whenKeyClicked(name):
    return ["whenKeyPressed", name]

def whenClicked():
    return ["whenClicked"]

def whenBackSwitch(name):
    return ["whenSceneStarts", name]

def whenReceive(message):
    return ["whenIReceive", message]

def broadcastMessage(name):
    return ["broadcast:", name]

def broadCastMessageWait(name):
    return ["doBroadcastAndWait:", name]

def not_identity(x):
    return ["not", x]

def SimpleEvent(e, a):
    # flatten the action list
    return [e] + a

def whQuestion(data):
    results = sem.learned.wh_query(data)
    if len(results) == 0:
        return "I don't know."
    else:
        return list(results)[0]

def npOnlyHuhResponse(data):
    return "What about %s?"%(pretty_print_entry(data))

# List commands
def getItem(ind, list_name):
    return ['getLine:ofList:', ind, list_name]

def wordMap(order_adverb):
    adverbToNumMap = {
        'firstly': 1,
        'first': 1,
        'second': 2,
        'secondly': 2,
        'third': 3,
        'thirdly': 3,
        'fourth': 4,
        'fourthly': 4,
        'fifth': 5,
        'fifthly': 5,
        'sixth': 6,
        'sixthly': 6,
        'seventh': 7}
    return adverbToNumMap[order_adverb]

def addToList(list_name, item):
    return [['append:toList:', item, list_name]]

def deleteItemFromList(list_name, ind):
    return [['deleteLine:ofList:', ind, list_name]]

def setItemInList(ind, list_name, item):
    return [['setLine:ofList:to:', ind, list_name, item]]

# Loop commands
def repeat_action_list(action_list, duration):
    print 'action_list'
    print action_list
    print 'duration'
    print duration
    if duration == 'forever':
        return ['doForever', action_list]
    else:
        return ['doRepeat', duration, action_list]

def get_duration(duration):
        return duration

# Sequential commands
def appendToProgram(action_list):
    program.append(action_list)
    return action_list


####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))

# All Command
sem.add_rule("S -> AL", identity)
#testing specific non terminals, will delete later
sem.add_rule("S -> BP", identity)
sem.add_rule("AL -> AP", lambda p: [p])
sem.add_rule("AL -> AP AL", lambda p, l: [p]+l)
sem.add_rule("AL -> AP And AL", lambda p,an, l: [p]+l)

sem.add_rule("AP -> SoundCommand", identity)
sem.add_rule("AP -> CreateCommand", identity)
sem.add_rule("AP -> DataCommand", identity)
sem.add_rule("AP -> EventHandler", identity)
sem.add_rule("AP -> OrderedCommand", identity)
sem.add_rule("AP -> SequentialCommand", identity)
sem.add_rule("AP -> ConditionalCommand", identity)
sem.add_rule("AP -> LoopCommand", identity)
sem.add_rule("AP -> TimerCommand", identity)
sem.add_rule("AP -> BroadcastCommand", identity)
sem.add_rule("AP -> ControlCommand", identity)

sem.add_rule("OrderedCommand -> OrderAdverb AL", lambda num, al: al)

# SequentialCommand
sem.add_rule("SequentialCommand -> SequenceAdverb AL", lambda seq_adv, action_list: appendToProgram(action_list))

# Create Command
sem.add_rule("CreateCommand -> Make Det Clone Of Myself", lambda m, det, c,o, my: createClone())

sem.add_rule("CreateCommand -> Make VARIABLE_LIST", lambda make, vl: createVariable(vl))


#sem.add_rule("CreateCommand -> Make List LIST_NAME For Det Single Sprite", lambda make, lis, name, fr, a, single, sprite: createSingleList(name))
sem.add_rule("CreateCommand -> Make List LIST_NAME", lambda make,l, name: createSingleList(name))
#sem.add_rule("CreateCommand -> Make List LIST_NAME For All Det Sprites", lambda make, lis, name, fr, al, the, sprites: createAllList(name))

sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME", lambda vl: [vl])
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME And VARIABLE_LIST", lambda vn,a, vl: [vn]+vl)


sem.add_rule("VARIABLE_NAME -> Variable VARIABLE_NAME", lambda l, name: name)
sem.add_rule("Variable -> Det Variable", lambda det, var: var)
sem.add_rule("Variable -> Variable Called", lambda v, c: v)
sem.add_rule("List -> Det List", lambda det, liss: liss)
sem.add_rule("List -> List Called", lambda liss, c: liss)

sem.add_rule("KEY_NAME -> Keyname KEY_NAME", lambda k, n: n)
sem.add_rule("Keyname -> Key", lambda k: None)
sem.add_rule("Keyname -> Det Key", lambda d, k: None)
sem.add_rule("Keyname -> Det Key Called", lambda d, k, c: None)
sem.add_rule("Keyname -> Key Called", lambda k, c: None)
sem.add_rule("KEY_NAME -> Det KEY_NAME", lambda det, name: name)
sem.add_rule("KEY_NAME -> KEY_NAME Key", lambda name, key: name)


sem.add_rule("ITEM -> NP", lambda i:i)
sem.add_rule("ITEM -> MESSAGE_NAME", lambda name: name)
sem.add_rule("ITEM -> Unk", lambda name: name)
sem.add_rule("ITEM -> VARIABLE_NAME", lambda name: name)
sem.add_rule("ITEM -> DATA_REPORTER", identity)

# Duration
sem.add_rule("Duration -> Unk 'times'", lambda np, times: get_duration(np))

# Sound Command
# Use the halting version f the play sound block
sem.add_rule("SoundCommand -> Play Det NAME_OF_SOUND Sound", lambda play, the, name, sound: singleCommand("doPlaySoundAndWait", name))

sem.add_rule("SoundCommand -> Set Volume To Unk", lambda sett, volume, too, unk: singleCommand("setVolumeTo:", unk))

sem.add_rule("SoundCommand -> Set Volume To Unk Percent", lambda sett, volume, too, unk, percent: singleCommand("setVolumeTo:", unk))

sem.add_rule("SoundCommand -> Change Volume By Unk", lambda change, volume, by, Unk: singleCommand("changeVolumeBy:", Unk))

sem.add_rule("SoundCommand -> Change Pitch Effect By Unk", lambda change, pitch, effect, by, Unk: singleCommand("changeTempoBy:", Unk))

sem.add_rule("SoundCommand -> Stop All Sounds", lambda stop, all, sounds: singleCommandNoValue("stopAllSounds"))

sem.add_rule("SoundCommand -> Stop", lambda stop: singleCommandNoValue("stopAllSounds"))

sem.add_rule("SoundCommand -> Softer", lambda softer: singleCommand("changeVolumeBy:", -10))

sem.add_rule("SoundCommand -> Louder", lambda louder: singleCommand("changeVolumeBy:", 10))

sem.add_rule("SoundCommand -> Slower", lambda slower: singleCommand("changeTempoBy:", -10))

sem.add_rule("SoundCommand -> Faster", lambda faster: singleCommand("changeTempoBy:", 10))


## Data Command

# todo: fix
sem.add_rule("DataCommand -> Delete VARIABLE_NAME", lambda delete, var_name: deleteVariable(var_name))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To BP", lambda s, var_name, to, bp: setVariable(var_name, bp))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To NP", lambda s, var_name, to, np: setVariable(var_name, np))
sem.add_rule("DataCommand -> Set VARIABLE_NAME To ITEM", lambda s, var_name, to, item: setVariable(var_name, item))
sem.add_rule("DataCommand -> Add NP To VARIABLE_NAME", lambda a, num, t, var_name:
changeVarBy(var_name, num))
sem.add_rule("DataCommand -> Increment VARIABLE_NAME By NP", lambda i, var_name, b, num: changeVarBy(var_name, num))
sem.add_rule("DataCommand -> Add VARIABLE_NAME To VARIABLE_NAME", lambda i, var1, b, var2: changeVarByVar(var2, getValue(var1)))
sem.add_rule("DataCommand -> Subtract NP From VARIABLE_NAME", lambda a, np, t, var_name: changeVarBy(var_name, np, 'negate'))
sem.add_rule("DataCommand -> Decrement VARIABLE_NAME By NP", lambda a, var_name, t, np: changeVarBy(var_name, np, 'negate'))
sem.add_rule("DataCommand -> Subtract VARIABLE_NAME From VARIABLE_NAME", lambda a, var1, t, var2: changeVarByVar(getValue(var2), var1, 'negate'))
sem.add_rule("DataCommand -> Multiply VARIABLE_NAME By NP", lambda m, var_name, b, np: setVariable(var_name, getProduct(getValue(var_name), np)))
sem.add_rule("DataCommand -> Multiply VARIABLE_NAME By VARIABLE_NAME", lambda m, var1, b, var2: setVariable(var1, getProduct(getValue(var1), getValue(var2))))
sem.add_rule("DataCommand -> Divide VARIABLE_NAME By NP", lambda d, var_name, b, np: setVariable(var_name, getQuotient(getValue(var_name), np)))
sem.add_rule("DataCommand -> Divide VARIABLE_NAME By VARIABLE_NAME", lambda d, var1, b, var2: setVariable(var1, getQuotient(getValue(var1), getValue(var2))))


# todo: fix commands working w/ lists
sem.add_rule("DataCommand -> Add ITEM To LIST_NAME", lambda a, item, t, list_name: addToList(list_name, item))
sem.add_rule("DataCommand -> Delete Ele NP Of LIST_NAME", lambda d, el, ind,o, list_name: deleteItemFromList(ind, list_name))
sem.add_rule("DataCommand -> Replace Ele NP Of LIST_NAME With ITEM", lambda r, e, ind, o,list_name,w, item: setItemInList(ind, list_name, item))
sem.add_rule("DataCommand -> Set Ele NP Of LIST_NAME To ITEM", lambda s, e, ind, o, list_name, t,
item: setItemInList(ind, list_name, item))
# Data Reporter
sem.add_rule("DataReporter -> The OrderAdverb Item In LIST_NAME", lambda t, order_adverb, i, inn, list_name: getItem(wordMap(order_adverb), list_name))

# Number Phrase
sem.add_rule("NP -> Unk", lambda unk: getNumber(unk))

sem.add_rule("NP -> NPP", identity)

sem.add_rule("NP -> Det NPP", lambda det, npp: npp)

sem.add_rule("NP -> VARIABLE_NAME", lambda v: getValue(v))

sem.add_rule("NP -> NP Plus NP", lambda unk1, plus, unk2: add(unk1, unk2))
sem.add_rule("NP -> NP Added To NP", lambda unk1, added, to, unk2: add(unk1, unk2))
sem.add_rule("NPP -> Sum Of NP And NP", lambda s, of, unk1, a, unk2: add(unk1, unk2))

sem.add_rule("NP -> NP Minus NP", lambda unk1, minus, unk2: subtract(unk1, unk2))
sem.add_rule("NP -> NP Subtracted By NP", lambda unk1, subtracted, by, unk2: subtract(unk1,unk2))

sem.add_rule("NP -> NP Subtracted From NP", lambda unk1, subtracted, by, unk2: subtract(unk2,unk1))

sem.add_rule("NP -> NP Times NP", lambda unk1, times, unk2: getProduct(unk1,unk2))
sem.add_rule("NP -> NP Multiplied By NP", lambda unk1, multiplied, by, unk2: getProduct(unk1,unk2))
sem.add_rule("NPP -> Product Of NP And NP", lambda product, of, unk1, a, unk2: getProduct(unk1,unk2))

sem.add_rule("NP -> NP Divided By NP", lambda unk1, divided, by, unk2: getQuotient(unk1,unk2))
sem.add_rule("NPP -> Random Number Between NP And NP", lambda r, n, b, unk1, a, unk2: getRandomNumberBetween(unk1, unk2))
sem.add_rule("NP -> Negative NP", lambda n, np: getProduct(-1,np))




sem.add_rule("EVENT -> When Det Green Flag Is Clicked", lambda w, t, g, f, i, c: whenGreenFlag())

sem.add_rule("EVENT -> When Det Program Starts", lambda w, t, p, s: whenGreenFlag())

sem.add_rule("EVENT -> When Green Flag Is Clicked", lambda w, g, f, i, c: whenGreenFlag())

sem.add_rule("EVENT -> When Program Starts", lambda w, p, s: whenGreenFlag())

sem.add_rule("EVENT -> When KEY_NAME Is Clicked", lambda w, name, iss, pressed: whenKeyClicked(name))

sem.add_rule("EVENT -> When Det Sprite Is Clicked", lambda w, t, s, iss, cli: whenClicked())

sem.add_rule("EVENT -> When Backdrop Switches To BACKDROP_NAME", lambda w, b, s, t, name: whenBackSwitch(name))

sem.add_rule("EVENT -> When Backdrop Switches To Det BACKDROP_NAME", lambda w, b, s, t, th, name: whenBackSwitch(name))

sem.add_rule("EVENT -> When I Receive MESSAGE_NAME", lambda w, i, r, message: whenReceive(message))

sem.add_rule("Timer -> Det Timer", lambda d, tim: tim)


sem.add_rule("EVENT -> When Timer CBP NP", lambda w, t, c, n: waitTillTimer(c([t], n)))


sem.add_rule("CBP -> Equal To", lambda e, t: lambda a, b: equalTo(a,b))
sem.add_rule("CBP -> Greater Than", lambda g, t: lambda a, b: greaterThan(a, b))
sem.add_rule("CBP -> Less Than", lambda l, t: lambda a, b: lessThan(a, b))
sem.add_rule("CBP -> Greater Than Or Equal To", lambda g, t, o, e, too: lambda a, b: GEQ(a, b))
sem.add_rule("CBP -> Less Than Or Equal To", lambda l, t, o, e, too: lambda a, b: LEQ(a, b))

sem.add_rule("CBP -> LMOD CBP", lambda m, c: lambda a, b: m(c(a, b)))

sem.add_rule("LMOD -> POS", lambda pos: lambda x: x)
sem.add_rule("LMOD -> NEG", lambda neg: lambda x: not_identity(x))



sem.add_rule("SimpleEventHandler -> EVENT AL ", lambda e, a: SimpleEvent(e, a))
sem.add_rule("EventHandler ->  SimpleEventHandler Thats It", lambda e, thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Thats It", lambda e, a, t, s, ti, thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler Too Thats It", lambda e, t,thats, it: e)
sem.add_rule("EventHandler -> SimpleEventHandler At Det Same Time Too Thats It", lambda e, a, t, s, ti, to, thats, it: e)



## TimerCommand
sem.add_rule("TimerCommand -> 'reset' Tim", lambda r, t: resetTimer())
sem.add_lexicon_rule("Ele",['element', 'item'],identity)

## Boolean Phrases
sem.add_rule("BP -> Item Unk In LIST_NAME", lambda i, unk, inn, name:itemInList(unk, name))
sem.add_rule("BP -> Item Unk LMOD In LIST_NAME", lambda i, unk, mod, inn, name: mod(itemInList(unk, name)))
sem.add_rule("BP -> VARIABLE_NAME CBP Unk", lambda var, cbp, unk: cbp(getValue(var), unk))

sem.add_rule("BP -> Unk CBP Unk", lambda unk1, cbp, unk2: cbp(unk1, unk2))
sem.add_rule("BP -> Timer CBP Unk", lambda tim, comp, Unk: comp(tim, Unk))

sem.add_rule("BP -> VARIABLE_NAME CBP VARIABLE_NAME", lambda var1, cbp, var2: cbp(getValue(var1), getValue(var2)))

sem.add_rule("BP -> LIST_NAME Contains ITEM", lambda name, con, it: itemInList(it, name))

sem.add_rule("BP -> Boolean" , identity)
sem.add_rule("Boolean -> 'true'" , lambda t: 1) # Scenario?
sem.add_rule("Boolean -> 'false'" , lambda t: 0) # Scenario?
sem.add_rule("Boolean -> LMOD 'true' ", lambda l, t: l(1))
sem.add_rule("Boolean -> LMOD 'false'" , lambda l, t: l(0))

sem.add_rule("BP -> BP And BP", lambda b1,andd, b2: logicAnd(b1, b2))
sem.add_rule("BP -> BP Or BP", lambda b1, orr, b2: logicOr(b1, b2))


## Broadcast Commands
sem.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME", lambda broadcast, name: broadcastMessage(name))
sem.add_rule("BroadcastCommand -> Broadcast MESSAGE_NAME And Wait", lambda b, name, a, w: broadCastMessageWait(name))
sem.add_rule("MESSAGE_NAME -> Det MESSAGE_NAME", lambda d, name: name)
sem.add_rule("MESSAGE_NAME -> Message MESSAGE_NAME", lambda d, name: name)
sem.add_rule("Message -> New Message", lambda d, name: name)
sem.add_rule("Message -> Det Message", lambda d, name: name)
sem.add_rule("Message -> Message Called", lambda d, name: name)



# Conditional Command
sem.add_rule("ConditionalCommand -> If BP Then AL Thats It", lambda i, bp, then, al, thats, it: ifCommand(bp,al))
sem.add_rule("ConditionalCommand -> If BP Then AL Thats It Else AL Thats It", lambda i, bp, then, al1, thats1, it1, ow, al2, thats2, it2: ifElseCommand(bp,al1,al2))

# Control Command

sem.add_rule("ControlCommand -> Wait Unk Seconds", lambda waitt, unk, seconds: wait(unk))

sem.add_rule("ControlCommand -> Wait Until BP", lambda wait, until, bp: waitUntil(bp))

sem.add_rule("ControlCommand -> Repeat AL Until BP", lambda repeat, al, untill, bp: until(bp, al))

sem.add_rule("ControlCommand -> Repeat AL Forever", lambda repeat, al, forever: doForever(al))

sem.add_rule("ControlCommand -> Repeat AL Unk Times", lambda repeatt, al, unk, times: repeat(unk, al))

sem.add_rule("ControlCommand -> Delete Det Clone", lambda delete, this, clone: deleteClone())



#LoopCommand
sem.add_rule("LoopCommand -> Repeat LoopCommandP", lambda r, lcp: lcp)
sem.add_rule("LoopCommand -> LoopCommandP", identity)
sem.add_rule("LoopCommand -> AL Should Be Repeated Duration", lambda action_list, t,s,b,r, duration: repeat_action_list(action_list, duration))
sem.add_rule("LoopCommandP -> AP Duration", lambda ap, duration: repeat_action_list([ap], duration))
sem.add_rule("LoopCommandP -> The Following Duration AL Thats It", lambda t, f, duration, action_list, tt, i: repeat_action_list(action_list, duration))
sem.add_rule("LoopCommandP -> The Following Steps Duration AL Thats It", lambda t, f, s, duration, action_list, tt, i: repeat_action_list(action_list, duration))


#####################################################################
## Lexicon

# Data Command Keywords
sem.add_lexicon_rule("Add", ["add"], identity)
sem.add_lexicon_rule("Increment", ["increment"], identity)
sem.add_lexicon_rule("Decrement", ["decrement"], identity)
sem.add_lexicon_rule("Subtract", ["subtract"], identity)
sem.add_lexicon_rule("From", ["from"], identity)
sem.add_lexicon_rule("With", ["with"], identity)


# Loop Command Keywords
sem.add_lexicon_rule("That", ["that"], identity)
sem.add_lexicon_rule("Be", ["be"], identity)
sem.add_lexicon_rule("Repeated", ["repeated"], identity)
sem.add_lexicon_rule("The", ["the"], identity)
sem.add_lexicon_rule("That", ["that"], identity)
sem.add_lexicon_rule("This", ["this"], identity)

# Names
sem.add_lexicon_rule("NAME_OF_SOUND",
                     ['meow'],
                     # TODO: the semantic rule for NAME_OF_SOUND could involve
                     # searching
                     lambda name: name)
sem.add_lexicon_rule("I", ["i"], identity)
sem.add_lexicon_rule("Sprite", ["sprite"], identity)

# Command Keywords
sem.add_lexicon_rule("Play", ['play'], identity)
sem.add_lexicon_rule("Set", ['set'], identity)
sem.add_lexicon_rule("Replace", ['replace'], identity)
sem.add_lexicon_rule("Change", ['change'], identity)
sem.add_lexicon_rule("Stop", ['stop', 'terminate'], identity)
sem.add_lexicon_rule("Wait", ['wait'], identity)
sem.add_lexicon_rule("Repeat", ['repeat', 'do'], identity)
sem.add_lexicon_rule("Repeated", ['repeated', 'done'], identity)
sem.add_lexicon_rule("Delete", ['delete'], identity)

# Conditional Command Keywords
sem.add_lexicon_rule("If", ['if'], identity)
sem.add_lexicon_rule("Then", ['then'], identity)
sem.add_lexicon_rule("Else", ['else', 'otherwise'], identity)
sem.add_lexicon_rule("Thats", ["thats"], identity)
sem.add_lexicon_rule("It", ["it"], identity)
sem.add_lexicon_rule("Until", ['until', 'till'], identity)

# Nouns
sem.add_lexicon_rule("Sounds", ['sounds'], identity)
sem.add_lexicon_rule("Sound", ['sound'], identity)
sem.add_lexicon_rule("Volume", ['volume'], identity)
sem.add_lexicon_rule("Pitch", ['pitch'], identity)
sem.add_lexicon_rule("Effect", ['effect'], identity)
sem.add_lexicon_rule("Percent", ['percent'], identity)
sem.add_lexicon_rule("Seconds", ['seconds'], identity)
sem.add_lexicon_rule("Times", ['times'], identity)
sem.add_lexicon_rule("Clone", ['clone'], identity)
sem.add_lexicon_rule("Steps", ['steps'], identity)

#Prep
sem.add_lexicon_rule("To",['to'],identity)
sem.add_lexicon_rule("By",['by'],identity)

#Comparison
sem.add_lexicon_rule("Softer",['softer', 'quieter'],identity)
sem.add_lexicon_rule("Louder",['louder'],identity)
sem.add_lexicon_rule("Slower",['slower'],identity)
sem.add_lexicon_rule("Faster",['faster'],identity)

#Adj
sem.add_lexicon_rule("All",['all'],identity)
sem.add_lexicon_rule("Following",['following'],identity)

#Adv
sem.add_lexicon_rule("Forever",['forever'],identity)

# # Determiners
sem.add_lexicon_rule("Det",
                      ['the', 'this'],
                      lambda word: lambda: None)

sem.add_lexicon_rule("Det",
                      ['a', 'an'],
                      lambda word: lambda: None)



sem.add_lexicon_rule("OrderAdverb",
                       ['secondly', 'fourthly', 'fifthly', 'seventh', 'second', 'fifth', 'sixthly', 'third', 'thirdly', 'fourth', 'sixth', 'firstly', 'first'],
                       lambda word: wordMap(word))

# handle sequencing adverbs
sem.add_lexicon_rule("SequenceAdverb",
                       ['then', 'after', 'finally'],
                       identity)

sem.add_lexicon_rule("Duration",
                       ['forever'],
                       lambda word: Dur(-1))

sem.add_lexicon_rule("Unk",
                       ['0','1','2','3','4','5','6','7','8','9'],
                       identity)

## EVENT
sem.add_lexicon_rule("When", ["when"], identity)
sem.add_lexicon_rule("Green", ["green"], identity)
sem.add_lexicon_rule("Flag", ["flag"], identity)
sem.add_lexicon_rule("Is", ["is"], identity)
sem.add_lexicon_rule("Clicked", ["pressed", "clicked"], identity)
sem.add_lexicon_rule("Program", ["program"], identity)
sem.add_lexicon_rule("Starts", ["starts"], identity)
sem.add_lexicon_rule("Backdrop", ["backdrop"], identity)
sem.add_lexicon_rule("Switches", ["switches"], identity)
sem.add_lexicon_rule("Receive", ["receive"], identity)
sem.add_lexicon_rule("At", ["at"], identity)
sem.add_lexicon_rule("Same", ["same"], identity)
sem.add_lexicon_rule("Time", ["time"], identity)
sem.add_lexicon_rule("Too", ["too", "simultaneously"], identity)
sem.add_lexicon_rule("Should", ['should'], identity)

## Timer
sem.add_lexicon_rule("Timer", ["timer"], identity)
sem.add_lexicon_rule("Reset", ["reset"], identity)

## Compare
sem.add_lexicon_rule("Equal", ["equal"], identity)
sem.add_lexicon_rule("Greater", ["greater"], identity)
sem.add_lexicon_rule("Less", ["less"], identity)
sem.add_lexicon_rule("Than", ["than"], identity)


## Logic
sem.add_lexicon_rule("Or", ["or"], identity)
sem.add_lexicon_rule("And", ["and"], identity)
sem.add_lexicon_rule("NEG", ["not"], identity)
sem.add_lexicon_rule("NEG", ["isn't"], identity)# not working
sem.add_lexicon_rule("POS", ["is"], identity)
sem.add_rule("NEG -> Is NEG", lambda x, y: y)

sem.add_lexicon_rule("In", ["in"], identity)
sem.add_lexicon_rule("List", ["list"], identity)
sem.add_lexicon_rule("Item",['item'],identity)
sem.add_lexicon_rule("Contains",['contains', 'has'],identity)
sem.add_lexicon_rule("Variable",['variable'],identity)
sem.add_lexicon_rule("Called",['called', 'named'],identity)
sem.add_lexicon_rule("Broadcast",['broadcast'],identity)
sem.add_lexicon_rule("New",['new'],identity)
sem.add_lexicon_rule("Message",['message'],identity)
sem.add_lexicon_rule("Key",['key', 'button'],identity)

sem.add_lexicon_rule("Make",['make', 'create'],identity)
sem.add_lexicon_rule("For",['for'],identity)
sem.add_lexicon_rule("Single",['single'],identity)
sem.add_lexicon_rule("Sprites",['sprites'],identity)
sem.add_lexicon_rule("Of",['of'],identity)
sem.add_lexicon_rule("Myself",['myself'],identity)
sem.add_lexicon_rule("Ele",['element'],identity)

## Operators
sem.add_lexicon_rule("Divided",['divided'],identity)
sem.add_lexicon_rule("Divide",['divide'],identity)
sem.add_lexicon_rule("Multiply",['multiply'],identity)
sem.add_lexicon_rule("Multiplied",['multiplied'],identity)
sem.add_lexicon_rule("Times",['times'],identity)
sem.add_lexicon_rule("Product",['product'],identity)
sem.add_lexicon_rule("Minus",['minus'],identity)
sem.add_lexicon_rule("Subtracted",['subtracted'],identity)
sem.add_lexicon_rule("Sum",['sum'],identity)
sem.add_lexicon_rule("Added",['added'],identity)
sem.add_lexicon_rule("Plus",['plus'],identity)
sem.add_lexicon_rule("Negative",['negative'],identity)
sem.add_lexicon_rule("Between",['between'],identity)
sem.add_lexicon_rule("Random",['random'],identity)
sem.add_lexicon_rule("Number",['number'],identity)
sem.add_lexicon_rule("From",['from'],identity)

##############################################################################
# Now we will run the rules you are adding to solve problems in this lab.
import my_rules
my_rules.add_my_rules(sem)






# -*- coding: utf-8 -*-

import lab3.cfg
from lab3.category import Category, GrammarCategory, Variable, C, StarCategory
from lab3.semantic_rule_set import SemanticRuleSet
from lab3.semantic_db import pretty_print_entry

####################################################################

def translate(data):
    pass

def translateModifier(data):
    pass

####################################################################

identity = lambda x: x

sem = SemanticRuleSet()

####################################################################
# Speech Actions
def processSentence(data):
    print('data is')
    print(data)
    return {"scripts": [[111, 146, data]]}

def soundCommand(name):
    print("soudncomannd called")
    print('name is')
    print(name)
    return [["playSound:", name]]
    
def setVariable(var_name, value):
    return [["setVar:to:", value]]
    
def deleteVariable(variable_name):
    # TODO: modify project.json to delete variable from sprite
    # Should return nothing or empty string?
    pass
    
def createClone():
    print("creating clone")
    return [["createCloneOf:", "myself"]]
    
def createVariable(vl):
    ## to do
    pass

def Dur(np):
    if np == -1:
        return [["doForever:"]]
    return [["doRepeat:", np]]
   
# OPERATORS
def add(n1, n2):
    return n1 + n2
  

def ynQuestion(data):
    if sem.learned.yesno_query(data):
        return "Yes."
    else:
        return "No."


def whQuestion(data):
    results = sem.learned.wh_query(data)
    if len(results) == 0:
        return "I don't know."
    else:
        return list(results)[0]


def npOnlyHuhResponse(data):
    return "What about %s?"%(pretty_print_entry(data))


####################################################################
# Start rules


sem.add_rule("Start -> S", lambda s: processSentence(s))

# All Commands
sem.add_rule("S -> AL", identity)
sem.add_rule("AL -> AP", identity)
sem.add_rule("AP -> SoundCommand", identity)
sem.add_rule("AP -> CreateCommand", identity)
sem.add_rule("AP -> DataCommand", identity)

# Create Command
sem.add_rule("CreateCommand -> create a clone of myself", createClone())
sem.add_rule("CreateCommand -> 'make' Var VARIABLE_LIST", lambda make, x, vl: createVariable(vl))
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME", lambda vl: [vl])
sem.add_rule("VARIABLE_LIST -> VARIABLE_NAME 'and' VARIABLE_LIST", lambda vn, vl: [vn]+vl)
sem.add_rule("VARIABLE_NAME -> Var VARIABLE_NAME", lambda x, v: v)
sem.add_rule("Var -> Det Var", lambda det, var: var)

# Duration
sem.add_rule("Duration -> Unk 'times'", lambda np, times: Dur(times))

# Sound Commands
sem.add_rule("SoundCommand -> 'play' 'the' NAME_OF_SOUND 'sound'", lambda play, the, name, sound: soundCommand(name))
sem.add_rule("SoundCommand -> 'set' 'volume' 'to' NP", lambda set, volume, to, np: np)
sem.add_rule("SoundCommand -> 'change' 'volume' 'by' NP", lambda set, volume, to, np: np)


# Data Command (incomplete)
sem.add_rule("DataCommand -> 'delete' Var VARIABLE_NAME", lambda delete, var, var_name: deleteVariable(var_name))

sem.add_rule("DataCommand -> 'set' VARIABLE_NAME 'to' BP", lambda s, var_name, to, bp: setVariable(var_name, bp))

sem.add_rule("DataCommand -> 'set' VARIABLE_NAME 'to' Unk", lambda s, var_name, to, unk: setVariable(var_name, unk))

# Number Phrase
sem.add_rule("Unk -> NP", identity)
sem.add_rule("NP -> Unk", identity)
sem.add_rule("NP -> NPP", identity)
sem.add_rule("NP -> Det NPP", lambda det, npp: ' '.join([det,npp]))
sem.add_rule("NP -> VARIABLE_NAME", identity)
sem.add_rule("NP -> Unk 'plus' Unk", lambda unk1, plus, unk2: add(unk1, unk2)) 
sem.add_rule("NP -> Unk 'added' 'to' Unk", lambda unk1, added, to, unk2: add(unk1, unk2))
sem.add_rule("NPP -> 'sum' 'of' Unk 'and' Unk", lambda s, of, unk1, a,  unk2: add(unk1, unk2))

sem.add_rule("NP -> Unk 'minus' Unk", lambda unk1, minus, unk2: subtract(unk1, unk2))
sem.add_rule("NP -> Unk 'subtracted' 'by' Unk", lambda unk1, subtracted, by, unk2: unk1-unk2)

sem.add_rule("NP -> Unk 'times' Unk", lambda unk1, times, unk2: unk1*unk2)
sem.add_rule("NP -> Unk 'multiplied' 'by' Unk", lambda unk1, multiplied, by, unk2: unk1*unk2)
sem.add_rule("NPP -> 'product' 'of' Unk 'and' Unk", lambda product, of, unk1, a, unk2: unk1*unk2)

sem.add_rule("NP -> Unk 'divided' 'by' Unk", lambda unk1, divided, by, unk2: float(unk1)/unk2)
sem.add_rule("NPP -> 'random' 'number' 'between' Unk 'and' Unk", lambda r, n, b, unk1, a, unk2: random.choice([x for x in xrange(unk1, unk2+1)]))
sem.add_rule("NP -> 'negative' NP", lambda n, np: -1*np)
sem.add_rule("NP -> 'negative' Unk", lambda n, unk: -1*unk)

####################################################################
## Lexicon

# Names
sem.add_lexicon_rule("NAME_OF_SOUND",
                     ['meow'],
                     lambda name: name)

# # Common nouns
# sem.add_lexicon_rule("N[-mass, number=singular]",
#                      ['book', 'city', 'dog', 'man', 'park', 'woman', 'country'],
#                      lambda word: lambda det, apstar:\
#                          C("Object", type=word, definite=det, mod=apstar))


# # Determiners
sem.add_lexicon_rule("Det",
                      ['the', 'this'],
                      lambda word: word)

sem.add_lexicon_rule("Det",
                      ['a', 'an'],
                      lambda word: word)
 
sem.add_lexicon_rule("Var",
                      ['variable', 'variable' 'called'],
                      lambda word: word)
                      
sem.add_lexicon_rule("OrderAdverb",
                       ['first', 'second', 'third', 'firstly', 'secondly', 'thirdly', 'then', 'after', 'finally'],
                       identity)
                       
sem.add_lexicon_rule("Duration",
                       ['forever'],
                       Dur(-1))
                       
sem.add_lexicon_rule("Unk",
                       ['0','1','2','3','4','5','6','7','8','9'],
                       identity)                      


##############################################################################
# Now we will run the rules you are adding to solve problems in this lab.
import my_rules
my_rules.add_my_rules(sem)



from yapl_lexer import *
from yapl_parser import *
import sys

# other global variables
variables = {"global": {}, "local":{}}

types = {'float':float , 'int': int, 'string': str, 'bool': bool, 'True': True, 'False':False}

def assignment_eval(p, env): #add a check if theres a name then
    exp = exp_eval(p[-1],env)
    for_flag = 0
    if env not in ['global','local']:
        temp = env.split('-') # for, local
        env = temp[1]
        called_by = temp[2]
        for_flag = 1 

    if p[0] == "assignment":
        name = p[2]
        if for_flag == 1:
            name = 'for-' + called_by 
        if type(exp) is types[p[1]]:
            if name not in list(variables[env].keys()):
                if for_flag == 1:
                    variables[env][name] = {p[2]:exp , 'accessible_to':[]}
                    for loops in list(variables[env].keys()):
                        if loops != name:
                            variables[env][loops]['accessible_to'].append(name)
                        else: 
                            break
                else:
                    variables[env][name] = exp
            elif name in list(variables[env].keys()) and for_flag == 1:
                variables[env][name][p[2]] = exp # initializing variables in for loop
                
            else:
                print("RedeclarationError")
                sys.exit()
        else:
            print("DATATYPES DON'T MATCH") 
            sys.exit()
        
    elif p[0] == "update_var":
        if for_flag == 1:
            name = "for-" + called_by
            if p[1] in list(variables[env][name].keys()):
                variables[env][name][p[1]] = exp
                return
            for loop in reversed(list(variables[env].keys())):
                if p[1] in list(variables[env][loop].keys()):
                    if name in variables[env][loop]['accessible_to']:
                        variables[env][loop][p[1]] = exp 
                        return
                    else:
                        print("Cannot update variable")
                        sys.exit()
            print("Could not find variable")
            sys.exit()
        else:
            if p[1] in list(variables[env].keys()):
                variables[env][p[1]] = exp
            

    elif p[0] == 'struct':
        struct_name = p[1]
        variables["struct"] = {struct_name : {"def":{}, "instances": {}}}
        for i in range(len(p[2])):
            attr = p[2][i]
            attr_type = attr[1]
            attr_name = attr[2]
            variables["struct"][struct_name]["def"][attr_name] = attr_type

    elif p[0] == 'struct-instance':
        if p[1] in list(variables['struct'].keys()):
            variables['struct'][p[1]]['instances'][p[2]] = {}

    elif p[0] == 'attribute-update':
        struct_name = ""
        instance = p[1][1]
        attribute_name = p[1][2]
        attribute_value = p[2][1]

        for struct in list(variables["struct"].keys()):
            if instance in list(variables["struct"][struct]['instances'].keys()):
                struct_name = struct
        if struct_name != "":
            variables["struct"][struct_name]['instances'][instance][attribute_name] = attribute_value

    return None

def exp_eval(p,env): # evaluate expression
    optype = p[0]
    if optype == 'comma-sep':
        return str(exp_eval(p[1],env)) + " " + str(exp_eval(p[2],env)) + " "

    elif optype == 'PRINT':
        result = exp_eval(p[1],env)
        print(result)
    
    elif optype == 'assignment' or optype == 'update_var':
        assignment_eval(p,env)

    elif optype == 'for':
        name = "for"+"-"+p[1][2] #name of current loop
        if p[1][0] == 'assignment':
            assignment_eval(p[1], 'for-local-'+p[1][2])
            isTrue = exp_eval(p[2], 'for-local-'+p[1][2])
            while isTrue == True:
                if len(p)==5: #statements in for loop
                    for stmts in p[4]:
                        exp_eval(stmts,'for-local-'+p[1][2]) # run statements
                    if p[3][0] == 'unary':
                        exp_eval(p[3], 'for-local') #update own value
                    if p[3][0] == 'update_var':
                        assignment_eval(p[3],'for-local-'+p[1][2])
                    isTrue = exp_eval(p[2], 'for-local-'+p[1][2]) #check condition
            del variables['local'][name]
            for loop in list(variables['local'].keys()):
                if name in variables['local'][loop]['accessible_to']:
                    variables['local'][loop]['accessible_to'].remove(name)
                
            
                    

                     

    elif optype == 'attribute-ref':
        instance = p[1]
        attr = p[2]
        for struct in list(variables["struct"].keys()):
            if instance in list(variables["struct"][struct]['instances'].keys()):
                if attr in list(variables["struct"][struct]['instances'][instance].keys()):
                    return(variables["struct"][struct]['instances'][instance][attr])
                else:
                    print("AttributeError") 
                    sys.exit()


    elif optype == 'if':
        if(exp_eval(p[1],env) == True):
            run_program(p[2])
        else:
            if(len(p) == 4): #there exists elseif or else statements 
                if len(p[3])==1: #only else 
                    else_statement = p[3][0]
                    run_program(else_statement[1][0])
                elif len(p[3])>=2: #elseif and else both
                    isTrue = False
                    for i in range(len(p[3])-1): #elif elif else break if any true. #check if any else if true
                        if p[3][i][0] == 'elif':
                            elif_statement = p[3][i]
                            isTrue = exp_eval(elif_statement[1],env)
                            if isTrue == True:
                                for stmts in elif_statement[2]:
                                    run_program([stmts])
                                break
                            else:
                                continue
                    if isTrue == False:
                        else_statement = p[3][len(p[3])-1][0]
                        for stmts in else_statement[1]:
                            run_program([stmts])



    elif optype == 'logical': #NOT OPERATION
        if p[1] == '!':
            x = not exp_eval(p[2],env)
            return x

    elif optype == 'unary':
        if env == 'global':
            if p[1][1] in list(variables[env].keys()):
                val = variables[env][p[1][1]]
                if type(val) is int:
                    if p[2] == "++":
                        variables[env][p[1][1]] += 1
                    if p[2] == "--":
                        variables[env][p[1][1]] -= 1
                    #print(variables)
                else:
                    print("INVALID DATATYPE FOR UNARY OPERATION")
                    sys.exit()

            else:
                print ("VARIABLE DOES NOT EXIST")
                sys.exit()
        if env == 'for-local':
            temp = env.split('-')
            
            var_name = temp[0]+"-"+p[1][1]
            scope = temp[1]
            key = p[1][1]
            if key in list(variables[scope][var_name].keys()):
                val = variables[scope][var_name][key]
                if type(val) is int:
                    if p[2] == "++":
                        variables[scope][var_name][key] += 1
                    if p[2] == "--":
                        variables[scope][var_name][key] -= 1
                    #print(variables)
                else:
                    print("INVALID DATATYPE FOR UNARY OPERATION")
                    sys.exit()

    elif optype == 'binop':
        operator = p[1]
        if (type(exp_eval(p[2],env)) in [float, int, bool] and type(exp_eval(p[3],env)) in  [float,int,bool]) or (type(exp_eval(p[2],env)) == str and type(exp_eval(p[3],env) == str)):
            if operator == "+":
                return exp_eval(p[2],env) + exp_eval(p[3],env)
            elif operator == "==":
                return exp_eval(p[2],env) == exp_eval(p[3],env)
            elif operator == "!=":
                return exp_eval(p[2],env) != exp_eval(p[3],env)

        if type(exp_eval(p[2],env)) in [float, int,bool] and type(exp_eval(p[3],env)) in  [float,int,bool]:
            if operator == "-":
                return  exp_eval(p[2],env) - exp_eval(p[3],env)
            elif operator == '*':
                return  exp_eval(p[2],env) * exp_eval(p[3],env)
            elif operator == '/':
                if exp_eval(p[3],env)!= 0:
                    return  exp_eval(p[2],env) / exp_eval(p[3],env)
                else:
                    return "DivisionByZero"
                    sys.exit()
            elif operator == '>':
                return exp_eval(p[2],env) > exp_eval(p[3],env)
            elif operator == '>=':
                return exp_eval(p[2],env) >= exp_eval(p[3],env)
            elif operator == '<':
                return exp_eval(p[2],env) < exp_eval(p[3],env)
            elif operator == '<=':
                return exp_eval(p[2],env) <= exp_eval(p[3],env)
            elif operator == '^':
                return pow(exp_eval(p[2],env),exp_eval(p[3],env))
            elif operator == '&&':
                return (exp_eval(p[2],env) and exp_eval(p[3],env))
            elif operator == '||':
                return (exp_eval(p[2],env) or exp_eval(p[3],env))
        else:
            print("TypeError") 
            sys.exit()
    else:
        if p[0] == "NAME":
            minus_flag = 0
            for_flag = 0
            var = ""
            if p[1][0] == '-':
                var = p[1][1:]
                minus_flag = 1
            else:
                var = p[1] #number to find

            if env not in ['local', 'global']:
                temp = env.split('-')
                env = temp[1]
                called_by = temp[2] #which loop requires it
                caller = 'for-' + called_by
                for_flag = 1

            if for_flag == 1:
                for loop in reversed(list(variables["local"])): #recurse through reversed list of loops
                    if var in list((variables["local"][loop].keys())):
                        if loop == caller or caller in variables["local"][loop]["accessible_to"]:
                            return variables["local"][loop][var]
                if var in list(variables["global"].keys()):
                    return variables["global"][var]
                print("Could not find variable")
                sys.exit()

            if var in list(variables[env].keys()):
                if minus_flag == 1:
                    return -variables[env][var]
                else:
                    return variables[env][var]
            else:
                print("Could not find variable")
                sys.exit()

        elif p[0] == "BOOL":
            return types[p[1]]
        else:
            return p[1]


def stmt_eval(p): # p is the parsed statement subtree / program
    stype = p[0] # node type of parse tree
    if stype == 'PRINT':
        result = exp_eval(p[1],"global")
        print(result)
    if stype == 'unary' or stype == 'logical' or stype == 'if':
        result = exp_eval(p, "global")
    if stype == 'for':
        exp_eval(p, "local")
    if stype in ['assignment','update_var', "struct", "struct-instance", "attribute-update"]:
        assignment_eval(p, "global")




def run_program(p): # p[0] == 'Program': a bunch of statements
    for stmt in p: # statements in proglist
        if stmt != None:
            stmt_eval(stmt) # statement subtree as tuple
        

if len(sys.argv) == 1:
    print('File name/path not provided as cmd arg.')
    exit(1)

while True:
    fileHandler = open(sys.argv[1],"r")
    userin = fileHandler.read()
    fileHandler.close()

    print("Welcome to your YAPL's Interpreter!")
    parsed = parser.parse(userin)
    if not parsed:
        continue
    
    for line in userin.split('\n'):
        print(line)
    print("=========================================\n{OUTPUT}")
    try:
        run_program(parsed)
    except Exception as e:
        print(e)
    
    input("Press any key to run code again.")


exit()
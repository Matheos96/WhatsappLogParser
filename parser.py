import sys
import re

MIN_MSGS = 5

my_dict = {}

username_regex = r'-\s[^:]*[a-zA-Z]+[^:]*:'

def countLines():
    i=0
    for line in file.readlines():
        user = re.search(username_regex, line)
        if user is not None:
            user = user.group(0)
            user = user[2:len(user)-1]
            my_dict[user] = my_dict.get(user, 0)+1
        i = i+1
    return i

def outputInfo():
    string = ""
    summ = 0
    for k,v in my_dict.items():
        if(v>MIN_MSGS):
            summ+=v
    for k,v, in my_dict.items():
        if (v>MIN_MSGS):
            print(k+":"+str(v)+" ("+str(round((v/float(summ))*100))+"%)")
            


print("\n------------ Welcome to Whatsapp Log Parser by Matheos Mattsson ------------\n")
try:
    file = open(sys.argv[1], 'r', encoding="utf8")
    print("Number of lines in file: "+str(countLines())+"\n")

    print("---Messages/User---")
    outputInfo()

except Exception as e:
    print("No input file specified! Give the file as an argument: python parser.py 'path_to_file'")
    print(str(e))




    

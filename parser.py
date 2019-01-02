import sys
import re

#"Margin of error" --- This is the minimum amount of messages a "user" has to have to be conidered a user. This is required since the regex below might on special occasions match things in the chat messages too...
MIN_MSGS = 5

my_dict = {}

username_regex = r'-\s[^:]*[a-zA-Z]+[^:]*:'

start_date = ""

stop_date = ""

def parse_lines():
    global start_date
    global stop_date
    i=0
    for line in file.readlines():
        if i==0:
            start_date = line[0:11]
        else:
            stop_date = line[0:11]
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
    print("Total messages: "+str(summ)+"\n")
            


print("\n------------ Welcome to Whatsapp Log Parser by Matheos Mattsson ------------\n")
try:
    file = open(sys.argv[1], 'r', encoding="utf8")
    print("Number of lines in file: "+str(parse_lines())+" (a long message can stretch over more than one line)\n")

    print("Log for time interval: "+start_date+" to "+stop_date+"\n")

    print("---Messages/User---")
    outputInfo()
    file.close()

except Exception as e:
    print("No input file specified! Give the file as an argument: python parser.py 'path_to_file'")
    print(str(e))




    

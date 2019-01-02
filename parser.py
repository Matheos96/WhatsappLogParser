import sys
import re

# "Margin of error" --- This is the minimum amount of messages a "user" has to have to be considered a user.
# This is required since the regex below might on special occasions match things in the chat messages too...
MIN_MSGS = 5
MIN_SYMBOLS = 50

persons_msgs = {}

persons_symbols = {}

username_regex = r'-\s[^:]*[a-zA-Z]+[^:]*:'

start_date = ""

stop_date = ""


def parse_lines():
    global start_date
    global stop_date
    global persons_msgs
    global persons_symbols
    i = 0
    for line in file.readlines():
        if i == 0:
            start_date = line[0:11]
        else:
            stop_date = line[0:11]
        user = re.search(username_regex, line)
        if user is not None:
            user = user.group(0)
            user = user[2:len(user)-1]
            persons_msgs[user] = persons_msgs.get(user, 0) + 1
            persons_symbols[user] = persons_symbols.get(user, 0) + len(line)
        i = i+1
    return i


def output_info():
    global persons_msgs
    persons_msgs = [(k, persons_msgs[k]) for k in sorted(persons_msgs, key=persons_msgs.get, reverse=True)]
    global persons_symbols
    persons_symbols = [(k, persons_symbols[k]) for k in sorted(persons_symbols, key=persons_symbols.get, reverse=True)]
    summa = 0
    for k, v in persons_msgs:
        if v > MIN_MSGS:
            summa += v

    print("---Messages/User---")

    for k, v, in persons_msgs:
        if v > MIN_MSGS:
            print(k+":"+str(v)+" ("+str(round((v/float(summa))*100))+"%)")
    print("Total messages: "+str(summa)+"\n")

    sum_symbols = 0

    for k, v in persons_symbols:
        if v > MIN_SYMBOLS:
            sum_symbols += v

    print("---Symbols/User---")

    for k, v, in persons_symbols:
        if v > MIN_SYMBOLS:
            print(k+":"+str(v)+" ("+str(round((v/float(sum_symbols))*100))+"%)")
    print("Total symbols: "+str(sum_symbols)+"\n")
            

print("\n------------ Welcome to WhatsApp Log Parser by Matheos Mattsson ------------\n")
try:
    file = open(sys.argv[1], 'r', encoding="utf8")
    print("Number of lines in file: "+str(parse_lines())+" (a long message can stretch over more than one line)\n")

    print("Log for time interval: "+start_date+" to "+stop_date+"\n")

    output_info()
    file.close()

except Exception as e:
    print("No input file specified! Give the file as an argument: python parser.py 'path_to_file'")
    print(str(e))





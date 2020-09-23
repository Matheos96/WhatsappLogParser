import sys
import re

# -----------------------------------------SETUP-----------------------------------------

# "Margin of error" --- This is the minimum amount of messages a "user" has to have to be considered a user.
# This is required since the regex below might on special occasions match things in the chat messages too...
MIN_MSGS = 4
MIN_SYMBOLS = 50

# The amount of popular words to be listed (from most used to least)
NO_POPULAR_WORDS = 10

# Minimum letters per word in popular words
MIN_POP_LENGTH = 0

# ---------------------------------------------------------------------------------------

persons_msgs = {}

persons_symbols = {}

words = {}

words_searchable = {}

username_regex = r'-\s[^:]*[a-zA-Z]+[^:]*:'

msg_regex = r'-\s[^:]*[a-zA-Z]+[^:]*:.*'

start_date = ""

stop_date = ""


def parse_lines():
    global start_date
    global stop_date
    global persons_msgs
    global persons_symbols
    global words
    i = 0
    for line in file.readlines():

        message = re.search(msg_regex, line)  # Find username+message

        if message is not None:
            message = message.group(0).split(":", 1)[-1]  # Chop away username
        else:
            message = line  # If no username on line, just take whole thing

        for word in message.split():
            word = word.lower()
            if (len(word) >= MIN_POP_LENGTH) and (word[0] != "<") and (word[len(word)-1] != ">"):  # No whatsapp tags
                words[word] = words.get(word, 0) + 1

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
    global words
    global words_searchable
    words_searchable = words.copy()
    words = [(k, words[k]) for k in sorted(words, key=words.get, reverse=True)]
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

    print("---Most Popular words - Minimum word length = " + str(MIN_POP_LENGTH) + "---")
    i = 0
    for k, v, in words:
        if i == NO_POPULAR_WORDS:
            break
        i += 1
        print(str(i)+". "+k + ":" + str(v))
            

def user_option():
    choice = input("Choose an option\n")
    if choice == "1":
        find_word()
        return True
    elif choice == "0" or choice == "q":
        return False
    return True


def find_word():
    while True:
        word = input("Enter a word (type q to quit): ")
        if word == "q":
            break
        result = words_searchable.get(word.lower())
        if result is None:
            result = "0"
        print(word+" occurs a number of "+str(result)+" times!\n")


print("\n------------ Welcome to WhatsApp Log Parser by Matheos Mattsson ------------\n")
try:
    file = open(sys.argv[1], 'r', encoding="utf8")
    print("Number of lines in file: "+str(parse_lines())+" (a long message can stretch over more than one line)\n")

    print("Log for time interval: "+start_date+" to "+stop_date+"\n")

    output_info()
    file.close()

    while True:
        print("\nWhat do you want to do?\nq = quit\n1 = Search for a word \n")
        if not user_option():
            break

except Exception as e:
    print("No input file specified! Give the file as an argument: python parser.py 'path_to_file'")
    print(str(e))





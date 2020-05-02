import csv

global current_attack
global csvfile

def load_attack(file):
    global current_attack, csvfile
    csvfile = open('Attacks/' + file, newline='')
    current_attack = DictReaderToArray(csv.DictReader(csvfile, delimiter=',', quotechar='|'))
    print("Loaded " + file)

def read_attack():
    global current_attack
    attack = current_attack
    for row in attack:
        print(row)

def end_attack():
    global current_attack, csvfile
    current_attack = None
    csvfile.close()
    csvfile = None

def get_current_rows():
    global current_attack
    out = [current_attack[0]]
    current_attack.pop(0)
    while len(current_attack) > 0:
        if current_attack[0]['Time'] == '0':
            out.append(current_attack.pop(0))
        else:
            return out

def DictReaderToArray(reader):
    out = []
    for row in reader:
        out.append(row)
    return out


# TODO: Create a function that returns all rows with 0 as first entry before the next non-zero first entry (all actions that take place before next delay)
# Or I could reformat everything so that it uses elapsed time instead of time since

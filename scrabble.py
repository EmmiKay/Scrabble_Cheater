####----------Imports-------------####
from copy import deepcopy   #for deepcopies
import score_word as sw    #import my module with score_word function
import sys                 #import sys to use system arguments

####---------Argument handling-----------####
try:
    tiles = list(sys.argv[1].strip().upper())   #remove any surrounding whitespace and make upppercase
except IndexError:
    print('No arguments passed. Please add a string after scrabble.py.')
    exit()

####----------initialize variables--------####
wildcards = tiles.count('*') + tiles.count('?')
alpha_tiles = [x for x in tiles if x.isalpha()]  #tiles without positionals or wilds
length_wout_pos = len(alpha_tiles) + wildcards
word_list = []
positional = ''

####-----------Error Handling and Positional Finder-------------####
if length_wout_pos > 7 or length_wout_pos < 2:
    raise Exception("""Letters and wildcards must be between 2 and 7
    characters long.""")

if tiles.count('*') > 1 or tiles.count('?') > 1:
    raise Exception('Do not use more than 2 wildcards (one "*" and one "?"").')

if len(tiles) - length_wout_pos > 1:
    raise Exception("""Only 1 positional number between 1 and 7 can be used. Do not
    use non-alphanumerics except for wildcards (* or ?)""")

for i in range(0,len(tiles)):
    if tiles[i] in {'1', '2', '3', '4', '5', '6', '7'} and tiles[i] != tiles[-1]:
        if tiles[i+1].isalpha():
            positional = tiles[i] + (tiles[i+1])  #checks that alpha character comes after number and adds number and character to positional variable
        else:
            raise Exception('Positional numbers must be followed by one of the 26 letters- no wildcards.')
    elif tiles[i].isalpha() or tiles[i] == "*" or tiles[i] == '?':
        continue
    else:
        raise Exception("""Please only use the 26 letters of the alphabet, the numbers
        1-7 for position, and the wildcard symbols "?" or "*".
        Position numbers cannot be at the end of the entry.""")

if positional:
    if int(positional[0]) > length_wout_pos:
        raise Exception('Position number cannot be longer than the sum of your letters and wildcards.')


####----------Read .txt file------------####
with open("sowpods.txt","r") as infile:
    raw_input = infile.readlines()
    data = [datum.strip('\n') for datum in raw_input]


####----------Main Code--------------####
for word in data:               # go through each word in the sowpods.txt file
    if len(word) > length_wout_pos:   #if word length is longer than tiles (without positional number), stop here
        continue

    cp_word = deepcopy(list(word)) #deep copies to not affect originals
    cp_tiles = deepcopy(alpha_tiles)
    wilds = deepcopy(wildcards)
    cp_wilds = word            #don't need to deepcopy since strings are immutable

    if positional:          #if the positional variable was filled above:
        if len(word) < int(positional[0]):    #moves onto next word if word is shorter than positional number
            continue
        elif word[int(positional[0])-1] != positional[1]:  #moves onto next word if positional doesn't match word
            continue
        else:
            cp_word.remove(cp_word[int(positional[0])-1])   #if it all matches, removes the positional letters from both tile copy and word copy
            cp_tiles.remove(positional[1])

    while len(cp_word) != 0:
        if cp_word[0] in cp_tiles:
            cp_tiles.remove(cp_word[0]) #if the letter is in the tiles, remove from both cp_tiles and cp_word to eliminate double counting
            cp_word.pop(0)
        else:
            if wilds != 0:     #if letter isn't in the tiles, check number of wildcards
                cp_wilds = cp_wilds.replace(str(cp_word[0]), '?',1)  #if wilds used, this creates a "wild" version of the word get the score
                cp_word.pop(0)   #remove the letter from the word
                wilds -= 1   #remove 1 wildcard after use
            else:
                break    #break if the letter isn't in the tiles and all wildcards are used
    if len(cp_word) == 0:   #if the lenghth of cp_word is 0, all letters were in the tiles
        word_list.append((sw.score_word(cp_wilds), word.lower()))  #appends the tuple of word score and the word

sorted_tups = sorted(word_list, key=lambda tup: (-tup[0], tup[1]))    #sorted in reverse by score, and alphabetically by word


####------------Print Result------------####
for i in sorted_tups:
    print(f'({i[0]}, {i[1]})')     #I would have just printed "i", except that I had to remove the '' to make it match the homework example output
print('Total number of words:',len(sorted_tups))

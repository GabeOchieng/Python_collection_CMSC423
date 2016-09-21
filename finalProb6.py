import sys

f = open(sys.argv[1], 'r')
att = (f.readline()).split()
k = int(att[0])
d = int(att[1])
pair_list = []

'''
uses first/last k-1 chars as prefix/suffix nodes as demonstrated in class
creates a graph with k-1 chars as the nodes  and connect the to each other
to create strings of k length

notes:
for ever read
    get prefix_pair
    get suffix_pair
    add node for prefix if not in graph
    add node for suffix pair in not in graph
    add edge from prefix to suffix
'''

# initialize pair_list with tuples containing the pairs
for line in f:
    string = (line.rstrip()).split("|")         # split the pairs
    pair_list.append((string[0], string[1]))    # store as tuples into pair_list

# This function initializes a dictionary with the prefixs as keys
# and the suffixs as values. The values are matched based on their
# prefix but are stored as 
def get_path(pList):
    pair_dic = {}

    # appends mers with the same prefix to the prefix in the dictionary
    for pair in pList:
        if (pair[0][0:len(pair[0])-1], pair[1][0:len(pair[1])-1]) not in pair_dic:
            pair_dic[(pair[0][0:len(pair[0])-1], pair[1][0:len(pair[1])-1])] = []
            pair_dic[(pair[0][0:len(pair[0])-1], pair[1][0:len(pair[1])-1])].append((pair[0][1:len(pair[0])],pair[1][1:len(pair[0])]))
        else:
            pair_dic[(pair[0][0:len(pair[0])-1], pair[1][0:len(pair[1])-1])].append((pair[0][1:len(pair[0])],pair[1][1:len(pair[0])]))





    # populate out_list with values from pair_dic that represent outgoing edges
    out_list = []
    for key, value in pair_dic.items():
        for pair in value:
            out_list.append(pair)
    
    # add in keys to out_list that were not included in values of pair_dic
    combined_list = []
    combined_list = list(out_list)
    for key, value in pair_dic.items():
        if key not in out_list:
            combined_list.append(key)
    
    for pair in combined_list:
        # get number of occurences of this pair in out_list
        out_pair_count = 0
        for val in out_list:
            if val == pair:
                out_pair_count += 1

        # if pair occurs in the keys of pair_dic get number of incoming edges
        # else there are no incoming edges
        if pair in pair_dic:
            in_pair_count = len(pair_dic[pair])
        else:
            in_pair_count = 0 

        # find the imbalance
        if out_pair_count > in_pair_count:
            imbalance = pair
        elif out_pair_count < in_pair_count:
            replace_pair = pair
        # else equal

    # Fix the unbalanced edges by adding a out pair 
    if imbalance != None and replace_pair != None:
        if imbalance in pair_dic:
            pair_dic[imbalance].append(replace_pair) # add to existing pair
        else:
            pair_dic[imbalance] = [replace_pair]     # add new out list to pair



################################################################################
    #set up the eulerian path by iterating through to create a eulerian cycle

    # set first element in path to abitrary key from dictionary
    # path_list will contains the order that creates a eulerian path
    path_list = [pair_dic.keys()[0]]#(pair_dic.itervalues().next())
    curr = path_list[0]

    # This loop sets up the first iteration for creating the path
    while True:
        # append the outgoing edge to the path list
        path_list.append(pair_dic[curr][0])

        # remove outgoing edge from values of pair
        # if pair has no more outgoing edges, remove the pair from dictionary
        pair_dic[curr] = pair_dic[curr][1:len(pair_dic[curr])]
        if not pair_dic[curr]:
            del pair_dic[curr]

        # check if last pair in path has edge to another pair in dictionary
        # and assign curr to pair. Else break from loop.
        if path_list[len(path_list)-1] in pair_dic:
            curr = path_list[len(path_list)-1]
        else:
            break

    curr = None
    # if first loop did not solve to create path,
    # run until all pairs in pair dictionary are used
    while pair_dic:
        for i in range(len(path_list)):          # for each pair in path_list
            if path_list[i] in pair_dic:         # if pair is in dictionary,
                final_path_list = [path_list[i]] # add to final_path_list and set
                curr = path_list[i]              # curr to the pair

                # run this for each outgoing pair of curr pair
                # until pair is no longer in dictionary
                while True:
                    out_pair = pair_dic[curr][0]
                    final_path_list.append(out_pair)

                    # remove outgoing edge from values of pair if pair
                    # has no more outgoing edges, remove pair from dictionary
                    pair_dic[curr] = pair_dic[curr][1:len(pair_dic[curr])]
                    if not pair_dic[curr]:
                        del pair_dic[curr]

                    # check if last pair in path has edge to another pair
                    # in dictionary and assign curr to pair. Else break
                    if final_path_list[len(final_path_list)-1] in pair_dic:
                        curr = final_path_list[len(final_path_list)-1]
                    else:
                        break
                # insert the new path into the path_list at i
                path_list = path_list[0:i] + final_path_list + path_list[i+1:len(path_list)]
                break
    final_path_list = path_list
################################################################################ 

    # get location of imbalance and remove it to have
    # a complete cycle without overlap
    for i in range(len(final_path_list)-1):
         if final_path_list[i:i+2] == [imbalance, replace_pair]:
             return final_path_list[i+1:len(final_path_list)]+final_path_list[1:i+1]

def main():
    # get the eulerian path
    eulerian_path = get_path(pair_list)

    # reattach string with each k-1 mer from the first position
    # of each tuple to create first string
    first_string = eulerian_path[0][0]               # set to the first k-1 mer
    for pair in eulerian_path[1:len(eulerian_path)]: # iterate through and attach
        first_string += pair[0][-1]                  # each first position k-1 mer
    
    # reattach string with each k-1 mer from the second position
    # of each tuple to create second string
    second_string = eulerian_path[0][1]
    for pair in eulerian_path[1:len(eulerian_path)]:
        second_string += pair[1][-1]

    # combine first string and second_string, accounting for the
    # gap and print
    print first_string[0:k+d]+second_string

main()












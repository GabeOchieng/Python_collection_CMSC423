import sys
from random import randint

f = open(sys.argv[1], 'r')
att = (f.readline()).split()
k_global = int(att[0])
t_global = int(att[1])
N_global = int(att[2])
dna_list_global = [line.strip() for line in f.readlines()]

# This function returns the hamming distance between two strings.
def get_hamming(string1, string2):
    s1 = list(string1)
    s2 = list(string2)
    mismatches = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            mismatches += 1
    return mismatches


# This function returns the score of the motifs list. Iterates
# over the length of the motif and concats the chars of the same
# index for each motif. Then compares each motif to a string of
# each 'ACGT' chars of the same length and gets the hamming
# distance. Stores the score to a list and adds the min to the
# total score.
def get_score(motifs):
    score = 0
    for i in range(len(motifs[0])):
        concat_motif = ''                     # recombined motif variable
        for j in range(len(motifs)):          # concat char at index i from each motif
            concat_motif += motifs[j][i]
            
        temp_score_holder = []                # score list per iteration
        for base in 'ACGT':
            comparer = base*len(concat_motif) # generate comparer(ex. AAAAAAA)
            temp_score = get_hamming(concat_motif, comparer)
            temp_score_holder.append(temp_score)
        score += min(temp_score_holder)       # add min score
        
    return score


# This function returns the profile generated by the input motif
# based on the equation given in class. Iterates over the length
# of a motif and concats the chars of the same index for each
# motif. Then generates a probability from the equation using the
# number of occurences of each base + 1 and dividing it by t + 4.
# Then add each probability to list and append list to profile.
def get_pseudocount_profile(motifs):
    profile = []
    for i in range(len(motifs[0])): 
        concat_motif = ''               # recombined motif variable
        for j in range(len(motifs)):    # concat char at index i from each motif
            concat_motif += motifs[j][i]

        prob_list = []
        for base in 'ACGT':
            probability = float(concat_motif.count(base)+1)/float(len(concat_motif)+4)
            prob_list.append(probability)
        profile.append(prob_list)

    return profile


# This function returns the most profile probable motif in input.
# Iterates over a dna sequence and multiples the total probability
# with the respective loction in the profile. Does this for each
# k-mer in the sequence.
def get_most_probable(dna, k, profile):
    curr_prob = 1.0
    best_prob = 0.0
    motif = ''
    
    for i in range((len(dna)-k+1)):
        curr_prob = 1.0
        word = list(dna[i:i+k])

        for i in range(len(word)):
            if word[i] == 'A':
                curr_prob *= float(profile[i][0])
            elif word[i] == 'C':
                curr_prob *= float(profile[i][1])
            elif word[i] == 'G':
                curr_prob *= float(profile[i][2])
            elif word[i] == 'T':
                curr_prob *= float(profile[i][3])
        if curr_prob > best_prob:
            best_prob = curr_prob
            motif = "".join(str(p) for p in word)
            
    return motif


# This funciton returns the best motif base don the pseudocode
# provided by the problem. Genereates random numbers to get the
# index of the motifs and use it to get a profile with while
# excluding one motif based on a random number. Then adjusts the
# motif list at the random index with the most probable motif of
# the dna list based on the profile. Returns a list containing
# the score and the motif list.
def gibbs_sampler(dna_list, k, t, N):
    rand_nums = []
    motifs = []

    # generate random nums and use them to get the random motifs
    for i in range(t):
        rand_nums.append(randint(0,len(dna_list[0])-k))
    for i in range(len(rand_nums)):
        n = rand_nums[i]
        motifs.append(dna_list[i][n:n+k])

    # initialize best with initial score and motif list
    best = [get_score(motifs), motifs]

    
    for i in range(N):
        rand_num = randint(0,t-1)
        motifs_to_pass_in = []

        # pass in list of motifs except for the one at
        # random index to get a profile with pseudocount
        for j in range(len(motifs)):
            if j != rand_num:
                motifs_to_pass_in.append(dna_list[j])
        profile = get_pseudocount_profile(motifs_to_pass_in)

        # create a motif list with the replacement at the
        # random index with a most probable motif from profile
        new_motifs = []
        for j in range(len(motifs)):
            if j != rand_num:
                new_motifs.append(motifs[j])
            else:
                new_motifs.append(get_most_probable(dna_list[j], profile, k))
        motifs = new_motifs

        # adjust best score and motif list
        curr_score = get_score(motifs)
        if curr_score < best[0]:
            best_score = [curr_score, motifs]

    return best


# This block runs the code 20 times and keeps track of best 
best = [k_global*t_global, []]
for i in range(20):
    curr_score = gibbs_sampler(dna_list_global, k_global, t_global, N_global)
    if curr_score[0] < best[0]:
        best = curr_score



    
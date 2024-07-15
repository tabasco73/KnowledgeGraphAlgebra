import time
import ast
import itertools
import numpy as np

from combinatorial_algorithm.matrix_build import get_size_nperm

def assess_pairs(sets_list, pair_size):
    """
    Assess the given list of sets to determine missing and duplicate pairs.
    
    Parameters:
    - sets_list: A list of sets or lists with numbers.
    - pair_size: Desired size of the pairs (e.g., 2 for pairs, 3 for triplets, etc.).
    
    Returns:
    - missing_pairs: A set of pairs that are missing from the sets_list.
    - duplicate_pairs: A set of pairs that are duplicated in the sets_list.
    """
    # Extracting pairs from the given list of sets
    pairs = []
    for s in sets_list:
        pairs.extend(itertools.combinations(s, pair_size))
    
    # Convert each pair to a tuple where the numbers are sorted
    normalized_pairs = [tuple(sorted(pair)) for pair in pairs]
    #print(sets_list)
    # Determine the range based on the maximum number in the sets_list
    max_num = max(max(s) for s in sets_list)
    
    # Create all possible pairs of numbers within the range
    all_possible_pairs = set(itertools.combinations(range(1, max_num + 1), pair_size))
    
    # Convert normalized pairs into a set
    normalized_pairs_set = set(normalized_pairs)
    
    # Check if all possible pairs are in the extracted pairs
    missing_pairs = all_possible_pairs - normalized_pairs_set
    
    # Check for duplicate pairs
    # Using a set for improved time complexity when checking if an item is in it
    seen_pairs = set()
    duplicate_pairs = set()
    for pair in normalized_pairs:
        if pair in seen_pairs:
            duplicate_pairs.add(pair)
        else:
            seen_pairs.add(pair)
    
    return missing_pairs, duplicate_pairs





def transform_to_actual(skeleton, element_order, n):
    #TODO Replace Characters with Integers
    #alphabet_BIG = list(range(65, 65 +n))
    alphabet_BIG = create_unique_letter_combinations(n+1)[1:]
    #print(alphabet_BIG)
    #alphabet_BIG = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V']
    for i in range(len(element_order)):
        skeleton = np.where(skeleton == alphabet_BIG[i], element_order[i], skeleton)
    return skeleton


def permut_skeleton(la_permut, skeleton, skelet0, order, n):
    revers_la_permut = la_permut.copy()
    revers_la_permut.reverse()
    #print(la_permut)
    number_order = [la_permut] + [ [la_permut[k] for k in order[i]] for i in range(n-3)] + [revers_la_permut]
    #print(number_order)
    skeletons = [[] for i in range(n-1)]
    for i in range(n-1):
        skeletons[i] = transform_to_actual(skeleton.copy(), number_order[i], n)
    merged = np.vstack((skeletons[0], skeletons[1]))
    for k in range(2, n-1):
        merged = np.vstack((merged, skeletons[k]))
    merged = np.vstack((skelet0, merged))
    #print(merged)
    return merged


def rearrange_pairs(pair_indices, n):
    sorted_pairs = sorted(pair_indices, key=lambda x: x[1])
    sorted_pairs = [sorted_pairs[n*i:n*(i+1)] for i in range(n)]
    sorted_pairs = [ [a+1 for a,b in long] for long in sorted_pairs]
    #print(len(pair_indices))
    #print(sorted_pairs)
    if [] in sorted_pairs:
        print(pair_indices)
        print(len(pair_indices))
        print('hello')
    return sorted_pairs


def get_matches(element_names, big_skeleton, n):
    pairs = []
    for name in element_names:
        #print(element_names)
        indices = np.where(big_skeleton == name)
        paired_indices = list(zip(indices[0], indices[1]))
        temp = rearrange_pairs(paired_indices, n)
        pairs += temp
    return pairs


def recursive_combinations(current_comb, remaining_categories, results):
    # Om det inte finns några kategorier kvar, lägg till den nuvarande kombinationen till resultaten
    if not remaining_categories:
        results.append(current_comb)
        return
    # Ta den första kategorin från kvarvarande kategorier
    current_category = remaining_categories[0]
    for perm in current_category:
        overlap = False
        for existing_perm in current_comb:
            if 0 in tuple(a - b for a, b in zip(existing_perm, perm)):
                overlap = True
                break
        # Om det inte finns någon överlappning, fortsätt rekursivt med nästa kategori
        if not overlap:
            recursive_combinations(current_comb + [perm], remaining_categories[1:], results)

# Good for n = 2,3,5,7
def generate_stricter_combinations(permutations, n):
    #print(permutations)
    permutation_categories = [[] for i in range(n-3)]
    for perm in permutations:
        permutation_categories[perm[0]-1].append(perm)
    #print(permutation_categories)
    results = []
    recursive_combinations([], permutation_categories, results)
    stricter_combinations3 = []
    for comb in results:
        valid = True
        for i in range(int(len(comb)/2)):
            test = comb[len(comb)-1-i]
            test = test[::-1]
            if comb[i] != test:
                valid = False
        if valid:
            stricter_combinations3.append(comb)
    return stricter_combinations3

# Good for n = 2,3,5,7
def generate_permutations(possible_numbers, current_permutation=None, used_numbers=None):
    if current_permutation is None:
        current_permutation = []
    if used_numbers is None:
        used_numbers = set()
    # If we have a permutation of the required length
    if len(current_permutation) == len(possible_numbers):
        return [current_permutation.copy()]
    # Get the possible numbers for the current position
    curr_possible_nums = possible_numbers[len(current_permutation)]
    permutations = []
    for num in curr_possible_nums:
        if num not in used_numbers:
            current_permutation.append(num)
            used_numbers.add(num)
            # Recursively get permutations for the next position
            permutations.extend(generate_permutations(possible_numbers, current_permutation, used_numbers))
            # Backtrack
            current_permutation.pop()
            used_numbers.remove(num)
    new_permutations = []
    for perm in permutations:
        new_permutations.append(tuple(perm))
    return new_permutations

# Good for n = 2,3,5,7
def generate_correct_permutations(n):
    valid_permutations = []
    hackade_intervall = [(i, i+1) for i in range(n-1)]
    hackade_intervall2 = hackade_intervall.copy()
    for hack in hackade_intervall2:
        hack = (hack[1],hack[0])
        hackade_intervall.append(hack)
    # Using 1 to n-2 as the fixed numbers
    fixed_nums = list(range(1, n-2))
    for fixed in fixed_nums:
        remaining_nums = list(set(range(n-2)) - {fixed})
        permut = [[fixed]] + [[num for num in remaining_nums + [n-2] if num not in [i,n-2-i]] for i in range(1,n-1)]
        possible_permuts = generate_permutations(permut)
        valid_permutations.extend(possible_permuts)
    valid_permutations = [perm for perm in valid_permutations if not any(tuple(perm[i:i+2]) in hackade_intervall for i in range(len(perm)-1))]
    valid_permutations = [perm for perm in valid_permutations if not ((perm[0] == 1 and perm[1] != 3) or 
                                                                      (perm[-1] == 1 and perm[-2] != 3) or
                                                                        (3 in [perm[1],perm[-2]] and 1 not in [perm[0],perm[-1]]))]
    return valid_permutations

def get_optimal_wrt_one(skeleton, ordercombs, skelet0, combo1, n, standard):
    max_score = 2000000
    #ordercombs = ordercombs[:1]
    for iter, ordern in enumerate(ordercombs, start=1):
        if iter % 100000 == 0:
            print(iter)
        ordern = list(ordern)
        start_time2 = time.time()
        merged = permut_skeleton(standard, skeleton, skelet0, ordern, n)
        end_time2 = time.time()
        start_time3 = time.time()
        paired_combos = get_matches(standard + ['XXX'], merged, n) + combo1

        end_time3 = time.time()
        #print(paired_combos)
        start_time4 = time.time()
        test_missing, test_duplicate = assess_pairs(paired_combos, 2)
        score = len(test_missing) + len(test_duplicate)
        #print(score)
        if score == 0:
            print(score )
        if score < max_score:
            max_score = score
            best_permut = ordern
            best_skeleton = skeleton
            if score == 0:
                end_time4 = time.time()
        end_time4 = time.time()
    return best_skeleton, best_permut, [end_time2-start_time2, end_time3-start_time3, end_time4-start_time4]

def create_unique_letter_combinations(size):
    # Skapa en lista med unika bokstavskombinationer
    single_letters = [chr(i) for i in range(65, 91)]  # Enkelbokstäver A-Z
    double_letters = [a + b for a in single_letters for b in single_letters]  # Dubbelbokstäver AA, AB, ..., ZZ
    all_combinations = single_letters + double_letters

    # Klipp listan för att matcha den önskade storleken
    if size > len(all_combinations):
        raise ValueError("Storleken är för stor för att skapa unika bokstavskombinationer.")
    return all_combinations[:size]

def create_exact_diagonal_array(size):
    letters = create_unique_letter_combinations(size)
    # Initialize an empty array of the desired size
    arr = np.empty((size, size), dtype='<U3')  # U3 för att hantera upp till tre tecken långa strängar

    for i in range(size):
        for j in range(size):
            # If on the diagonal, set to 'XXX'
            if i == j:
                arr[i, j] = 'XXX'
            else:
                # Adjust the letter's position considering the rotation
                pos = (j - i + size) % size
                arr[i, j] = letters[pos]
    print(f'{arr=}')
    return arr



def optimal_permut_uneven(n):
    alphabet = list(range(n+2))
    alphabet = [str(a)+'.' for a in alphabet]
    combo1 = [ list(range(1+k*n,n*(k+1) + 1))for k in range(n)]
    standard = [letter for letter in alphabet[:n-1]]
    listan = [[letter for i in range(n)] for letter in standard]
    skelet0 = np.array(
        [['XXX' for i in range(n)]] + listan
    )
    skeleton_old = create_exact_diagonal_array(n)
    ordercombs = get_size_nperm(n)
    print('1')
    best_skeletonet, best_permut, times = get_optimal_wrt_one(skeleton_old, ordercombs, skelet0, combo1, n, standard)
    print('2')
    merged = permut_skeleton(standard, best_skeletonet, skelet0, best_permut, n)
    print('3')
    paired_combos = get_matches(standard + ['XXX'], merged, n) + combo1
    print('4')
    test_missing, test_duplicate = assess_pairs(paired_combos, 2)
    score = len(test_missing) + len(test_duplicate)
    #print(best_permut)
    #print(best_skeletonet)
    print(times)
    return score == 0, paired_combos

if __name__ == '__main__':
    verdict, res = optimal_permut_uneven(101)
    print(verdict)

import ast
from utility.utility_files import read_prompt, write_answer
from combinatorial_algorithm.matrix_check import optimal_permut_uneven


def swap_all_integers_n(new_values, n):
    if len(new_values) != n*n:
        print('Wrong size')
        return None 
    """
    Swap all integers in the predefined 3D array with the integers in new_values.
    
    :param new_values: The list of new integers that will replace the original integers.
    :return: The modified 3D array.
    """
    a, n121 = optimal_permut_uneven(n)
    mapping = dict(zip(range(1, n*n+1), new_values))
    for i in range(len(n121)):
        for j in range(len(n121[i])):
                n121[i][j] = mapping[n121[i][j]]
    return n121

if __name__ == '__main__':
    n = 29
    new_values = list(range(n*n+1, n*n*2+1))
    swapped_array = swap_all_integers_n(new_values, n)
    print(swapped_array)
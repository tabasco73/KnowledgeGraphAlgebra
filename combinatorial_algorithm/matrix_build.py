import numpy as np

def calc_value(i, j, modulus):
    förskjutning_fv_rad = (i+1)*j
    omoddat = (i + förskjutning_fv_rad)
    modskiftupp = -((i + förskjutning_fv_rad)//modulus)
    val = omoddat % modulus + modskiftupp
    while not(0 <= val < modulus):
        if val >= modulus:
            val = (val - 1) % modulus
        else :
            val = (val + 1) % modulus        
    return val

def create_updated_matrix(size, modulus):
    return np.array([[calc_value(i,j,modulus) for j in range(size)] for i in range(0, size // 2)])


def create_symmetric_matrix(matrix_5x10):
    flipped_rows = np.flip(matrix_5x10[::-1], axis=1)
    matrix_10x10 = np.vstack([matrix_5x10, flipped_rows])
    return matrix_10x10

def get_size_nperm(n):
    size = n-1
    modulus = n-1
    result_matrix = create_updated_matrix(size, modulus)
    #print(result_matrix)
    symmetric_result = create_symmetric_matrix(result_matrix)
    #print(symmetric_result)
    tr = [tuple(row) for row in symmetric_result]
    tr = [tr[1:-1]]
    #print(tr)
    #print(len(tr[0]))
    return tr

#get_size_nperm(17)



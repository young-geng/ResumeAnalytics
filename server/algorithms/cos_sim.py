"""
Cosine similarity
"""


"""
Cosine similarity of row vectors in matrix A and B
If matrix A is n by d, and matrix B is m by d,
this function returns a matrix n by m
"""
def cos_sim(A, B):
    A_norm = np.sum(np.square(A), axis=1)
    B_norm = np.sum(np.square(B), axis=1)
    product = A.dot(B.T)
    return product / (A_norm.dot(B_norm.T))

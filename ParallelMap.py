# Parallel mapping utilities
from multiprocessing import Pool as MP


def parmap(fuction, iter_list, threads=1):
    pool = MP(threads)
    retval = pool.map(fuction, iter_list)
    pool.close()
    pool.join()
    return retval





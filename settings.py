from suite2p import default_ops
from pathlib import Path


def generate_ops(one_photon=False, fs=20):

    ops = default_ops()
    ops['fs'] = fs
    ops['roidetect'] = False
    ops['keep_movie_raw'] = True
    ops['1Preg'] = one_photon

    return ops


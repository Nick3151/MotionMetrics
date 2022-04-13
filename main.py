import numpy as np
import sys
from pathlib import Path
from suite2p import run_s2p, default_ops, io
from metrics import mean_max_intensity, mean_correlation
import matplotlib.pyplot as plt


if __name__ == '__main__':
    fs = 20
    p = Path.cwd()
    p = p.parent
    p = p / 'Widefield' / '011222_GC32_GCaMP'
    # only run on specified tiffs
    db = {
        'look_one_level_down': False,  # whether to look in ALL subfolders when searching for tiffs
        'data_path': [str(p)],
        # a list of folders with tiffs
        # (or folder of folders with tiffs if look_one_level_down is True, or subfolders is not empty)
        'subfolders': [],  # choose subfolders of 'data_path' to look in (optional)
        'tiff_list': ['leftCam_011222_GC32_GCaMP.tif']  # list of tiffs in folder * data_path *!
    }
    ops = default_ops()
    ops['roidetect'] = False
    ops['fs'] = fs
    ops['keep_movie_raw'] = True
    ops['save_folder'] = 'register_default'

    ops_1p = ops.copy()
    ops_1p['1Preg'] = True
    ops_1p['save_folder'] = 'register_1p'

    output_ops = run_s2p(ops=ops, db=db)

    f = io.binary.BinaryFile(Lx=output_ops['Lx'], Ly=output_ops['Ly'], read_filename=output_ops['reg_file'])
    data_reg = f.data
    f = io.binary.BinaryFile(Lx=output_ops['Lx'], Ly=output_ops['Ly'], read_filename=output_ops['raw_file'])
    data_raw = f.data

    output_ops_1p = run_s2p(ops=ops_1p, db=db)
    f = io.binary.BinaryFile(Lx=output_ops_1p['Lx'], Ly=output_ops_1p['Ly'], read_filename=output_ops_1p['reg_file'])
    data_reg_1p = f.data

    mmp_pre = mean_max_intensity(data_raw)
    mmp_post = mean_max_intensity(data_reg)
    mmp_post_1p = mean_max_intensity(data_reg_1p)
    mcm_pre = mean_correlation(data_raw)
    mcm_post = mean_correlation(data_reg)
    mcm_post_1p = mean_correlation(data_reg_1p)

    t = np.arange(len(mmp_pre))/fs
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.plot(t, mmp_pre)
    plt.plot(t, mmp_post)
    plt.plot(t, mmp_post_1p)
    plt.title('Mean Maximum Projection')
    plt.legend(['raw', 'registered default', 'registered 1p'])

    plt.subplot(2, 1, 2)
    plt.plot(t, mcm_pre)
    plt.plot(t, mcm_post)
    plt.plot(t, mcm_post_1p)
    plt.title('Mean Correlation')
    plt.legend(['raw', 'registered default', 'registered 1p'])

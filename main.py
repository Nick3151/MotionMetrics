import numpy as np
import sys
import pandas as pd
from pathlib import Path
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import time

from suite2p import run_s2p, default_ops, io
from metrics import mean_max_intensity, mean_correlation
from settings import generate_ops


if __name__ == '__main__':
    folder_name = '120121_LC11_NC_GCaMP'
    side = 'right'
    file_name = side + 'Cam_' + folder_name
    save_folder_name_default = side + '_register_default'
    save_folder_name_1p = side + '_register_1p'
    fs = 20
    p = Path.cwd()
    p = p.parent
    p = p / 'Widefield' / folder_name

    db = {
        'data_path': str(p),
        'save_path0': str(p / save_folder_name_default),
        'tiff_list': [str(p / (file_name + '.tif'))]
    }

    Path.mkdir(p / save_folder_name_default, exist_ok=True)
    Path.mkdir(p / save_folder_name_1p, exist_ok=True)

    if not Path.exists(p / save_folder_name_default / 'ops_default.npy'):
        ops_default = generate_ops()
        np.save(str(p / save_folder_name_default / 'ops_default.npy'), ops_default)
    else:
        ops_default = np.load(str(p / save_folder_name_default / 'ops_default.npy'), allow_pickle=True)
        ops_default = ops_default.item()

    if not Path.exists(p / save_folder_name_1p / 'ops_1p.npy'):
        ops_1p = generate_ops(one_photon=True)
        np.save(str(p / save_folder_name_1p / 'ops_1p.npy'), ops_1p)
    else:
        ops_1p = np.load(str(p / save_folder_name_1p / 'ops_1p.npy'), allow_pickle=True)
        ops_1p = ops_1p.item()

    output_ops = run_s2p(ops=ops_default, db=db)

    f = io.binary.BinaryFile(Lx=output_ops['Lx'], Ly=output_ops['Ly'], read_filename=output_ops['reg_file'])
    data_reg = f.data
    f = io.binary.BinaryFile(Lx=output_ops['Lx'], Ly=output_ops['Ly'], read_filename=output_ops['raw_file'])
    data_raw = f.data

    db = {
        'data_path': str(p),
        'save_path0': str(p / save_folder_name_1p),
        'tiff_list': [str(p / (file_name + '.tif'))]
    }

    output_ops_1p = run_s2p(ops=ops_1p, db=db)
    f = io.binary.BinaryFile(Lx=output_ops_1p['Lx'], Ly=output_ops_1p['Ly'], read_filename=output_ops_1p['reg_file'])
    data_reg_1p = f.data

    win = 100
    overlap = 50
    t0 = time.time()
    print("Evaluate mean max projection...")
    mmp_pre = mean_max_intensity(data_raw, win, overlap)
    mmp_post = mean_max_intensity(data_reg, win, overlap)
    mmp_post_1p = mean_max_intensity(data_reg_1p, win, overlap)
    print("Run time %0.2f sec" % (time.time()-t0))
    t1 = time.time()
    print("Evaluate mean correlation...")
    mcm_pre = mean_correlation(data_raw, win, overlap)
    mcm_post = mean_correlation(data_reg, win, overlap)
    mcm_post_1p = mean_correlation(data_reg_1p, win, overlap)
    print("Run time %0.2f sec" % (time.time()-t1))

    t = np.arange(len(mmp_pre))/fs*(win-overlap)
    plt.figure(figsize=[12, 8])
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
    plt.show()

    metrics = np.array([[mmp_pre.mean(), mmp_post.mean(), mmp_post_1p.mean(), mcm_pre.mean(), mcm_post.mean(), mcm_post_1p.mean()]])
    # df = pd.DataFrame(data=metrics, index=[file_name],
    #                   columns=['Mean Max Projection Raw', 'Mean Max Projection Registered', 'Mean Max Projection Registered 1p',
    #                            'Mean Correlation Raw', 'Mean Correlation Registered', 'Mean Correlation Registered 1p'])
    # df.to_csv('metrics.csv', mode='a', header=False)

import numpy as np
import scipy


def corr2_coeff(A, B):
    # A: N * T
    # B: M * T
    # Return: N * M
    # Rowwise mean of input arrays & subtract from input arrays themeselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA**2).sum(1)
    ssB = (B_mB**2).sum(1)

    # Finally get corr coeff
    return np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))


def mean_max_intensity(images, win=100, overlap=50):
    assert win > overlap
    total_len = np.shape(images)[0]
    mmp_tmp = []
    for i in np.arange(0, total_len-win+overlap, win-overlap):
        i_tmp = np.arange(i, i+win)
        mmp_tmp.append(images[i_tmp, :, :].max(0).mean())
    mmp = np.array(mmp_tmp)
    return mmp


def mean_correlation(images, win=100, overlap=50):
    assert win > overlap
    total_len = np.shape(images)[0]
    mcm_tmp = []
    for i in np.arange(0, total_len-win+overlap, win-overlap):
        i_tmp = np.arange(i, i+win)
        images_tmp = images[i_tmp, :, :].reshape((win, -1))
        ref_tmp = images_tmp.mean(0).reshape((1, -1))
        mcm_tmp.append(corr2_coeff(images_tmp, ref_tmp).mean())
    mcm = np.array(mcm_tmp)
    return mcm

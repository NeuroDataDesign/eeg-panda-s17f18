from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats.mstats
import time
import warnings
warnings.filterwarnings("ignore")

def multivariatet(mean,cov,dof,N):
    d = len(cov)
    g = np.tile(np.random.gamma(dof/2.,2./dof,N),(d,1)).T
    Z = np.random.multivariate_normal(np.zeros(d),cov,N)
    return mean + Z/np.sqrt(g)
    
def eval_density(dcopula,u1,u2,bin_width):
    T = len(dcopula[0])
    proba = 0
    for t in range(0,T):
        if dcopula[0][t] > u1 and dcopula[0][t] <= u1+bin_width and \
           dcopula[1][t] > u2 and dcopula[1][t] <= u2+bin_width:
            proba += 1
            
    return proba / T
    
def build_density_copula(dcopula,nbBins=10):
    bin_width = 1 / nbBins
    m = bin_width / 2
    density_copula = np.zeros((nbBins,nbBins))
    bins_limit = np.linspace(0, 1, num=nbBins+1)[:nbBins]
    signatures = []
    
    for u1 in bins_limit:
        for u2 in bins_limit:
            ev_pr = eval_density(dcopula,u1,u2,bin_width)
            density_copula[round(u1/bin_width)][round(u2/bin_width)] = ev_pr
            signatures.append([np.array([u1+m,u2+m]),ev_pr])
                        
    return density_copula, signatures

def build_dist_mat(signatures):
    N = len(signatures)
    dist_mat = np.zeros((N,N))
    for i in range(0,len(signatures)):
        for j in range(i,len(signatures)):
            v1 = signatures[i][0]
            v2 = signatures[j][0]
            dist_mat[i,j] = np.linalg.norm(v1-v2)
            dist_mat[j,i] = dist_mat[i,j]
    
    return dist_mat
    
def gen_sample(mean,cov,N,nbins,typ):
    if typ=="Gaussian":
        XG = np.random.multivariate_normal(mean,cov,N)
        XG_x = scipy.stats.mstats.rankdata(XG[:,0]) / len(XG[:,0])
        XG_y = scipy.stats.mstats.rankdata(XG[:,1]) / len(XG[:,1])

        empirical_copula_XG = np.array([XG_x,XG_y])
        density_XG, signatures_ecopula_XG = build_density_copula(empirical_copula_XG,nbins)
        
        return XG, empirical_copula_XG, density_XG, signatures_ecopula_XG
    
    if typ=="Student":
        Xsample = multivariatet(mean,cov,3,N)
        Xsample_x = scipy.stats.mstats.rankdata(Xsample[:,0]) / len(Xsample[:,0])
        Xsample_y = scipy.stats.mstats.rankdata(Xsample[:,1]) / len(Xsample[:,1])
        
        empirical_copula = np.array([Xsample_x,Xsample_y])
        density_ecopula,signatures_ecopula = build_density_copula(empirical_copula,nbins)
        
        return Xsample, empirical_copula, density_ecopula, signatures_ecopula
        
def plot_copula_sample(X,ecopula,dcopula,typ):
    if typ=="Gaussian":
        fig = plt.figure(2,figsize=(20,5))
        fig.suptitle("(left) observations, (mid) pseudo-observations, (right) estimated density of the empirical copula",fontsize=20)
        ax = plt.subplot(1,3,1)
        ax.text(0.5, -0.1,'Bivariate Gaussian $\mathcal{N}(0,\Sigma)$', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.scatter(X[:,0],X[:,1])
        ax = plt.subplot(1,3,2)
        ax.text(0.5, -0.1,'Empirical copula transform', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.scatter(ecopula[0],ecopula[1])
        ax = plt.subplot(1,3,3)
        ax.text(0.5, -0.1,'Gaussian copula estimated density', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.pcolor(dcopula)
        plt.show()
    if typ=="Student":
        fig = plt.figure(1,figsize=(20,5))
        fig.suptitle("(left) observations, (mid) pseudo-observations, (right) estimated density of the empirical copula",fontsize=20)
        ax = plt.subplot(1,3,1)
        ax.text(0.5, -0.1,'Bivariate Student $\\nu = 3$', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.scatter(X[:,0],X[:,1])
        ax = plt.subplot(1,3,2)
        ax.text(0.5, -0.1,'Empirical copula transform', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.scatter(ecopula[0],ecopula[1])
        ax = plt.subplot(1,3,3)
        ax.text(0.5, -0.1,'Student $\\nu = 3$ copula estimated density', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)
        ax.pcolor(dcopula)
        plt.show()

def draw_timeseries(increments):
    fig = plt.figure(3,figsize=(20,15))
    plt.suptitle("Bivariate time series (the 2 variates share the same color)",fontsize=24)

    ax = plt.subplot(2,2,1)
    for i in range(5):
        incr = increments[i]
        incr_x = incr[:,0]
        sx = 10**3 + np.cumsum(incr_x)
        incr_y = incr[:,1]
        sy = 10**3 + np.cumsum(incr_y)
        clr = np.random.rand(3,)
        ax.plot(sx,color=clr)
        ax.plot(sy,color=clr)
    ax.text(0.5, -0.1,'The 2 variates are positively correlated (no-tail dependence)', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)

    ax = plt.subplot(2,2,2)
    for i in range(5,10):
        incr = increments[i]
        incr_x = incr[:,0]
        sx = 10**3 + np.cumsum(incr_x)
        incr_y = incr[:,1]
        sy = 10**3 + np.cumsum(incr_y)
        clr = np.random.rand(3,)
        ax.plot(sx,color=clr)
        ax.plot(sy,color=clr)
    ax.text(0.5, -0.1,'The 2 variates are positively correlated (tail dependence)', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)


    ax = plt.subplot(2,2,3)
    for i in range(10,15):
        incr = increments[i]
        incr_x = incr[:,0]
        sx = 10**3 + np.cumsum(incr_x)
        incr_y = incr[:,1]
        sy = 10**3 + np.cumsum(incr_y)
        clr = np.random.rand(3,)
        ax.plot(sx,color=clr)
        ax.plot(sy,color=clr)
    ax.text(0.5, -0.1,'The 2 variates are negatively correlated (no-tail dependence)', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)

    ax = plt.subplot(2,2,4)
    for i in range(15,20):
        incr = increments[i]
        incr_x = incr[:,0]
        sx = 10**3 + np.cumsum(incr_x)
        incr_y = incr[:,1]
        sy = 10**3 + np.cumsum(incr_y)
        clr = np.random.rand(3,)
        ax.plot(sx,color=clr)
        ax.plot(sy,color=clr)
    ax.text(0.5, -0.1,'The 2 variates are negatively correlated (tail dependence)', horizontalalignment='center',verticalalignment='center',transform=ax.transAxes,fontsize=16)

    plt.show()
    

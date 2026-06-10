'''
This counts the number of neighbors, as defined in Section 2.1, for each star in the search sample.  
Need to run this before making the binary catalog.
'''
from astropy.table import Table
import multiprocessing, psutil
from sklearn.neighbors import BallTree
from find_binaries_edr3 import duplicates_msk, unique_value_msk, fetch_table_element, get_delta_mu_and_sigma
 
tab = Table.read('edr3_parallax_snr5_goodG.fits.gz') # 64407853 sources

size_max_pc = 5 # max projected separation out to which to search
dispersion_max_kms = 5 # max velocity difference in kms
ra, dec, pmra, pmdec, parallax, parallax_error, pmra_error, pmdec_error, G = fetch_table_element(['ra', 'dec', 'pmra', 'pmdec', 'parallax', 'parallax_error', 'pmra_error', 'pmdec_error', 'phot_g_mean_mag'], tab )

s_max_cluster = 206265*size_max_pc
theta_max_radians = s_max_cluster/(1000/parallax)/3600 * np.pi/180
coords = np.vstack([dec*np.pi/180, ra*np.pi/180,]).T
tree = BallTree(coords[G < 18], leaf_size = 10, metric = 'haversine') # build tree of all stars brighter than 18

# data for stars brighter than G = 18
ra_b, dec_b, pmra_b, pmdec_b, parallax_b, parallax_error_b, pmra_error_b, pmdec_error_b, G_b = ra[G < 18], dec[G < 18], pmra[G < 18], pmdec[G < 18], parallax[G < 18], parallax_error[G < 18], pmra_error[G < 18], pmdec_error[G < 18], G[G < 18]

Nblock = 20000 # how many stars to process at once per core
Nmax = len(coords)//Nblock + 1 
sigma_cut = 2 # how many sigma tolerance 
def query_this_j(j):
    '''
    function to pass to multiprocessing pool. deal with Nblock stars. 
    '''
    # see how far along we are and make sure we aren't running out of memory.
    print(j, j*Nblock/len(coords),  psutil.virtual_memory().percent)

    # find the stars in this block
    msk = (np.arange(len(coords)) >= int(j*Nblock)) & (np.arange(len(coords)) < int((j+1)*Nblock))
    
    # find their companions and angular distances
    these_inds, these_dists = tree.query_radius(coords[msk], r = theta_max_radians[msk], return_distance = True)      
    
    # copy astrometry of stars in this block  
    parallax_, parallax_error_, pmra_, pmra_error_, pmdec_, pmdec_error_ = parallax[msk], parallax_error[msk], pmra[msk], pmra_error[msk], pmdec[msk], pmdec_error[msk] 

    # for each star, see how many of the companions within 5 pc (projected) have consistent parallax and similar proper motion 
    N_neighbors = np.zeros(len(parallax_))
    for i, idxs in enumerate(these_inds):
        thetas_arcsec = these_dists[i]*180/np.pi*3600
        d_par_over_sigma = np.abs(parallax_[i] - parallax_b[idxs])/np.sqrt(parallax_error_[i]**2 + parallax_error_b[idxs]**2)
        delta_mu, sigma_delta_mu = get_delta_mu_and_sigma(pmra1 = pmra_[i], pmdec1 = pmdec_[i], 
            pmra2 = pmra_b[idxs], pmdec2 = pmdec_b[idxs], pmra_error1 = pmra_error_[i], 
            pmdec_error1 = pmdec_error_[i], pmra_error2 = pmra_error_b[idxs], 
            pmdec_error2 = pmdec_error_b[idxs])
            
        mu_max = 0.21095*dispersion_max_kms*parallax_[i]            
        neighbors = (delta_mu < mu_max + sigma_cut*sigma_delta_mu) & (d_par_over_sigma < sigma_cut) & (thetas_arcsec > 1e-3) # theta > 1e-3 arcsec to make sure you don't count yourself as a neighbor
        N_neighbors[i] = np.sum(neighbors) 
    return N_neighbors

pool = multiprocessing.Pool(multiprocessing.cpu_count())
all_result = pool.map(query_this_j,  np.arange(Nmax))
pool.close()
N_neighbors = np.concatenate(all_result)

# save these for later
np.savez('neighbor_counts_edr3_all.npz', source_id = fetch_table_element('source_id', tab), N_neighbors = N_neighbors)

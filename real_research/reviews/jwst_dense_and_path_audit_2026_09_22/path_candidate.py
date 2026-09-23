import os
import json
import numpy as np

def simulate_photon(a, b, rng):
    x = np.zeros(3)
    u = rng.normal(size=3)
    u = u / np.linalg.norm(u)
    
    t = 0.0
    s = 0.0
    z = 0.0
    
    I_s = 0.0
    I_z = 0.0
    collisions = 0
    
    M = a + b
    
    max_steps = 10000
    
    for _ in range(max_steps):
        disc = z*z + 1.0 - s
        if disc < -1e-12:
            raise ValueError("Invalid geometry")
        disc = max(0.0, disc)
        dist_boundary = -z + np.sqrt(disc)
        
        dt_prop = rng.exponential(scale=1.0/M)
        dt = min(dt_prop, dist_boundary)
        
        I_s += a*(s*dt + z*dt*dt + dt**3/3.0) + b*(s*s*dt + 2*s*z*dt*dt + (2*s+4*z*z)*dt**3/3.0 + z*dt**4 + dt**5/5.0)
        I_z += a*(z*z*dt + z*dt*dt + dt**3/3.0) + b*(s*z*z*dt + (s*z+z**3)*dt*dt + (s+5*z*z)*dt**3/3.0 + z*dt**4 + dt**5/5.0)
        
        x = x + u * dt
        t += dt
        s = np.dot(x, x)
        z = np.dot(x, u)
        
        if dt == dist_boundary:
            return t, z, I_s, I_z, collisions, True
        
        prob_accept = (a + b*s) / M
        if rng.random() < prob_accept:
            collisions += 1
            while True:
                mu = 2.0 * rng.random() - 1.0
                if 3.0*(1.0 + mu*mu)/8.0 > rng.random():
                    break
            
            while True:
                v = rng.normal(size=3)
                v = v - np.dot(v, u)*u
                norm_v = np.linalg.norm(v)
                if norm_v > 1e-12:
                    v = v / norm_v
                    break
            
            u = mu*u + np.sqrt(1.0 - mu*mu)*v
            z = np.dot(x, u)
    
    raise ValueError("Max steps exceeded")

def main():
    mode = os.environ["ORCH_MODE"]
    inputs = json.load(open(os.environ["ORCH_INPUTS"]))
    
    profiles = [
        {"a": 1.0, "b": 0.0, "d": 0.5},
        {"a": 1.0, "b": 1.0, "d": 0.75}
    ]
    
    seeds = {
        "main": [1100101, 1100102],
        "positive": [1100201, 1100202],
        "negative": [1100301, 1100302]
    }
    
    N = 8000 if mode == "main" else 16000 if mode == "positive" else 8000
    
    checks = {}
    measurements = {}
    
    for profile, seed in zip(profiles, seeds[mode]):
        a = profile["a"]
        b = profile["b"]
        d = profile["d"]
        
        rng = np.random.default_rng(seed)
        
        T_arr = np.zeros(N)
        Z_arr = np.zeros(N)
        D_arr = np.zeros(N)
        Is_arr = np.zeros(N)
        Iz_arr = np.zeros(N)
        Coll_arr = np.zeros(N, dtype=int)
        
        for i in range(N):
            t, z, i_s, i_z, coll, escaped = simulate_photon(a, b, rng)
            if not escaped:
                continue
            T_arr[i] = t
            Z_arr[i] = z
            D_arr[i] = t - z
            Is_arr[i] = i_s
            Iz_arr[i] = i_z
            Coll_arr[i] = coll
        
        if mode == "negative":
            R = (T_arr - d)**2 - (2/3)*Is_arr - (11/9)*(1 - Z_arr**2)
        else:
            R = (D_arr - d)**2 - (2/3)*Is_arr - (11/9)*(1 - Z_arr**2)
        
        mean_R = np.mean(R)
        std_R = np.std(R)
        se_R = std_R / np.sqrt(N)
        z_score_R = mean_R / se_R if se_R > 0 else 0.0
        
        if a == 1.0 and b == 0.0:
            p_no_coll = np.exp(-1.0)
        elif a == 1.0 and b == 1.0:
            p_no_coll = np.exp(-4.0/3.0)
        
        n_no_coll = np.sum(Coll_arr == 0)
        freq_no_coll = n_no_coll / N
        
        se_no_coll = np.sqrt(p_no_coll * (1 - p_no_coll) / N)
        z_score_no_coll = (freq_no_coll - p_no_coll) / se_no_coll if se_no_coll > 0 else 0.0
        
        mean_D = np.mean(D_arr)
        std_D = np.std(D_arr)
        se_D = std_D / np.sqrt(N)
        z_score_D = (mean_D - d) / se_D if se_D > 0 else 0.0
        
        cert = (
            abs(z_score_R) <= 5.0 and
            abs(z_score_no_coll) <= 5.0 and
            abs(z_score_D) <= 5.0 and
            np.all(Z_arr >= -1e-12) and
            np.all(Z_arr <= 1 + 1e-12) and
            np.all(D_arr >= -1e-12)
        )
        
        if mode == "negative":
            cert = not cert
        
        checks["path_certificate"] = bool(cert)
        measurements[f"profile_{a}_{b}"] = {
            "z_score_R": z_score_R,
            "z_score_no_coll": z_score_no_coll,
            "z_score_D": z_score_D,
            "mean_D": mean_D,
            "freq_no_coll": freq_no_coll
        }
    
    print(json.dumps({
        "protocol": 2,
        "complete": True,
        "checks": checks,
        "measurements": measurements
    }))

if __name__ == "__main__":
    main()
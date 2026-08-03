import numpy as np
import matplotlib as plt
import pylhe

# path to uncompressed LHE file
# assuming in parent folder
lhe_file = "MG5_aMC_v3_5_3/higgs_gamgam/Events/run_01/unweighted_events.lhe"

masses = []

for event in pylhe.read_lhe(lhe_file):
    photons = []

    for particle in event.particles:
        # check if photon and final state / filter only outgoing photons
        if particle.id == 22 & particle.status == 1:
            photons.append(particle)

        if len(photons) == 2:
            p1 = photons[0]
            p2 = photons[1]

            Etot = p1.e + p2.e
            pxtot = p1.px + p2.px
            pytot = p1.py + p2.py
            pztot = p1.pz + p2.pz

            m2 = Etot**2 - (pxtot**2 + pytot**2 + pztot**2)
            m = np.sqrt(max(0,m2)) #use max to protect against float precision err

            masses.append(m)

# plot the invar mass
numbins = 50
xmin = 120
xmax = 130
binwidth = (xmax-xmin)/numbins
plt.figure(figsize=(6,4),dpi=300)
plt.hist(masses,bins=numbins,range=(xmin,xmax),color='pink',edgecolor='red')
plt.title(r'$H \to \gamma\gamma$',fontsize=14)
plt.xlabel('Invariant Mass',fontsize=12)
plt.ylabel(f'Counts / {binwidth} GeV',fontsize=12)
plt.grid(alpha=0.3)
plt.savefig("higgs_invarmass.png")
print("Analysis complete, figure saved as higgs_invarmass.png")
import numpy as np
import matplotlib.pyplot as plt
import pylhe

# path to uncompressed LHE file
# assuming in parent folder
lhe_file = "MG5_aMC_v3_5_3/higgs_gamgam/Events/run_01/unweighted_events.lhe"

masses = []

# need version-agnostic function for extracting
# tried different version 
def get_events(file_path):
    # Standard pylhe v1.0+ API
    if hasattr(pylhe, "LHEFile"):
        return pylhe.LHEFile.fromfile(file_path).events
    # Fallback options for legacy/alternative versions
    elif hasattr(pylhe, "read_lhe_with_attributes"):
        return pylhe.read_lhe_with_attributes(file_path)
    elif hasattr(pylhe, "read_lhe_file"):
        return pylhe.read_lhe_file(file_path)
    elif hasattr(pylhe, "read_lhe"):
        return pylhe.read_lhe(file_path)
    else:
        raise AttributeError("Could not find a supported reading function in pylhe.")

for event in get_events(lhe_file):
    photons = []

    for particle in event.particles:
        # check if photon and final state / filter only outgoing photons
        if (particle.id == 22) & (particle.status == 1):
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
    #print("photons: "+str(photons))

#print(masses)
# plot the invar mass
numbins = 100
xmin = 120
xmax = 130
binwidth = (xmax-xmin)/numbins
plt.figure(figsize=(5,4),dpi=300)
plt.hist(masses,bins=numbins,range=(123,128),color='pink',edgecolor='red')
plt.title(r'$H \to \gamma\gamma$ events from MadGraph5\_aMC@NLO',fontsize=14)
plt.xlabel(r'Invariant Mass $m_{\gamma\gamma}$',fontsize=12)
plt.ylabel(f'Counts / {binwidth} GeV',fontsize=12)
plt.grid(alpha=0.3)
figname = "sim_analysis/plots/madgraph_higgs_invarmass.png"
plt.tight_layout()
plt.savefig(figname)
print("Analysis complete, figure saved as " + figname)

np.savez(
    "mg_hmass_histogram_data.npz",
    masses=masses,
)
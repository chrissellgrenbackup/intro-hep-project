import numpy as np
import matplotlib.pyplot as plt
import pylhe

# path to uncompressed LHE file
# assuming in parent folder
lhe_file = "MG5_aMC_v3_5_3/higgs_gamgam/Events/run_01/unweighted_events.lhe"

pts_lead = []
pts_sub = []
etas = []
dphis = []

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
    photons = [p for p in event.particles if (p.id == 22) & (p.status == 1)]

    if len(photons) == 2:
        p1 = photons[0]
        p2 = photons[1]

        pt1 = np.sqrt(p1.px**2+p1.py**2)
        pt2 = np.sqrt(p2.px**2+p2.py**2)

        # check which photon is leading
        if pt1 > pt2:
            plead = p1
            psub = p2
        else:
            plead = p2
            psub = p1

        # unncessary repeat
        pts_lead.append(np.sqrt(plead.px**2+plead.py**2))
        pts_sub.append(np.sqrt(psub.px**2+psub.py**2))

        for p in (plead,psub):
            pmag = np.sqrt(p.px**2+p.py**2+p.pz**2)
            eta = 0.5 * np.log((pmag+p.pz)/(pmag-p.pz))
            etas.append(eta)

        phi1 = np.arctan2(p1.py,p1.px)
        phi2 = np.arctan2(p2.py,p2.px)
        dphi = np.abs(phi1-phi2)
        if dphi > np.pi: dphi = 2*np.pi - dphi
        dphis.append(dphi)

fig, axes = plt.subplots(2,2,figsize=(12,10),dpi=400)

# 1. Leading Photon pT
axes[0, 0].hist(pts_lead, bins=40, range=(0, 100), color='crimson', edgecolor='black', alpha=0.7)
axes[0, 0].set_title(r'Leading Photon Transverse Momentum $p_T^{\gamma_1}$',fontsize=14)
axes[0, 0].set_xlabel(r'$p_T$ [GeV]',fontsize=14)
axes[0, 0].set_ylabel('Events',fontsize=14)

# 2. Subleading Photon pT
axes[0, 1].hist(pts_sub, bins=40, range=(0, 100), color='coral', edgecolor='black', alpha=0.7)
axes[0, 1].set_title(r'Subleading Photon Transverse Momentum $p_T^{\gamma_2}$',fontsize=14)
axes[0, 1].set_xlabel(r'$p_T$ [GeV]',fontsize=14)
axes[0, 1].set_ylabel('Events',fontsize=14)

# 3. Pseudorapidity
axes[1, 0].hist(etas, bins=40, range=(-4, 4), color='mediumpurple', edgecolor='black', alpha=0.7)
axes[1, 0].set_title(r'Photon Pseudorapidity $\eta_\gamma$',fontsize=14)
axes[1, 0].set_xlabel(r'$\eta$',fontsize=14)
axes[1, 0].set_ylabel('Photons',fontsize=14)

# 4. Delta Phi
axes[1, 1].hist(dphis, bins=40, range=(0, np.pi), color='teal', edgecolor='black', alpha=0.7)
axes[1, 1].set_title(r'Azimuthal Separation $\Delta\phi_{\gamma\gamma}$',fontsize=14)
axes[1, 1].set_xlabel(r'$\Delta\phi$ [rad]',fontsize=14)
axes[1, 1].set_ylabel('Events',fontsize=14)

# export the data to read into the Hgg_analysis notebook (for side by side data vs. MC plots)
np.savez(
    "mg_kin_histogram_data.npz",
    pts_lead=pts_lead,
    pts_sub=pts_sub,
    etas=etas,
    dphis=dphis,
)

plt.suptitle("Photon Kinematics for Raw MadGraph Events",fontsize=16,y=0.96)
plt.tight_layout()
plt.savefig("sim_analysis/plots/madgraph_photon_kinematics.png")
print("Saved kinematic plots as 'sim_analysis/plots/madgraph_photon_kinematics.png'.")
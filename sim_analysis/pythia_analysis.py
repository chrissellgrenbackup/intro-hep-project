import pyhepmc
import vector
import matplotlib.pyplot as plt
import numpy as np

dirpath = '/Users/chris/intro-hep-project/MG5_aMC_v3_5_3/higgs_gamgam/Events/run_02/'
filename = "tag_1_pythia8_events.hepmc"

pts_lead = []
pts_sub = []
etas = []
dphis = []
masses = []

print("looping over events")

with pyhepmc.open(dirpath+filename) as f:
    for event in f:
        # create 4-vec object for all photons in event that are in final state
        photons = [vector.obj(px=p.momentum.px,py=p.momentum.py,pz=p.momentum.pz,E=p.momentum.e)
            for p in event.particles if (p.pid == 22) and (p.status == 1)]

        # sort photons descending pT
        photons.sort(key=lambda p:p.pt,reverse=True)

        if len(photons)>=2:
            lead = photons[0]
            sublead = photons[1]
            diphoton = lead + sublead
            masses.append(diphoton.mass)

            pts_lead.append(lead.pt)
            pts_sub.append(sublead.pt)
            etas.extend([lead.eta,sublead.eta])
            dphi = np.abs(lead.phi-sublead.phi)
            if dphi > np.pi: dphi = 2*np.pi - dphi
            dphis.append(dphi)

print("loop done")

np.savez(
    "/Users/chris/intro-hep-project/histodata/pythia_kin_histogram_data.npz",
    pts_lead=pts_lead,
    pts_sub=pts_sub,
    etas=etas,
    dphis=dphis,
    masses=masses
)
print("saved events to /Users/chris/intro-hep-project/histodata/pythia_kin_histogram_data.npz")

#fig, axes = plt.subplots(2,2,figsize=(12,10),dpi=400)
#plt.title("Photon Kinematics after Pythia8 Showering")
## 1. Leading Photon pT
#axes[0, 0].hist(pts_lead, bins=40, range=(0, 100), color='crimson', edgecolor='black', alpha=0.7)
#axes[0, 0].set_title(r'Leading Photon Transverse Momentum $p_T^{\gamma_1}$')
#axes[0, 0].set_xlabel(r'$p_T$ [GeV]')
#axes[0, 0].set_ylabel('Events')
#
## 2. Subleading Photon pT
#axes[0, 1].hist(pts_sub, bins=40, range=(0, 100), color='coral', edgecolor='black', alpha=0.7)
#axes[0, 1].set_title(r'Subleading Photon Transverse Momentum $p_T^{\gamma_2}$')
#axes[0, 1].set_xlabel(r'$p_T$ [GeV]')
#axes[0, 1].set_ylabel('Events')
#
## 3. Pseudorapidity
#axes[1, 0].hist(etas, bins=40, range=(-4, 4), color='mediumpurple', edgecolor='black', alpha=0.7)
#axes[1, 0].set_title(r'Photon Pseudorapidity $\eta_\gamma$')
#axes[1, 0].set_xlabel(r'$\eta$')
#axes[1, 0].set_ylabel('Photons')
#
## 4. Delta Phi
#axes[1, 1].hist(dphis, bins=40, range=(0, np.pi), color='teal', edgecolor='black', alpha=0.7)
#axes[1, 1].set_title(r'Azimuthal Separation $\Delta\phi_{\gamma\gamma}$')
#axes[1, 1].set_xlabel(r'$\Delta\phi$ [rad]')
#axes[1, 1].set_ylabel('Events')
#
#plt.tight_layout()
#plt.savefig("plots/pythia_photon_kinematics.png")
#print("Saved kinematic plots as 'pythia_photon_kinematics.png'.")
#
## plot the invar mass
#numbins = 100
#xmin = 120
#xmax = 130
#binwidth = (xmax-xmin)/numbins
#plt.figure(figsize=(6,4),dpi=300)
#plt.hist(masses,bins=numbins,range=(xmin,xmax),color='pink',edgecolor='red')
#plt.title(r'$H \to \gamma\gamma$, after Pythia8 showering',fontsize=14)
#plt.xlabel('Invariant Mass',fontsize=12)
#plt.ylabel(f'Counts / {binwidth} GeV',fontsize=12)
#plt.grid(alpha=0.3)
#figname = "plots/pythia_higgs_invarmass.png"
#plt.savefig(figname)
#print("Analysis complete, figure saved as " + figname)

#print("Doing tests on number of photons that pass test")
#print("Num photons with no eta restriction: "+str(len(etas)))
#etas_survive = [eta for eta in etas if np.abs(eta) < 2.37]
#print("Num photons passing eta restriction: "+str(len(etas_survive)))
#pts_sub_survive = [pt for pt in pts_sub if pt > 10]
#print("Num sublead photons passing pt restriction: "+str(len(pts_sub_survive)))
#pts_lead_survive = [pt for pt in pts_lead if pt > 10]
#print("Num lead photons passing pt restriction: "+str(len(pts_lead_survive)))
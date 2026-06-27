#include <TLorentzVector.h>
#include <iostream>
#include "TRandom3.h"

void basic4vec(){
    TLorentzVector muon1;
    TLorentzVector muon2;
    TLorentzVector parent;

    TRandom3 rand(0);
    Double_t phi =  rand.Uniform(-3.14,3.14);
    Double_t phi2 = rand.Uniform(-3.14,3.14);
    Double_t eta =  rand.Uniform(-5,5);
    Double_t eta2 = rand.Uniform(-5,5);
    Double_t pt = 20; //gev
    Double_t pt2 = 15; 
    muon1.SetPtEtaPhiM(pt,eta,phi,0.105); //muon
    muon2.SetPtEtaPhiM(pt2,eta2,phi2,0.105);

    parent = muon1 + muon2;
    Double_t mass = parent.M();

    Printf("The invariant mass of the parent particle is: %f GeV", mass);

   // std::cout << "the invariant mass of the parent particle is: " << mass << " GeV." << std::endl;
    
}
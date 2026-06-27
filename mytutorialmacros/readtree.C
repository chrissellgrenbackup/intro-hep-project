// goal:
// open .root file containing TTree() (use one from this folder created by tree102basic)
// get the tree
// declare variable called setbranchaddress
// create TH1F histogram
// run the event loop, filling the histogram each iteration
// draw the histogram

//for each event:
   // load it (GetEntry)
  //  apply selections (cuts)
  //  compute quantities
 //   fill histograms

 #include <TFile.h>
 #include <TTree.h>
 #include <TCanvas.h>
 #include <TH1F.h>
 #include <iostream>

void readtree(){
    auto f = TFile::Open("tree102.root"); // opening root file
    // now make tree object from root file
    TTree* T = (TTree*)f->Get("ntuple");

    Float_t x;
    T->SetBranchAddress("x",&x);

    auto h1 = new TH1F("h1","x",100,-4,4); // what are reasonable ranges here?
    Int_t nevent = T->GetEntries(); 

    for (Int_t iev=0;iev<nevent; iev++){
        T->GetEntry(iev);
        if (iev % 1000 ==0) std::cout<< "Processing event " << iev << std::endl;
        h1->Fill(x);
    }
    auto c1 = new TCanvas();
    h1->Draw();
    std::cout << "I should now see the histogram of x" << std::endl;
}
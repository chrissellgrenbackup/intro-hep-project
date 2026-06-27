#include <TRandom.h>
#include <TTree.h>
#include <TCanvas.h>
#include <TStyle.h>

#include <Riostream.h>

class Detector {
    public:
        Double_t E; // energy
        Double_t t; // time
};

class Event : public TObject {
    public:
        Detector a;
        Detector b;

        ClassDefOverride(Event,1)
};

void tree103basic_copy(){
    // create a TTree
    auto tree = new TTree("tree", "treelibrated tree");
    auto e = new Event;

    // create a branch with energy
    tree->Branch("event",&e);
    // fill in some events with random numbers
    Int_t nevent = 10000;
    for (Int_t iev=0; iev<nevent; iev++){
        if (iev % 1000 == 0)
            std::cout << "Processing event " << iev << "..." << std::endl;
        
        Float_t ea, eb;
        gRandom->Rannor(ea,eb);
        e->a.E = ea;
        e->b.E = eb;
        e->a.t = gRandom->Rndm();
        e->b.t = e->a.t + gRandom->Gaus(0.,.1); // same time as a but with random "resolution"

        tree->Fill(); // fill tree with current event
    }

    // start the viewer, can look at structure of Event class
    tree->StartViewer();
    gROOT->SetStyle("Plain");
    // create tree variables
    auto c1 = new TCanvas();
    c1->Divide(2,2);
    c1->cd(1);
    tree->Draw("a.E");
    tree->Draw("a.E","3*(-.2<b.E && b.E<.2)","same"); //energy condition on b, scaled by 3
    c1->cd(2);
    tree->Draw("b.E:a.E","","colz"); // one energy against the other
    c1->cd(3);
    tree->Draw("b.t","","e");
    tree->Draw("a.t","","same"); 
    c1->cd(4);
    tree->Draw("b.t:a.t");

    std::cout << std::endl;
    std::cout << "You can now examine structure of the tree in the TreeViewer" << std::endl;
    std::cout << std::endl;
}
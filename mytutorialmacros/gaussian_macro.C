#include "TH1F.h"
#include "TRandom3.h"
#include "TCanvas.h"

void gaussian_macro() {
    // create my hist
    TH1F *hist = new TH1F("myhist", "Gaussian Distribution Init Test; Value; Entries", 100, -10, 10);
    //initialize generator
    TRandom3 rand;
    // loop 10,000 times to generate data and fill hist
    for (int i = 0; i < 10000; ++i){
        double val = rand.Gaus(0,2);
        hist->Fill(val);
    }

    // make canvas to draw on
    TCanvas *c1 = new TCanvas("c1", "Canvas", 800, 600);
    hist->SetFillColor(kBlue - 9);
    hist->SetLineColor(kBlue + 2);
    hist->SetLineWidth(2);

    hist->Draw();

    c1->SaveAs("firstplot.pdf");
}
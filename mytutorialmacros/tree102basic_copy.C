void tree102basic_copy() { 
    TString dir = gROOT->GetTutorialDir();
    dir.Append("/io/tree");
    dir.ReplaceAll("/./","/");

    auto f = TFile::Open("tree102.root", "RECREATE");
    auto h1 = new TH1F("h1", "x distribution",100,-4,4);
    auto T = new TTree("ntuple","data from ascii file");
    Long64_t nlines = T->ReadFile(TString::Format("%s/basic.dat",dir.Data()),"x:y:z");
    printf("found %lld points\n",nlines);
    T->Draw("x", "z>2");
    T->Write();
}
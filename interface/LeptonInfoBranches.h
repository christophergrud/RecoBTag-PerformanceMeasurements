#ifndef LEPTONINFOBRANCHES_H
#define LEPTONINFOBRANCHES_H

#include <TTree.h>
#include "DataFormats/MuonReco/interface/MuonSelectors.h"

const UInt_t nMaxGens_= 100000;
const UInt_t nMaxMus_= 100000;

class LeptonInfoBranches {

  public :

    int   nMu;
    int   nGenPart;

    //----------------------
    // Pat Mu Basic Variables
    //----------------------
    float Mu_pt[nMaxMus_];
    float Mu_eta[nMaxMus_];
    float Mu_phi[nMaxMus_];
    float Mu_mass[nMaxMus_];


    //-----------------------
    // Pat Mu Isolation Variables
    //-----------------------
    float   Mu_trkIso[nMaxMus_];
    float   Mu_trackerIsoSumPT[nMaxMus_];
    float   Mu_ecalIso[nMaxMus_];
    float   Mu_hcalIso[nMaxMus_];
    float   Mu_hoIso[nMaxMus_];
    float   Mu_ecalVetoIso[nMaxMus_];
    float   Mu_hcalVetoIso[nMaxMus_];
    float   Mu_pfisor03chargedhadron[nMaxMus_];
    float   Mu_pfisor03chargedparticle[nMaxMus_];
    float   Mu_pfisor03neutralhadron[nMaxMus_];
    float   Mu_pfisor03photon[nMaxMus_];
    float   Mu_pfisor03neutralhadronht[nMaxMus_];
    float   Mu_pfisor03photonht[nMaxMus_];
    float   Mu_pfisor03pu[nMaxMus_];
    float   Mu_pfisor04chargedhadron[nMaxMus_];
    float   Mu_pfisor04chargedparticle[nMaxMus_];
    float   Mu_pfisor04neutralhadron[nMaxMus_];
    float   Mu_pfisor04photon[nMaxMus_];
    float   Mu_pfisor04neutralhadronht[nMaxMus_];
    float   Mu_pfisor04photonht[nMaxMus_];
    float   Mu_pfisor04pu[nMaxMus_];
    
    //------------------
    // Pat Mu ID variables
    //------------------
    int Mu_isPF[nMaxMus_];
    int Mu_isGlobal[nMaxMus_];
    int Mu_isTracker[nMaxMus_];
    int Mu_isGood[nMaxMus_];
    int Mu_isHighPt[nMaxMus_];
    int Mu_nTrackLayers[nMaxMus_];
    int Mu_nPixelLayers[nMaxMus_];
    int Mu_nPixelHits[nMaxMus_];
    int Mu_nValidHits[nMaxMus_];
    int Mu_nMatchedStations[nMaxMus_];
    float Mu_innerTrack_normChi2[nMaxMus_];
    float Mu_innerTrack_dxyVertPos[nMaxMus_];
    float Mu_innerTrack_dzVertPos[nMaxMus_];
    float Mu_bestTrack_dzVertPos[nMaxMus_];
    float Mu_bestTrack_dxyVertPos[nMaxMus_];
    float Mu_globalTrack_normChi2[nMaxMus_];
    float Mu_IP3D[nMaxMus_];
    float Mu_IP3Der[nMaxMus_];
    float Mu_IP2D[nMaxMus_];
    float Mu_IP2Der[nMaxMus_]; 
    
    //------------------------
    // MC Truth Information
    //------------------------
    float GenPart_phi[nMaxGens_];
    float GenPart_pt[nMaxGens_];
    float GenPart_eta[nMaxGens_];
    int GenPart_mother[nMaxGens_];
    float GenPart_mass[nMaxGens_];
    int GenPart_pdgid[nMaxGens_];
    int GenPart_status[nMaxGens_];
    float GenPart_vertX[nMaxGens_];
    float GenPart_vertY[nMaxGens_];
    float GenPart_vertZ[nMaxGens_];

    void RegisterTree(TTree *tree, std::string name="") {
      if(name!="") name += ".";
      //------------------------------
      // Pat Mu Isolation Variables
      //------------------------------
      tree->Branch((name+"nMu").c_str()         ,&nMu        ,(name+"nMu/I").c_str());
      tree->Branch((name+"Mu_trkIso").c_str()   ,Mu_trkIso   ,(name+"Mu_trkIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_trackerIsoSumPT").c_str()   ,Mu_trackerIsoSumPT   ,(name+"Mu_trackerIsoSumPT["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_ecalIso").c_str()   ,Mu_ecalIso   ,(name+"Mu_ecalIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_hcalIso").c_str()  ,Mu_hcalIso  ,(name+"Mu_hcalIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_hoIso").c_str()  ,Mu_hoIso  ,(name+"Mu_hoIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_ecalVetoIso").c_str() ,Mu_ecalVetoIso ,(name+"Mu_ecalVetoIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_hcalVetoIso").c_str() ,Mu_hcalVetoIso ,(name+"Mu_hcalVetoIso["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03chargedhadron").c_str()	  ,Mu_pfisor03chargedhadron	 ,(name+"Mu_pfisor03chargedhadron["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03chargedparticle").c_str()   ,Mu_pfisor03chargedparticle   ,(name+"Mu_pfisor03chargedparticle["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03neutralhadron").c_str()       ,Mu_pfisor03neutralhadron       ,(name+"Mu_pfisor03neutralhadron["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03photon").c_str()      ,Mu_pfisor03photon      ,(name+"Mu_pfisor03photon["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03neutralhadronht").c_str()      ,Mu_pfisor03neutralhadronht      ,(name+"Mu_pfisor03neutralhadronht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03neutralhadronht").c_str()    ,Mu_pfisor03neutralhadronht    ,(name+"Mu_pfisor03neutralhadronht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03photonht").c_str()	  ,Mu_pfisor03photonht	 ,(name+"Mu_pfisor03photonht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor03pu").c_str()	  ,Mu_pfisor03pu	 ,(name+"Mu_pfisor03pu["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04chargedhadron").c_str()	  ,Mu_pfisor04chargedhadron	 ,(name+"Mu_pfisor04chargedhadron["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04chargedparticle").c_str()   ,Mu_pfisor04chargedparticle   ,(name+"Mu_pfisor04chargedparticle["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04neutralhadron").c_str()       ,Mu_pfisor04neutralhadron       ,(name+"Mu_pfisor04neutralhadron["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04photon").c_str()      ,Mu_pfisor04photon      ,(name+"Mu_pfisor04photon["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04neutralhadronht").c_str()      ,Mu_pfisor04neutralhadronht      ,(name+"Mu_pfisor04neutralhadronht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04neutralhadronht").c_str()    ,Mu_pfisor04neutralhadronht    ,(name+"Mu_pfisor04neutralhadronht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04photonht").c_str()	  ,Mu_pfisor04photonht	 ,(name+"Mu_pfisor04photonht["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_pfisor04pu").c_str()	  ,Mu_pfisor04pu	 ,(name+"Mu_pfisor04pu["+name+"nMu]/F").c_str());
      //---------------------------
      // Pat Mu ID Variables
      //---------------------------
      tree->Branch((name+"Mu_isPF").c_str() ,Mu_isPF ,(name+"Mu_isPF["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_isGlobal").c_str()    ,Mu_isGlobal	 ,(name+"Mu_isGlobal["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_isTracker").c_str()       ,Mu_isTracker       ,(name+"Mu_isTracker["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_isGood").c_str()  ,Mu_isGood  ,(name+"Mu_isGood["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_isHighPt").c_str()     ,Mu_isHighPt     ,(name+"Mu_isHighPt["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_nTrackLayers").c_str()    ,Mu_nTrackLayers    ,(name+"Mu_nTrackLayers["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_nPixelLayers").c_str()   ,Mu_nPixelLayers   ,(name+"Mu_nPixelLayers["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_nPixelHits").c_str()    ,Mu_nPixelHits    ,(name+"Mu_nPixelHits["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_nValidHits").c_str() ,Mu_nValidHits ,(name+"Mu_nValidHits["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_nMatchedStations").c_str()      ,Mu_nMatchedStations       ,(name+"Mu_nMatchedStations["+name+"nMu]/I").c_str());
      tree->Branch((name+"Mu_innerTrack_normChi2").c_str()          ,Mu_innerTrack_normChi2           ,(name+"Mu_innerTrack_normChi2["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_innerTrack_dxyVertPos").c_str()         ,Mu_innerTrack_dxyVertPos          ,(name+"Mu_innerTrack_dxyVertPos["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_innerTrack_dzVertPos").c_str()         ,Mu_innerTrack_dzVertPos          ,(name+"Mu_innerTrack_dzVertPos["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_bestTrack_dxyVertPos").c_str()       ,Mu_bestTrack_dxyVertPos        ,(name+"Mu_bestTrack_dxyVertPos["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_bestTrack_dzVertPos").c_str()       ,Mu_bestTrack_dzVertPos        ,(name+"Mu_bestTrack_dzVertPos["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_globalTrack_normChi2").c_str()      ,Mu_globalTrack_normChi2       ,(name+"Mu_globalTrack_normChi2["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_IP3D").c_str()      ,Mu_IP3D       ,(name+"Mu_IP3D["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_IP2D").c_str()      ,Mu_IP2D       ,(name+"Mu_IP2D["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_IP3Der").c_str()      ,Mu_IP3Der       ,(name+"Mu_IP3Der["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_IP2Der").c_str()      ,Mu_IP2Der       ,(name+"Mu_IP2Der["+name+"nMu]/F").c_str());
      //---------------------------
      // Pat Mu Basic Variables
      //---------------------------
      tree->Branch((name+"Mu_pt").c_str() ,Mu_pt ,(name+"Mu_pt["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_phi").c_str() ,Mu_phi ,(name+"Mu_phi["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_eta").c_str() ,Mu_eta ,(name+"Mu_eta["+name+"nMu]/F").c_str());
      tree->Branch((name+"Mu_mass").c_str() ,Mu_mass ,(name+"Mu_mass["+name+"nMu]/F").c_str());
      //----------------------------
      // MC Truth Information
      //----------------------------
      tree->Branch((name+"nGenPart").c_str()         ,&nGenPart        ,(name+"nGenPart/I").c_str());
      tree->Branch((name+"GenPart_pt").c_str() ,GenPart_pt ,(name+"GenPart_pt["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_phi").c_str() ,GenPart_phi ,(name+"GenPart_phi["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_eta").c_str() ,GenPart_eta ,(name+"GenPart_eta["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_mass").c_str() ,GenPart_mass ,(name+"GenPart_mass["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_mother").c_str() ,GenPart_mother ,(name+"GenPart_mother["+name+"nGenPart]/I").c_str());
      tree->Branch((name+"GenPart_pdgid").c_str() ,GenPart_pdgid ,(name+"GenPart_pdgid["+name+"nGenPart]/I").c_str());
      tree->Branch((name+"GenPart_status").c_str() ,GenPart_status ,(name+"GenPart_status["+name+"nGenPart]/I").c_str());
      tree->Branch((name+"GenPart_vertX").c_str() ,GenPart_vertX ,(name+"GenPart_vertX["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_vertY").c_str() ,GenPart_vertY ,(name+"GenPart_vertY["+name+"nGenPart]/F").c_str());
      tree->Branch((name+"GenPart_vertZ").c_str() ,GenPart_vertZ ,(name+"GenPart_vertZ["+name+"nGenPart]/F").c_str());
    }



    //------------------------------------------------------------------------------------------------------------------

    void ReadTree(TTree *tree, std::string name="") {
      if (name!="") name += ".";
      
      //--------------------------------------
      // Pat Mu Isolation Variables
      //--------------------------------------
      tree->SetBranchAddress((name+"nMu").c_str()         ,&nMu        ) ;
      tree->SetBranchAddress((name+"Mu_trkIso").c_str()   ,Mu_trkIso   ) ;
      tree->SetBranchAddress((name+"Mu_trackerIsoSumPT").c_str()   ,Mu_trackerIsoSumPT   ) ;
      tree->SetBranchAddress((name+"Mu_ecalIso").c_str()   ,Mu_ecalIso   ) ;
      tree->SetBranchAddress((name+"Mu_hcalIso").c_str()  ,Mu_hcalIso  ) ;
      tree->SetBranchAddress((name+"Mu_hoIso").c_str()  ,Mu_hoIso  ) ;
      tree->SetBranchAddress((name+"Mu_ecalVetoIso").c_str() ,Mu_ecalVetoIso ) ;
      tree->SetBranchAddress((name+"Mu_hcalVetoIso").c_str() ,Mu_hcalVetoIso ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03chargedhadron").c_str()     ,Mu_pfisor03chargedhadron     ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03chargedparticle").c_str()   ,Mu_pfisor03chargedparticle   ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03neutralhadron").c_str()       ,Mu_pfisor03neutralhadron       ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03photon").c_str()      ,Mu_pfisor03photon      ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03neutralhadronht").c_str()      ,Mu_pfisor03neutralhadronht      ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03photonht").c_str()    ,Mu_pfisor03photonht    ) ;
      tree->SetBranchAddress((name+"Mu_pfisor03pu").c_str()	    ,Mu_pfisor03pu	   ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04chargedhadron").c_str()     ,Mu_pfisor04chargedhadron     ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04chargedparticle").c_str()   ,Mu_pfisor04chargedparticle   ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04neutralhadron").c_str()       ,Mu_pfisor04neutralhadron       ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04photon").c_str()      ,Mu_pfisor04photon      ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04neutralhadronht").c_str()      ,Mu_pfisor04neutralhadronht      ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04photonht").c_str()    ,Mu_pfisor04photonht    ) ;
      tree->SetBranchAddress((name+"Mu_pfisor04pu").c_str()	    ,Mu_pfisor04pu	   ) ;
      //-----------------------------------
      // Pat Mu ID Variables
      //-----------------------------------
      tree->SetBranchAddress((name+"Mu_isPF").c_str()     ,Mu_isPF     ) ;
      tree->SetBranchAddress((name+"Mu_isGlobal").c_str() ,Mu_isGlobal ) ;
      tree->SetBranchAddress((name+"Mu_isTracker").c_str()    ,Mu_isTracker    ) ;
      tree->SetBranchAddress((name+"Mu_isGood").c_str()       ,Mu_isGood       ) ;
      tree->SetBranchAddress((name+"Mu_isHighPt").c_str()  ,Mu_isHighPt  ) ;
      tree->SetBranchAddress((name+"Mu_nTrackLayers").c_str()     ,Mu_nTrackLayers     ) ;
      tree->SetBranchAddress((name+"Mu_nPixelLayers").c_str()    ,Mu_nPixelLayers    ) ;
      tree->SetBranchAddress((name+"Mu_nPixelHits").c_str()   ,Mu_nPixelHits   ) ;
      tree->SetBranchAddress((name+"Mu_nValidHits").c_str()    ,Mu_nValidHits    ) ;
      tree->SetBranchAddress((name+"Mu_nMatchedStations").c_str() ,Mu_nMatchedStations ) ;
      tree->SetBranchAddress((name+"Mu_innerTrack_normChi2").c_str()            ,Mu_innerTrack_normChi2            ) ;
      tree->SetBranchAddress((name+"Mu_innerTrack_dxyVertPos").c_str()      ,Mu_innerTrack_dxyVertPos       ) ;
      tree->SetBranchAddress((name+"Mu_innerTrack_dzVertPos").c_str()          ,Mu_innerTrack_dzVertPos           ) ;
      tree->SetBranchAddress((name+"Mu_innerTrack_dxyVertPos").c_str()          ,Mu_innerTrack_dxyVertPos           ) ;
      tree->SetBranchAddress((name+"Mu_globalTrack_normChi2").c_str()         ,Mu_globalTrack_normChi2          ) ;
      tree->SetBranchAddress((name+"Mu_IP3D").c_str()         ,Mu_IP3D          ) ;
      tree->SetBranchAddress((name+"Mu_IP2D").c_str()         ,Mu_IP2D          ) ;
      tree->SetBranchAddress((name+"Mu_IP3Der").c_str()         ,Mu_IP3Der          ) ;
      tree->SetBranchAddress((name+"Mu_IP2Der").c_str()         ,Mu_IP2Der          ) ; 
      //-----------------------------------
      // Pat Mu Basic Variables
      //-----------------------------------
      tree->SetBranchAddress((name+"Mu_pt").c_str()         ,Mu_pt          ) ;
      tree->SetBranchAddress((name+"Mu_eta").c_str()         ,Mu_eta          ) ;
      tree->SetBranchAddress((name+"Mu_phi").c_str()         ,Mu_phi          ) ;
      tree->SetBranchAddress((name+"Mu_mass").c_str()         ,Mu_mass          ) ;
      //-----------------------------------
      // MC Truth Information
      //----------------------------------
      tree->SetBranchAddress((name+"nGenPart").c_str()         ,&nGenPart        ) ;
      tree->SetBranchAddress((name+"GenPart_pt").c_str()         ,GenPart_pt          ) ;
      tree->SetBranchAddress((name+"GenPart_phi").c_str()         ,GenPart_phi          ) ;
      tree->SetBranchAddress((name+"GenPart_eta").c_str()         ,GenPart_eta          ) ;
      tree->SetBranchAddress((name+"GenPart_mother").c_str()         ,GenPart_mother          ) ;
      tree->SetBranchAddress((name+"GenPart_mass").c_str()         ,GenPart_mass          ) ;
      tree->SetBranchAddress((name+"GenPart_pdgid").c_str()         ,GenPart_pdgid          ) ;
      tree->SetBranchAddress((name+"GenPart_status").c_str()         ,GenPart_status          ) ;
      tree->SetBranchAddress((name+"GenPart_vertX").c_str()         ,GenPart_vertX          ) ;
      tree->SetBranchAddress((name+"GenPart_vertY").c_str()         ,GenPart_vertY          ) ;
      tree->SetBranchAddress((name+"GenPart_vertZ").c_str()         ,GenPart_vertZ          ) ;

    }

};

#endif

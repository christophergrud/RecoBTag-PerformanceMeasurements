import FWCore.ParameterSet.Config as cms

process = cms.Process("testJET")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.load("FWCore.MessageService.MessageLogger_cfi")

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(5)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
        #'/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7C-v1/00000/008BD264-1526-E211-897A-00266CFFA7BC.root'
        'file:/cms/data23/grud/CMSSW_5_3_18/src/muonHiggs/res/TestHiggs_py_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_RECO_100_1_F2L.root' 
   )
)

process.printList = cms.EDAnalyzer("ParticleListDrawer",
    src = cms.InputTag("genParticles"),
    maxEventsToPrint = cms.untracked.int32(1)
)
#-------------------------------------------------------------------------

process.p = cms.Path(
    process.printList
)

process.MessageLogger.destinations = cms.untracked.vstring('cout','cerr')
#process.MessageLogger.cout = cms.PSet(
#    threshold = cms.untracked.string('ERROR')
#)


###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
import string

options = VarParsing ('python')

options.register('runOnData', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run this on real data"
)

## Make sure correct global tags are used (please refer to https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions)

options.register('mcGlobalTag', 'START53_V27',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "MC global tag"
)
options.register('dataGlobalTag', 'FT53_V21A_AN6',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Data global tag"
)
options.register('outFilename', 'outfile',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)
options.register('reportEvery', 10,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=10)"
)
options.register('wantSummary', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)
options.register('usePFchs', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Use PFchs"
)
options.register('doJTA', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run jet-track association"
)
options.register('useExplicitJTA', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Use explicit jet-track association"
)
options.register('doBTagging', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run b tagging"
)
## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 10000)

options.parseArguments()

print "Running on data: %s"%('True' if options.runOnData else 'False')
print "Using PFchs: %s"%('True' if options.usePFchs else 'False')

## Global tag
globalTag = options.mcGlobalTag
if options.runOnData:
    globalTag = options.dataGlobalTag

## Jet energy corrections
inputJetCorrLabelAK5 = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
inputJetCorrLabelAK7 = ('AK7PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

if not options.usePFchs:
    inputJetCorrLabelAK5 = ('AK5PF', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    inputJetCorrLabelAK7 = ('AK7PF', ['L1FastJet', 'L2Relative', 'L3Absolute'])

if options.runOnData:
    inputJetCorrLabelAK5[1].append('L2L3Residual')
    inputJetCorrLabelAK7[1].append('L2L3Residual')

## b tagging
bTagInfos = ['impactParameterTagInfos','secondaryVertexTagInfos','inclusiveSecondaryVertexFinderTagInfos'
             ,'softMuonTagInfos','secondaryVertexNegativeTagInfos']
             #,'inclusiveSecondaryVertexFinderFilteredTagInfos']
bTagDiscriminators = ['jetProbabilityBJetTags','combinedSecondaryVertexBJetTags'
                      #,'trackCountingHighPurBJetTags','trackCountingHighEffBJetTags','jetBProbabilityBJetTags'
                      #,'simpleSecondaryVertexHighPurBJetTags','simpleSecondaryVertexHighEffBJetTags'
                      ,'combinedInclusiveSecondaryVertexBJetTags']
                      #,'simpleInclusiveSecondaryVertexHighEffBJetTags','simpleInclusiveSecondaryVertexHighPurBJetTags'
                      #,'doubleSecondaryVertexHighEffBJetTags']

import FWCore.ParameterSet.Config as cms

process = cms.Process("PF2PAT")

## MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
############## IMPORTANT ########################################
# If you run over many samples and you save the log, remember to reduce
# the size of the output by prescaling the report of the event number
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.cerr.default.limit = 10
#################################################################

## Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = globalTag + '::All'

# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src = cms.InputTag("genParticles"),
                                            select = cms.vstring(
                                                "keep status = 3"
                                                ,"++keep (abs(pdgId) = 13)"
                                                ,"++keep (abs(pdgId) = 15)"
                                                )
                                            )

## Events to process
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

## Options and Output Report
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(options.wantSummary) )

#-------------------------------------
## Input files
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # /TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/Summer12_DR53X-PU_S10_START53_V7C-v1/AODSIM
       # '/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7C-v1/00000/008BD264-1526-E211-897A-00266CFFA7BC.root'
#  	'file:/cms/se/phedex/store/mc/Summer12_DR53X/BprimeBprimeToBHBHinc_M-1000_TuneZ2star_8TeV-madgraph/AODSIM/PU_S10_START53_V7C-v1/10000/024BEF94-E93D-E211-BB47-0030487F16F7.root' 
#        'file:/cms/data23/grud/CMSSW_5_3_9/src/test/bHiggs/res/TestHiggs_py_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_RECO_55_1_a7T.root'
#         'file:/cms/data23/grud/CMSSW_5_3_18/src/TestHiggs_py_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_RECO.root'
#       'file:/cms/data23/grud/CMSSW_5_3_18/src/bHiggs/res/TestHiggs_py_GEN_SIM_DIGI_L1_DIGI2RAW_RAW2DIGI_RECO_99_1_u5k.root'
#        'file:/cms/data23/grud/CMSSW_5_3_18/src/step2_DIGI_L1_DIGI2RAW_RAW2DIGI_RECO.root'
#	'/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_100_1_gKP.root'
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_100_1_gKP.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_10_1_01a.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_11_1_0JQ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_12_1_B9r.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_13_1_1K9.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_14_1_wsg.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_15_1_Ddl.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_16_1_9zf.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_17_1_cXK.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_18_1_V8Q.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_19_1_6zJ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_1_1_52e.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_20_1_5LG.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_21_1_02J.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_22_1_dBC.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_23_1_wVN.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_24_1_BGZ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_25_1_lR9.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_26_1_Ok3.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_27_1_lBD.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_28_1_8eB.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_29_1_t5u.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_2_1_xdj.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_30_1_XYt.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_31_1_7Ze.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_32_1_k5Y.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_33_1_tEm.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_34_1_WnG.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_35_1_ePU.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_36_1_eDC.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_37_1_b2A.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_38_1_i8C.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_39_1_OA2.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_3_1_Y4c.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_40_1_SVO.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_41_1_0yK.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_42_1_Cg5.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_43_1_NBp.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_44_1_qpT.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_45_1_6UV.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_46_1_TdE.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_47_1_Wap.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_48_1_hTR.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_49_1_Dqr.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_4_1_Gib.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_50_1_K3h.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_51_1_8hZ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_52_1_hnD.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_53_1_byF.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_54_1_W5l.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_55_1_n0C.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_56_1_6jF.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_57_1_rex.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_58_1_OhJ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_59_1_7vA.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_5_1_cRp.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_60_1_yoS.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_61_1_1kC.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_62_1_hMy.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_63_1_znO.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_64_1_Byw.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_65_1_IND.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_66_1_7TA.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_67_1_M3o.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_68_1_v0c.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_69_1_h6B.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_6_1_jqB.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_70_1_UOv.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_71_1_6kK.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_72_1_FQQ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_73_1_uqX.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_74_1_aC8.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_75_1_K1J.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_76_1_uq5.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_77_1_0KB.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_78_1_wBk.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_79_1_L6z.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_7_1_sT9.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_80_1_X5a.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_81_1_BnT.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_82_1_umo.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_83_1_D3M.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_84_1_0yn.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_85_1_LMo.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_86_1_gau.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_87_1_RQb.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_88_1_eEg.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_89_1_qvZ.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_8_1_1wF.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_90_1_QNx.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_91_1_eZz.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_92_1_v14.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_93_1_DQM.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_94_1_ecC.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_95_1_nmN.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_96_1_DA2.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_97_1_k8y.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_98_1_28v.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_99_1_Mbe.root',
    '/store/user/cgrud/HiggsTo4Mu_M-125-10_TuneZ2star_8TeV-pythia6/Summer12_DR53X-PU_S10_START53_V27/220d40fbdddd6cac91a1e3c002f91223/STEP2_RAW2DIGI_L1Reco_RECO_VALIDATION_DQM_PU_9_1_5Nm.root'

  )
)

if options.runOnData:
    process.source.fileNames = [
        # /SingleMu/Run2012D-22Jan2013-v1/AOD
        '/store/data/Run2012D/SingleMu/AOD/22Jan2013-v1/10000/0449388F-D2A7-E211-BEED-E0CB4E55363D.root'
    ]

#-------------------------------------
outFilename = string.replace(options.outFilename,'.root','') + '_mc.root'
if options.runOnData :
    outFilename = string.replace(options.outFilename,'.root','') + '_data.root'

## Output file
process.TFileService = cms.Service("TFileService",
   fileName = cms.string(outFilename)
)
#-------------------------------------
## Standard PAT Configuration File
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Configure PAT to use PF2PAT instead of AOD sources
## this function will modify the PAT sequences.
from PhysicsTools.PatAlgos.tools.pfTools import *

## Output Module Configuration (expects a path 'p')
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string("test.root"),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    outputCommands = cms.untracked.vstring('drop *', *patEventContent)
)

postfix = "PFlow"
jetAlgo="AK5"
usePF2PAT(process,runPF2PAT=True, jetAlgo=jetAlgo, runOnMC=not options.runOnData, postfix=postfix,
          jetCorrections=inputJetCorrLabelAK5, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'))

## Top projections in PF2PAT
getattr(process,"pfPileUp"+postfix).checkClosestZVertex = False
getattr(process,"pfNoPileUp"+postfix).enable = options.usePFchs
getattr(process,"pfNoMuon"+postfix).enable = True
getattr(process,"pfNoElectron"+postfix).enable = True
getattr(process,"pfNoTau"+postfix).enable = False
getattr(process,"pfNoJet"+postfix).enable = True

#-------------------------------------
## CA8 jets (Gen and Reco)
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag("genParticlesForJetsNoNu")
)
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsCHS = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = getattr(process,"pfJets"+postfix).src,
    srcPVs = getattr(process,"pfJets"+postfix).srcPVs,
    doAreaFastjet = getattr(process,"pfJets"+postfix).doAreaFastjet,
    jetPtMin = cms.double(20.)
)

## CA8 filtered jets (Gen and Reco) (each module produces two jet collections, fat jets and subjets)
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNuFiltered = ca4GenJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag("genParticlesForJetsNoNu"),
    useFiltering = cms.bool(True),
    nFilt = cms.int32(3),
    rFilt = cms.double(0.3),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
process.ca8PFJetsCHSFiltered = ak5PFJetsFiltered.clone(
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    src = getattr(process,"pfJets"+postfix).src,
    srcPVs = getattr(process,"pfJets"+postfix).srcPVs,
    doAreaFastjet = getattr(process,"pfJets"+postfix).doAreaFastjet,
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    jetPtMin = cms.double(20.)
)
## CA8 BDRS filtered jets (Gen and Reco) (each module produces two jet collections, fat jets and subjets)
## Compared to the above filtered jets, here dynamic filtering radius is used (as in arXiv:0802.2470)
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNuBDRSFiltered = ca4GenJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag("genParticlesForJetsNoNu"),
    useFiltering = cms.bool(True),
    useDynamicFiltering = cms.bool(True),
    nFilt = cms.int32(3),
    rFilt = cms.double(0.3),
    rFiltFactor = cms.double(0.5),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)
from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
process.ca8PFJetsCHSBDRSFiltered = ak5PFJetsFiltered.clone(
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    src = getattr(process,"pfJets"+postfix).src,
    srcPVs = getattr(process,"pfJets"+postfix).srcPVs,
    doAreaFastjet = getattr(process,"pfJets"+postfix).doAreaFastjet,
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    jetPtMin = cms.double(20.),
    useDynamicFiltering = cms.bool(True),
    rFiltFactor = cms.double(0.5)
)
## CA8 pruned jets (Gen and Reco) (each module produces two jet collections, fat jets and subjets)
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
process.ca8GenJetsNoNuPruned = ca4GenJets.clone(
    SubJetParameters,
    rParam = cms.double(0.8),
    src = cms.InputTag("genParticlesForJetsNoNu"),
    usePruning = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
process.ca8PFJetsCHSPruned = ak5PFJetsPruned.clone(
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    src = getattr(process,"pfJets"+postfix).src,
    srcPVs = getattr(process,"pfJets"+postfix).srcPVs,
    doAreaFastjet = getattr(process,"pfJets"+postfix).doAreaFastjet,
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    jetPtMin = cms.double(20.)
)
## CA8 jets with Kt subjets (Gen and Reco) (each module produces two jet collections, fat jets and subjets)
## Kt subjets produced using Kt-based pruning with very loose pruning cuts (pruning is effectively disabled)
from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
process.ca8GenJetsNoNuKtSubjets = ca4GenJets.clone(
    SubJetParameters.clone(
        zcut = cms.double(0.),
        rcut_factor = cms.double(9999.)
    ),
    rParam = cms.double(0.8),
    src = cms.InputTag("genParticlesForJetsNoNu"),
    usePruning = cms.bool(True),
    useKtPruning = cms.bool(True),
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets")
)
from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
process.ca8PFJetsCHSKtSubjets = ak5PFJetsPruned.clone(
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    src = getattr(process,"pfJets"+postfix).src,
    srcPVs = getattr(process,"pfJets"+postfix).srcPVs,
    doAreaFastjet = getattr(process,"pfJets"+postfix).doAreaFastjet,
    writeCompound = cms.bool(True),
    jetCollInstanceName=cms.string("SubJets"),
    jetPtMin = cms.double(20.),
    useKtPruning = cms.bool(True),
    zcut = cms.double(0.),
    rcut_factor = cms.double(9999.)
)

#-------------------------------------
## PATify the above jets
from PhysicsTools.PatAlgos.tools.jetTools import *
## Default AK5 jets (switching done to run only specified b-tag algorithms)
switchJetCollection(process,
    cms.InputTag("pfNoTau"+postfix),
    jetIdLabel='ak5',
    rParam = 0.5,
    useLegacyFlavour=False,
    doJTA=options.doJTA,
    doBTagging=options.doBTagging,
    btagInfo=bTagInfos,
    btagdiscriminators=bTagDiscriminators,
    jetCorrLabel = inputJetCorrLabelAK5,
    doType1MET   = False,
    genJetCollection = cms.InputTag("ak5GenJetsNoNu"),
    doJetID      = False,
    postfix = postfix
)
## CA8 jets
switchJetCollection(process,
    cms.InputTag('ca8PFJetsCHS'),
    jetIdLabel='ca8',
    rParam = 0.8,
    useLegacyFlavour=False,
    doJTA=options.doJTA,
    doBTagging=options.doBTagging,
    btagInfo=bTagInfos,
    btagdiscriminators=bTagDiscriminators,
    jetCorrLabel = inputJetCorrLabelAK5,
    doType1MET   = False,
    genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
    doJetID      = False,
)
### Filtered CA8 jets
#addJetCollection(
    #process,
    #cms.InputTag('ca8PFJetsCHSFiltered'),
    #'CA8','FilteredPFCHS',
    #getJetMCFlavour=False,
    #doJTA=False,
    #doBTagging=False,
    #btagInfo=bTagInfos,
    #btagdiscriminators=bTagDiscriminators,
    #jetCorrLabel=inputJetCorrLabelAK7,
    #doType1MET=False,
    #doL1Cleaning=False,
    #doL1Counters=False,
    #doJetID=False,
    #genJetCollection=cms.InputTag("ca8GenJetsNoNu")
#)
### Filtered subjets of CA8 jets
#addJetCollection(
    #process,
    #cms.InputTag('ca8PFJetsCHSFiltered','SubJets'),
    #'CA8', 'FilteredSubjetsPFCHS',
    #rParam = 0.8,
    #useLegacyFlavour=False,
    #doJTA=options.doJTA,
    #doBTagging=options.doBTagging,
    #btagInfo=bTagInfos,
    #btagdiscriminators=bTagDiscriminators,
    #jetCorrLabel=inputJetCorrLabelAK5,
    #doType1MET=False,
    #doL1Cleaning=False,
    #doL1Counters=False,
    #doJetID=False,
    #genJetCollection=cms.InputTag('ca8GenJetsNoNuFiltered','SubJets')
#)
### Pruned CA8 jets
#addJetCollection(
    #process,
    #cms.InputTag('ca8PFJetsCHSPruned'),
    #'CA8','PrunedPFCHS',
    #getJetMCFlavour=False,
    #doJTA=False,
    #doBTagging=False,
    #btagInfo=bTagInfos,
    #btagdiscriminators=bTagDiscriminators,
    #jetCorrLabel=inputJetCorrLabelAK7,
    #doType1MET=False,
    #doL1Cleaning=False,
    #doL1Counters=False,
    #doJetID=False,
    #genJetCollection=cms.InputTag("ca8GenJetsNoNu")
#)
### Pruned subjets of CA8 jets
#addJetCollection(
    #process,
    #cms.InputTag('ca8PFJetsCHSPruned','SubJets'),
    #'CA8', 'PrunedSubjetsPFCHS',
    #rParam = 0.8,
    #useLegacyFlavour=False,
    #doJTA=options.doJTA,
    #doBTagging=options.doBTagging,
    #btagInfo=bTagInfos,
    #btagdiscriminators=bTagDiscriminators,
    #jetCorrLabel=inputJetCorrLabelAK5,
    #doType1MET=False,
    #doL1Cleaning=False,
    #doL1Counters=False,
    #doJetID=False,
    #genJetCollection=cms.InputTag('ca8GenJetsNoNuPruned','SubJets')
#)

#-------------------------------------
## N-subjettiness

from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness

process.NjettinessCA8 = Njettiness.clone(
    src = cms.InputTag("ca8PFJetsCHS"),
    cone = cms.double(0.8)
)

process.patJets.userData.userFloats.src += ['NjettinessCA8:tau1','NjettinessCA8:tau2','NjettinessCA8:tau3']

#-------------------------------------
## Grooming ValueMaps

#from RecoJets.JetProducers.ca8PFJetsCHS_groomingValueMaps_cfi import ca8PFJetsCHSPrunedLinks

#process.ca8PFJetsCHSPrunedMass = ca8PFJetsCHSPrunedLinks.clone(
    #src = cms.InputTag("ca8PFJetsCHS"),
    #matched = cms.InputTag("ca8PFJetsCHSPruned"),
    #distMax = cms.double(0.8),
    #value = cms.string('mass')
#)

#process.ca8PFJetsCHSFilteredMass = ca8PFJetsCHSPrunedLinks.clone(
    #src = cms.InputTag("ca8PFJetsCHS"),
    #matched = cms.InputTag("ca8PFJetsCHSFiltered"),
    #distMax = cms.double(0.8),
    #value = cms.string('mass')
#)

#process.patJets.userData.userFloats.src += ['ca8PFJetsCHSPrunedMass','ca8PFJetsCHSFilteredMass']

#-------------------------------------
## Enable clustering-based jet-SV association for IVF vertices and AK5 jets
#process.inclusiveSecondaryVertexFinderTagInfosAODPFlow = process.inclusiveSecondaryVertexFinderTagInfosAODPFlow.clone(
    #useSVClustering = cms.bool(True),
    ##useSVMomentum   = cms.bool(True), # otherwise using SV flight direction
    #jetAlgorithm    = cms.string("AntiKt"),
    #rParam          = cms.double(0.5),
    #ghostRescaling  = cms.double(1e-18)
#)
## Enable clustering-based jet-SV association for IVF vertices and pruned subjets of CA8 jets
#process.inclusiveSecondaryVertexFinderTagInfosCA8PrunedSubjetsPFCHS = process.inclusiveSecondaryVertexFinderTagInfosCA8PrunedSubjetsPFCHS.clone(
    #useSVClustering = cms.bool(True),
    ##useSVMomentum   = cms.bool(True), # otherwise using SV flight direction
    #jetAlgorithm    = cms.string("CambridgeAachen"),
    #rParam          = cms.double(0.8),
    #ghostRescaling  = cms.double(1e-18),
    #fatJets         = cms.InputTag("ca8PFJetsCHS"),
    #groomedFatJets   = cms.InputTag("ca8PFJetsCHSPruned")
#)

#-------------------------------------
## New jet flavor still requires some cfg-level adjustments for subjets until it is better integrated into PAT
## Adjust the jet flavor for CA8 filtered subjets
#process.patJetFlavourAssociationCA8FilteredSubjetsPFCHS = process.patJetFlavourAssociation.clone(
    #groomedJets = cms.InputTag("ca8PFJetsCHSFiltered"),
    #subjets = cms.InputTag("ca8PFJetsCHSFiltered", "SubJets")
#)
#process.patJetsCA8FilteredSubjetsPFCHS.JetFlavourInfoSource = cms.InputTag("patJetFlavourAssociationCA8FilteredSubjetsPFCHS","SubJets")
### Adjust the jet flavor for CA8 pruned subjets
#process.patJetFlavourAssociationCA8PrunedSubjetsPFCHS = process.patJetFlavourAssociation.clone(
    #groomedJets = cms.InputTag("ca8PFJetsCHSPruned"),
    #subjets = cms.InputTag("ca8PFJetsCHSPruned", "SubJets")
#)
#process.patJetsCA8PrunedSubjetsPFCHS.JetFlavourInfoSource = cms.InputTag("patJetFlavourAssociationCA8PrunedSubjetsPFCHS","SubJets")

#-------------------------------------
## Establish references between PATified fat jets and subjets using the BoostedJetMerger
process.selectedPatJetsCA8FilteredPFCHSPacked = cms.EDProducer("BoostedJetMerger",
    jetSrc=cms.InputTag("selectedPatJetsCA8FilteredPFCHS"),
    subjetSrc=cms.InputTag("selectedPatJetsCA8FilteredSubjetsPFCHS")
)

process.selectedPatJetsCA8PrunedPFCHSPacked = cms.EDProducer("BoostedJetMerger",
    jetSrc=cms.InputTag("selectedPatJetsCA8PrunedPFCHS"),
    subjetSrc=cms.InputTag("selectedPatJetsCA8PrunedSubjetsPFCHS")
)

## Define BoostedJetMerger sequence
process.jetMergerSeq = cms.Sequence(
    #process.selectedPatJetsCA8FilteredPFCHSPacked
    #+ process.selectedPatJetsCA8PrunedPFCHSPacked
)

#-------------------------------------
from PhysicsTools.PatAlgos.tools.coreTools import *
## Remove taus from the PAT sequence
removeSpecificPATObjects(process,names=['Taus'],postfix=postfix)
## Keep only jets in the default sequence
removeAllPATObjectsBut(process, ['Jets','Muons','Electrons'])

## Remove MC matching when running over data
if options.runOnData:
    removeMCMatching( process, ['All'] )

#-------------------------------------
## Produce a collection of good primary vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter("PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone(
        minNdof = cms.double(4.0), # this is >= 4
        maxZ = cms.double(24.0),
        maxRho = cms.double(2.0)
    ),
    src = cms.InputTag('offlinePrimaryVertices')
)

## Good primary vertex event filter
process.primaryVertexFilter = cms.EDFilter('VertexSelector',
    src = cms.InputTag('offlinePrimaryVertices'),
    cut = cms.string('!isFake & ndof > 4 & abs(z) <= 24 & position.Rho <= 2'),
    filter = cms.bool(True)
)

#-------------------------------------
## Define your analyzer and/or ntuple maker
process.load("RecoBTag.PerformanceMeasurements.BTagAnalyzer_cff")
process.btagana.use_selected_tracks   = True  ## False if you want to run on all tracks : used for commissioning studies
process.btagana.useTrackHistory       = False ## Can only be used with GEN-SIM-RECODEBUG files
process.btagana.produceJetProbaTree   = True ## True if you want to keep track and SV info! : used for commissioning studies
process.btagana.producePtRelTemplate  = False  ## True for performance studies
process.btagana.primaryVertexColl     = cms.InputTag('goodOfflinePrimaryVertices')
process.btagana.Jets                  = cms.InputTag('selectedPatJets'+postfix)
process.btagana.patMuonCollectionName = cms.InputTag('selectedPatMuons')
process.btagana.use_ttbar_filter      = cms.bool(False)
process.btagana.triggerTable          = cms.InputTag('TriggerResults::RECO') # Data and MC

#-------------------------------------
## If using explicit jet-track association
if options.useExplicitJTA:
    from RecoJets.JetAssociationProducers.ak5JTA_cff import ak5JetTracksAssociatorExplicit
    for m in getattr(process,"patDefaultSequence"+postfix).moduleNames():
        if m.startswith('jetTracksAssociatorAtVertex'):
            print 'Switching ' + m + ' to explicit jet-track association'
            setattr( process, m, ak5JetTracksAssociatorExplicit.clone(jets = getattr(getattr(process,m),'jets')) )
    for m in getattr(process,"patDefaultSequence").moduleNames():
        if m.startswith('jetTracksAssociatorAtVertex'):
            print 'Switching ' + m + ' to explicit jet-track association'
            setattr( process, m, ak5JetTracksAssociatorExplicit.clone(jets = getattr(getattr(process,m),'jets')) )

#-------------------------------------
## Remove tau stuff that really shouldn't be there (probably a bug in PAT)
process.patDefaultSequence.remove(process.kt6PFJetsForRhoComputationVoronoi)
for m in getattr(process,"patDefaultSequence").moduleNames():
    if m.startswith('hpsPFTau'):
        getattr(process,"patDefaultSequence").remove(getattr(process,m))

process.patDefaultSequencePFlow.remove(process.kt6PFJetsForRhoComputationVoronoiPFlow)
for m in getattr(process,"patDefaultSequence"+postfix).moduleNames():
    if m.startswith('hpsPFTau'):
        getattr(process,"patDefaultSequence"+postfix).remove(getattr(process,m))
#-------------------------------------
## Define jet sequences
process.genJetSeq = cms.Sequence(
    process.ca8GenJetsNoNu
    #+ process.ca8GenJetsNoNuFiltered
    #+ process.ca8GenJetsNoNuBDRSFiltered
    #+ process.ca8GenJetsNoNuPruned
    #+ process.ca8GenJetsNoNuKtSubjets
)
process.jetSeq = cms.Sequence(
    (
    process.ca8PFJetsCHS
    #+ process.ca8PFJetsCHSFiltered
    #+ process.ca8PFJetsCHSBDRSFiltered
    #+ process.ca8PFJetsCHSPruned
    #+ process.ca8PFJetsCHSKtSubjets
    )
    * (
    process.NjettinessCA8
    #+ process.ca8PFJetsCHSFilteredMass
    #+ process.ca8PFJetsCHSPrunedMass
    )
)

if not options.runOnData:
    process.jetSeq = cms.Sequence( process.genJetSeq + process.jetSeq )

#-------------------------------------
## Adapt primary vertex collection
from PhysicsTools.PatAlgos.tools.pfTools import *
adaptPVs(process, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), postfix=postfix, sequence='patPF2PATSequence')
adaptPVs(process, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), postfix='', sequence='jetSeq')
adaptPVs(process, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), postfix='', sequence='patDefaultSequence')

#-------------------------------------
## Add TagInfos to PAT jets
patJets = ['patJets'+postfix]

for m in patJets:
    if hasattr(process,m):
        print "Switching 'addTagInfos' for " + m + " to 'True'"
        setattr( getattr(process,m), 'addTagInfos', cms.bool(True) )

#-------------------------------------
## Path definition
process.p = cms.Path(
    process.prunedGenParticles
    *process.primaryVertexFilter
    * process.goodOfflinePrimaryVertices
    * (
    getattr(process,"patPF2PATSequence"+postfix)
    + ( process.jetSeq * process.patDefaultSequence )
    )
    * process.jetMergerSeq
    * (
    process.btagana
    )
)

## Delete output module
del process.out

## Schedule definition
process.schedule = cms.Schedule(process.p)


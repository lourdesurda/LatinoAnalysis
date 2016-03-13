#!/usr/bin/env python

#import json
import sys
import os
import ROOT
import optparse



if __name__ == '__main__':
    print '''
--------------------------------------------------------------------------------------------------

  __ \                               \  |        _)                                       
  |   |   __|  _` | \ \  \   /        \ |  |   |  |   __|   _` |  __ \    __|   _ \   __| 
  |   |  |    (   |  \ \  \ /       |\  |  |   |  | \__ \  (   |  |   |  (      __/ \__ \ 
 ____/  _|   \__,_|   \_/\_/       _| \_| \__,_| _| ____/ \__,_| _|  _| \___| \___| ____/ 
                                                                                          
--------------------------------------------------------------------------------------------------
'''    

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)

    parser.add_option('--outputDirPlots' , dest='outputDirPlots' , help='output directory'                           , default='./')
    parser.add_option('--inputFile'      , dest='inputFile'      , help='input file with histograms'                 , default='input.root')
    parser.add_option('--nuisancesFile'  , dest='nuisancesFile'  , help='file with nuisances configurations'         , default=None )
    parser.add_option('--samplesFile'    , dest='samplesFile'    , help='file with samples'                          , default=None )
    parser.add_option('--cutName'        , dest='cutName'        , help='cut names'                                  , default=None )


    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print " inputFile =           ", opt.inputFile
    print " nuisancesFile =       ", opt.nuisancesFile
    print " samplesFile =         ", opt.samplesFile
    print " outputDirPlots =      ", opt.outputDirPlots
    print " cutName =             ", opt.cutName
    
    os.system ("mkdir " + opt.outputDirPlots + "/") 

    
    samples = {}
    if os.path.exists(opt.samplesFile) :
      handle = open(opt.samplesFile,'r')
      exec(handle)
      handle.close()

    nuisances = {}
    if os.path.exists(opt.nuisancesFile) :
      handle = open(opt.nuisancesFile,'r')
      exec(handle)
      handle.close()

    ROOTinputFile = ROOT.TFile.Open( opt.inputFile, 'READ')
       
    # loop over nuisances
    for sampleName, sample in samples.iteritems():
      nameNominal = 'histo_' + sampleName
      nbins = 100
      if nameNominal in ROOTinputFile.GetListOfKeys() :
        histoNominal = ROOTinputFile.Get(nameNominal)
        nbins = histoNominal.GetNbinsX()
      print " nbins = ", nbins
      
      for nuisanceName, nuisance in nuisances.iteritems(): 
        print " nuisanceName = ", nuisanceName
        #print " nuisance = ", nuisance
        if 'name' in nuisance.keys() :
          nameDown = 'histo_' + sampleName + '_CMS_' + (nuisance['name']) + 'Down'
          nameUp   = 'histo_' + sampleName + '_CMS_' + (nuisance['name']) + 'Up'
          
          if nameDown in ROOTinputFile.GetListOfKeys() :
            print ('root -b -q DrawNuisances.cxx\(\\\"' + opt.inputFile + '\\\",\\\"' + nameNominal + '\\\",\\\"' + nameUp + '\\\",\\\"' + nameDown + '\\\",\\\"' + opt.outputDirPlots + '\\\"\) ')
            os.system ('root -b -q DrawNuisances.cxx\(\\\"' + opt.inputFile + '\\\",\\\"' + nameNominal + '\\\",\\\"' + nameUp + '\\\",\\\"' + nameDown + '\\\",\\\"' + opt.outputDirPlots + '\\\"\) ')
        else :
          if nuisanceName == 'stat' : # 'stat' has a separate treatment, it's the MC/data statistics
            if 'samples' in nuisance.keys():
              if sampleName in nuisance['samples'].keys() :
                for iBin in range(1, nbins): # max number of bins
                  nameDown = 'histo_' + sampleName + '_CMS_' + opt.cutName + '_' + sampleName + '_ibin_' + str(iBin) + '_stat' + 'Down'
                  nameUp   = 'histo_' + sampleName + '_CMS_' + opt.cutName + '_' + sampleName + '_ibin_' + str(iBin) + '_stat' + 'Up'
                  # print " nameUp = ", nameUp
                  # e.g.  CMS_hww2l2v_13TeV_of1j_ggH_hww_ibin_1_stat
                  
                  if nameDown in ROOTinputFile.GetListOfKeys() :
                    print ('root -b -q DrawNuisances.cxx\(\\\"' + opt.inputFile + '\\\",\\\"' + nameNominal + '\\\",\\\"' + nameUp + '\\\",\\\"' + nameDown + '\\\",\\\"' + opt.outputDirPlots + '\\\"\) ')
                    os.system ('root -b -q DrawNuisances.cxx\(\\\"' + opt.inputFile + '\\\",\\\"' + nameNominal + '\\\",\\\"' + nameUp + '\\\",\\\"' + nameDown + '\\\",\\\"' + opt.outputDirPlots + '\\\"\) ')
         
                                         



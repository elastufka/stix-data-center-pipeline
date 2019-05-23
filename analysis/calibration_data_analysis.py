import pickle, gzip
import numpy as np
import math
import os
from pprint import pprint
#from matplotlib import pyplot as plt
from ROOT import TGraph, TFile,TCanvas,TH1F
from array import array 
from core import stix_parser
from core import stix_logger
import datetime
_stix_logger= stix_logger._stix_logger

raw_dir='GU/raw/'
l0_dir='GU/l0/'
l1_dir='GU/l1/'
proc_log='GU/log/processing.log'
ana_log='GU/log/calibration.log'


def graph2(x,y, title, xlabel, ylabel):
    n=len(x)
    g=TGraph(n,array('d',x),array('d',y))
    g.GetXaxis().SetTitle(xlabel)
    g.GetYaxis().SetTitle(ylabel)
    g.SetTitle(title)
    return g

def hist(k,y, title, xlabel, ylabel):
    n=len(y)
    total=sum(y)
    h2=TH1F("h%d"%k,"%s; %s; %s"%(title,xlabel,ylabel),n,0,n)
    for i,val in enumerate(y):
        for j in range(val):
            h2.Fill(i)
            #to correct the histogram wrong entries
        #h2.SetBinContent(i+1,val)
    h2.GetXaxis().SetTitle(xlabel)
    h2.GetYaxis().SetTitle(ylabel)
    h2.SetTitle(title)
    #h2.SetEntries(sum)

    return h2 

def search(name, data):
    return [element for element in data if element['name'] == name]

def get_calibration_spectra(packet):
    param=packet['parameters']

    calibration=search('NIX00159',param)[0]

    cal=calibration['children']
    nstruct=int(calibration['raw'][0])
    detectors=[int(item['raw'][0]) for item in cal if item['name']=='NIXD0155']
    pixels=[int(item['raw'][0]) for item in cal if item['name']=='NIXD0156']
    spectra=[[int(it['raw'][0]) for it in  item['children']] for item in cal if item['name']=='NIX00146']
    #kspectra=[item['children'] for item in cal if item['name']=='NIX00146']
    counts=[]
    for e in spectra:
        counts.append(sum(e))

    result=[]
    for i in range(nstruct):
        result.append({'detector':detectors[i],
            'pixel':pixels[i],
            'counts':counts[i],
            'spec':spectra[i]})
    return result





def analysis(file_in, file_out):
    alog=open(ana_log,'a+')
    alog.write('-'*20+'\n')
    now=datetime.datetime.now()
    alog.write(str(now)+'\n')
    alog.write(file_in+'\n')
    f=None
    if file_in.endswith('.pklz'):
        f=gzip.open(file_in,'rb')
    else:
        f=open(file_in,'rb')

    data=pickle.load(f)['packet']
    detector_id=[]
    triggers=[]
    print('Number of packets:')
    print(len(data))
    ip=1
    cc=TCanvas()
    fr=TFile(file_out,"recreate")
    h=TH1F("h","Triggers; Pixel #; Counts",12*32,0,12*32)
    for i, d in enumerate(data):
        results=get_calibration_spectra(d)
        for row in results:
            if row['counts']>0:
                alog.write('packet %d: %d events in Detector %d Pixel %d\n' %(i, row['counts'], row['detector'], row['pixel']))
                print('Detector %02d Pixel %02d: %0d events' %(row['detector'], row['pixel'],row['counts']))
                xlabel=('ADC channel')
                ylabel=('Counts')
                title=('Detector %d Pixel %d'%(row['detector'], row['pixel']))
                g=hist(ip, row['spec'],title,xlabel,ylabel)
                cc.cd()
                ip+=1
                g.Draw("hist")
                fr.cd()
                cc.Write(("c_d_{}_{}_p_{}").format(ip,row['detector'],row['pixel']))
                h.Fill(12*row['detector']+row['pixel'], row['counts'])
                     

    cc.cd()
    h.Draw("hist")
    cc.Write('triggers')
    #g.Write("trigger")
    fr.Close()


    


def main():
    print('opening log file...')
    log=open(proc_log,'r+')
    log_content=log.read()
    for f in os.listdir(raw_dir):
        if f.endswith(".dat"):
            raw_filename=(os.path.join(raw_dir, f))
            if raw_filename in log_content:
                print('Processed already: %s '%raw_filename)
                continue
            filename=os.path.splitext(f)[0]+'.pkl'
            l0_filename=os.path.join(l0_dir,filename)
            filename=os.path.splitext(f)[0]+'.root'
            l1_filename=os.path.join(l1_dir,filename)
            print('Parsing file %s -> %s'%( raw_filename, l0_filename))
            log.write(raw_filename+'\n')

            #stix_telemetry_parser.parse_stix_raw_file(raw_filename, 
            #    l0_filename, 54124, 'array')

            stix_logger._stix_logger.set_logger('log/process.log', 2)
            parser = stix_parser.StixTCTMParser()
            parser.parse_file(raw_filename, l0_filename, 54124, 'tree','binary', 'calibration run')
            analysis(l0_filename, l1_filename)


main()
#analysis('GU/l0/calibration_asw152_2.pkl','GU/l1/calibration_asw152_2.root')


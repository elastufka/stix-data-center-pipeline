#!/usr/bin/python3
# export request from db to json
#@Author: Hualin Xiao
#@Date:   Feb. 11, 2020

import sys
from pprint import pprint
from stix.core import stix_datetime
from datetime import datetime
import pymongo
import json


data_levels={'L0':0, 'L1':1,'L2':2,'L3':3,'Spectrogram':4, 'Aspect':5}

def get_uid(start_unix, level):
    start_datetime = stix_datetime.unix2datetime(start_unix)
    year = start_datetime.year
    month = start_datetime.month
    day = start_datetime.day
    hour = start_datetime.hour
    minute = start_datetime.minute
    request_id = (year & 0xF) << 28
    request_id |= (month & 0xF) << 24
    request_id |= (day & 0x1F) << 19
    request_id |= (hour & 0x1F) << 14
    request_id |= (minute & 0x3F) << 8
    request_id |= (level & 0xF) << 4
    return request_id

def form_aspect_request(start_unix, stop_unix,summing):
    start_obt = int(stix_datetime.unix2scet(start_unix))
    stop_obt = int(stix_datetime.unix2scet(stop_unix))
    return {"name":
                "AIXF422A",
                'actionTime':'00:02:00',
                "parameters": [[
                    "XF422A01",
                    start_obt,
                ], [
                    "XF422A02",
                    stop_obt,
                ], ["XF422A03", summing]]
            }


def form_bsd_request(start_unix,
                 level,
                 detector_mask,
                 tmin,
                 tmax,
                 tunit,
                 emin,
                 emax,
                 eunit,
                 pixel_mask=0xfff,
                 action_time='00:00:10'):
    uid = get_uid(start_unix, level)
    start_obt = int(stix_datetime.unix2scet(start_unix))
    num_detectors = sum([(detector_mask & (1 << i)) >> i
                         for i in range(0, 32)])
    num_pixels = sum([((pixel_mask & (1 << i)) >> i) for i in range(0, 12)])
    #print(num_detectors, num_pixels)
    T = tmax / tunit
    M = num_detectors
    P = num_pixels
    E = emax - emin + 1
    data_volume = 1.1 * T * (M * P * (E + 4) + 16)
    parameters = [
        ['PIX00076', uid],
        ['PIX00070', level],
        ['PIX00072', start_obt],
        ['PIX00073', 0],  #subseconds
        ['PIX00248', "0x%X" % detector_mask],
        ['PIX00071', 1],  #number of structure
        ['PIX00077', tmin],
        ['PIX00078', tmax],
        ['PIXX0079', tunit],
        ['PIX00200', emin],
        ['PIX00201', emax],
        ['PIX00202', eunit]
    ]
    return {
        'name': 'ZIXX3801',
        'actionTime': action_time,
        'uid': uid,
        'data_volume': data_volume,
        'parameters': parameters
    }

def form_mask_config_telecommands(detector_mask, pixel_mask):
    return [{
                "name":
                "AIXF414A",
                "parameters": [[
                    "XF414A01",
                    "424",
                ], [
                    "XF414A02",
                    "0",
                ], ["XF414A03", "0x%X" % detector_mask]]
            },
            {
                "name":
                "AIXF414A",
                "parameters": [[
                    "XF414A01",
                    "425",
                ], [
                    "XF414A02",
                    "0",
                ], ["XF414A03", "0x%X" % pixel_mask]]
            },
        ]


def main(_ids, json_filename, server='localhost', port=9000):
    try:
        connect = pymongo.MongoClient(server, port)
        db = self.connect["stix"]
        collection= db['user_data_request_forms']
    except Exception as e:
        print('can not connect to mongodb')
        return 

    requst_forms = list(collection.find(
            {'_id': {'$in':_ids}}))
    
    last_detector_mask=0
    last_pixel_mask=0
    total_volume=0

    with open(json_filename, 'w') as json_file:
        requests = { 'occurrences':  []  }
        for form in requst_forms:
            start_utc = form['start_utc']
            unix_t0 = stix_datetime.utc2unix(start_utc)
            unix = unix_t0 + i * dt
            level=data_levels[form['request_type']]
            TC={}
            if level==5:
                TC=form_aspect_request(unix_t0, unix_t0+dt, int(form['averaging']))
                requests['occurrences'].append(TC)
                
            else:
                mask_TCs=[]
                detector_mask =form['detector_mask']
                pixel_mask = form['pxiel_mask']
                dt = int(form['duration'])
                tbin=int(form['time_bin'])
                emin=int(form['emin'])
                emax=int(form['emax'])
                eunit=int(form['eunit'])
                if detector_mask!=last_detector_mask and pixel_mask!=last_pixel_mask:
                    mask_TCs=form_mask_config_telecommands(detector_mask, pixel_mask)
                    requests['occurrences'].extend(mask_TCs)
                
                TC = form_bsd_request(unix_t0, level, detector_mask, 0, dt * 10, tbin * 10, emin,
                                  emax, eunit+1, pixel_mask)
                requests['occurrences'].append(TC)
                total_volume += TC['data_volume']


                last_pixel_mask=pixel_mask
                last_detector_mask=detector_mask


        json_file.write(json.dumps(requests, indent=4))

        print('Operation requests have been written to ', json_filename)
        print('data volume: {} KB ({} MB)'.format(total_volume / 1024.,
                                                      total_volume / (1024 * 1024)))



if __name__ == '__main__':
    if len(sys.argv)==5:
        ids=range(int(sys.argv[1]), int(sys.argv[2]))
        print(ids)
        main(ids, sys.argv[3], int(sys.argv[4]))
    else:
        print(' run start_id, stop_id, filename, port')

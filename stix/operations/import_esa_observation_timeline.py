import pymongo
import json

from stix.spice import stix_datetime as sdt
from pprint import pprint
connect = pymongo.MongoClient()
db = connect['stix']['events']

timeline_file_id='LTP06_v1'


def create_report(_id, subject, start, end, descr):
    report={
    "_id" : _id,
    "author" : "Hualin",
    "subject" :subject,
    "event_type" : "norminal",
    "start_utc" : start,
    "end_utc" : end,
    "description" : descr,
    "submit" : "",
    "creation_time" : sdt.now(),
    "timeline_file_id":timeline_file_id,
    "status" : 0,
    "hidden" : False
    }
    pprint(report)
    db.save(report)

name_map={
        'STIX_BASIC': 'STIX in nominal observation mode',
        'STIX_ANALYSIS':'Data request window',
        }


def import_timeline(filename):
    f=open(filename)
    data = json.load(f)
    observations=data['observations']
    try:
        next_id = db.find({}).sort(
            '_id', -1).limit(1)[0]['_id'] + 1
    except IndexError:
        next_id=0

    for obs in observations:
        name=obs['name']
        start=obs['startDate']
        end=obs['endDate']
        if name=='STIX_BASIC':
            continue
        vol=obs['numberParameters']['SCI_REQUEST_VOLUME']
        data_vol=f"Max science data volume: {vol['value']} {vol['unit']}"
        subject=name_map.get(name, name)

        create_report(next_id, subject, start, end, descr=data_vol)
        next_id+=1



    
filename='SSTX_observation_timeline_export_M06_V01.json'
import_timeline(filename)

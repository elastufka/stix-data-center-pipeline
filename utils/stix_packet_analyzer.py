#!/usr/bin/python3
#stix packet analyzer

import sys
sys.path.append('..')
sys.path.append('.')
from core import stix_parameter as stp

class StixPacketAnalyzer(object):
    def __init__(self):
        self._parameters = []
        self._parameter_vector={}
        self._header=None
    def merge_packets(self,packets, SPIDs, default_value_type='eng'):
        num = 0 
        for packet in packets:
            try:
                if int(packet['header']['SPID']) not in  SPIDs:
                    continue
            except ValueError:
                continue
            self.merge(packet, default_value_type)
            num+=1
        return num

    def merge(self, packet, default_value_type='eng'):
        parameters=packet['parameters']
        header=packet['header']
        if 'UTC' in header:
            if 'UTC' not in self._parameter_vector:
                self._parameter_vector['UTC']=[header['UTC']]
            else:
                self._parameter_vector['UTC'].append(header['UTC'])
        if 'time' not in self._parameter_vector:
            self._parameter_vector['time']=[header['time']]
        else:
            self._parameter_vector['time'].append(header['time'])

        for e in parameters:
            param = stp.StixParameter()
            param.clone(e)
            value=0
            name=param.name
            if 'NIXG' in name:
                continue
            value=param.get_raw_int()
            if default_value_type=='eng':
                if isinstance(param.eng, (float,int)):
                    value=param.eng

            if name in self._parameter_vector:
                self._parameter_vector[name].append(value)
            else:
                self._parameter_vector[name]=[value]
            if param.children:
                self.merge(param.children, default_value_type)

    def get_merged_parameters(self):
        return self._parameter_vector



    def load(self,packet):
        try:
            self._parameters =packet['parameters'] 
            self._header=packet['header']
        except KeyError:
            print('Unsupported format')
    def load_parameters(self,parameters):
        if isinstance(parameters,list):
            self._parameters = parameters
        else:
            print('Not a parameter list')

    def find(self, name_list,  parameters=None):
        if not isinstance(name_list,list):
            name_list=[name_list]

        if not parameters:
            parameters=self._parameters
        results ={name:[] for name in name_list }
        #results=dict()
        for e in parameters:
            param = stp.StixParameter()
            param.clone(e)
            if param.name in name_list:
                results[param.name].append(param.parameter)
            if param.children:
                children_results=self.find(name_list, param.children)
                for k,v in children_results:
                    if v:
                        results[k].extend(v)
        return results

    def get_raw(self, name_list, raw_type='int', parameters=None):
        if not isinstance(name_list,list):
            name_list=[name_list]
        params=self.find(name_list,parameters)
        #results=dict()
        results ={name:[] for name in name_list }
        for name in name_list:
            param=params[name]
            for p in param:
                pp=stp.StixParameter()
                pp.clone(p)
                value=-1
                try:
                    value=int(pp.raw[0])
                except (TypeError, IndexError,ValueError):
                    print('can not get raw value for {}: value: {} '.format(name,
                        str(pp.raw)))
                results[name].append(value)
        return results
    def get_eng(self, name_list, parameters=None):
        if not isinstance(name_list,list):
            name_list=[name_list]
        params=self.find(name_list,parameters)
        #results=dict()
        results ={name:[] for name in name_list }
        for name in name_list:
            param=params[name]
            for p in param:
                pp=stp.StixParameter()
                pp.clone(p)
                results[name].append(pp.eng)
        return results

    def find_child(self, parent_name, order=1):
        num_found=0
        for e in self._parameters:
            param = stp.StixParameter()
            param.clone(e)
            if param.name == parent_name:
                num_found+=1
                if num_found==order:
                    return param.children

        return None
    def get_child_raw(self,param_name, order=1):
        results=[]
        for child in self.get_child(param_name,order):
            param = stp.StixParameter()
            param.clone(e)
            results.append(param.raw)
        return results



    def find_all(self, pattern, plist=None,dtype='raw'):
        """
        pattern examples:
            pattern='NIX00159>NIX00146'
                return the values of all NIX00146 under NIX00159
            pattern='NIX00159>NIX00146>*'
                return the children's value of all NIX00146 

        """
        pnames=pattern.split('>')
        results=[]
        if not pnames:
            return []
        if not plist:
            plist=self._parameters
        try:
            pname=pnames.pop(0)
        except IndexError:
            return []
        for e in plist:
            param = stp.StixParameter()
            param.clone(e)
            if param.name == pname or pname=='*':
                if pnames:
                    ret=self.find_all('>'.join(pnames), param.children, dtype)
                    if ret:
                        results.append(ret)
                else:
                    result_ok=False
                    if dtype == 'eng':
                        if param.eng:
                            results.append(param.eng)
                            result_ok=True
                    if dtype == 'raw' or result_ok:
                        results.append(param.get_raw_int())

        return results




def analyzer():
    return StixPacketAnalyzer()




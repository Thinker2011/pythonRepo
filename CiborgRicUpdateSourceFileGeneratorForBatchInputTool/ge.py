import xml.etree.ElementTree as ET
from __builtin__ import classmethod
import json
import re

'''This python tool used for the sourcefiles needs for batchInput'''

class Ge():
    def __init__(self,filename):
        self.brokersStr =''
        self.tenorsStr=''
        tree = ET.parse(filename)
        root = tree.getroot()
        for schemas in root.findall('Schema'):
            if 'Brokers' == schemas.get('Type'):
                print schemas.get('DefaultValue')
                self.brokers=Ge._parseBrokerRawStr(schemas.get('DefaultValue'))
                
            if 'Tenors' == schemas.get('Type'):
                print schemas.get('DefaultValue')
                self.tenors=Ge._parseTenorRawStr(schemas.get('DefaultValue'))
            
            if 'IN_SUB_RIC' ==schemas.get('Key'):
                print schemas.get('DefaultValue')
                self.formatStr = Ge._parseFormat(schemas.get('DefaultValue'))
                
            if 'PRI_PRO_PREFIX_IN'== schemas.get('Key'):
                self.prefixStr = schemas.get('DefaultValue').encode('ascii')
            
        return None
    
    
    def generate(self,fielddict={'fid393':'1.0','fid275':'1.1'}):     
        fl = open('ge.xml','wb')
        fl.write('<file></file>')
        fl.close()
        tree=ET.parse('ge.xml')
        fileE=tree.getroot()
        for broker in self.brokers.items():
            for tenor in self.tenors:
                ricname = Ge._combineRicName(broker, tenor, self.prefixStr,self.formatStr)
                attrib=fielddict
                attrib.update({'name':ricname.encode('ascii')})
                ET.SubElement(fileE,'ric',attrib)
        tree.write('ge.xml')
        
    
    @classmethod
    def _parseBrokerRawStr(cls,str):
        return json.JSONDecoder().decode(str)
    
    @classmethod
    def _parseTenorRawStr(cls,str):
        return json.JSONDecoder().decode(str)
    
    @classmethod
    def _parseFormat(cls,str):
        return str
    
    @classmethod
    def _combineRicName(cls,broker,tenor,prefix,formatStr):    
        fs=formatStr.replace('<tenor>',tenor).replace('<broker>',broker[0]).replace('<broker.sid>',broker[1][u'SID'])
        fs = prefix + fs
        print fs
        return fs
        
                
            

    

def generate():
    fileName=raw_input('input filename:')
    gnt = Ge(fileName)
    gnt.generate()
    raw_input('finished')
    
    
if __name__ =='__main__':
    generate()
    
    
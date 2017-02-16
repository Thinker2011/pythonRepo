import xml.etree.ElementTree as ET
from __builtin__ import classmethod

class Ge():
    def __init__(self,filename):
        self.brokersStr =''
        self.tenorsStr=''
        tree = ET.parse(filename)
        root = tree.getroot()
        for schemas in root.findall('schema'):
            if 'Brokers' == schemas.get('Type'):
                self.brokers=Ge._parseBrokerRawStr(schemas.get('defaultValue'))
                
            if 'Tenors' == schemas.get('Type'):
                self.tenors=Ge._parseTenorRawStr(schemas.get('defaultValue'))
            
            if 'IN_SUB_RIC' ==schemas.get('Key'):
                self.formatStr = Ge._parseFormat(schemas.get('defaultValue'))
            
        return None
    
   
        
    
    def generate(self,fielddict={'field393':'1.0','field275':'1.0'}):     
        fl = open('ge.xml','wb')
        fl.write('<file></file>')
        fl.close()
        tree=ET.parse('ge.xml')
        fileE=tree.getroot()
        for broker in self.brokers:
            for tenor in self.tenors:
                ricname = Ge._combineRicName(broker, tenor, self.formatStr)
                attrib = {'name':ricname}.update(fielddict)
                ET.SubElement(fileE,'ric', attrib)
        tree.write('ge.xml')
        
    
    @classmethod
    def _parseBrokerRawStr(cls,str):
        
        return ['broker']
    
    @classmethod
    def _parseTenorRawStr(cls,str):
        return ['tenor']
    
    @classmethod
    def _parseFormat(cls,str):
        return 'OK'
    
    @classmethod
    def _combineRicName(cls,broker,tenor,formatStr):
        return 'hh'
    
if __name__ =='__main__':
    fileName=raw_input('input filename:')
    print fileName
    gnt = Ge(fileName)   
    gnt.generate()
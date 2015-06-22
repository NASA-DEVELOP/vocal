'''
Created on Jun 15, 2015

@author: nqian
'''
# import antigravity
import json

import ast
import Constants
from gui.Polygon import PolygonDrawer


def byteify(inp):
    if isinstance(inp, dict):
        return {byteify(key):byteify(value) for key,value in inp.iteritems()}
    elif isinstance(inp, list):
        return [byteify(element) for element in inp]
    elif isinstance(inp, unicode):
        return inp.encode('utf-8')
    else:
        return inp

class PolygonReader(object):
    '''
    Reads JSON files and transfers the data into PolygonDrawer objects
    '''

    # TODO: add exception handling
    def __init__(self, fileName="C:\\Users\\nqian\\Documents\\Carol.json"):
        '''
        Initializes attributes
        '''
        self.__fileName = fileName
        self.__data = {} 
        
    def setFileName(self, fileName):
        self.__fileName = fileName
        
    def readFromFileJSON(self):   
        with open(self.__fileName, 'r') as infile:
            data = json.load(infile)
#           test = json.dumps(data, sort_keys=True,
#                              indent=2, separators=(',', ': '))
#           print test
#           print data["Backscattered"]
#           print data["Depolarized"]
#           debug = yaml.safe_load(test)
#           print type(test)
        self.__data = data
        
    def readFromStrJSON(self, data):
        self.__data = json.loads(data)
        for plt in [x for x in self.__data if x in Constants.PLOTS]:
            for shape in self.__data[plt]:
                if "vertices" in self.__data[plt][shape]:
                    self.__data[plt][shape]["vertices"] = \
                        [[x[0],x[1]] for x in ast.literal_eval(self.__data[plt][shape]["vertices"]) if len(x) == 2]
                if "attributes" in self.__data[plt][shape]:
                    self.__data[plt][shape]["attributes"] = \
                        ast.literal_eval(self.__data[plt][shape]["attributes"])
    # TODO: add exception
    def packPolygonDrawer(self, polygonList, plotType, canvas, master):
        for shape in self.__data[plotType]:
            #print int(self.__data[plotType][shape]['id']) not in [x.getID() for x in polygonList]
            if int(self.__data[plotType][shape]['id']) in [x.getID() for x in polygonList]: continue
            color = self.__data[plotType][shape]['color']
            vertices = self.__data[plotType][shape]['vertices']
            attributes = self.__data[plotType][shape]['attributes']
            _id = self.__data[plotType][shape]['id']
            polygonList[-1].setID(_id)
            polygonList[-1].setColor(color)
            polygonList[-1].setVertices(vertices)
            polygonList[-1].setPlot(plotType)
            polygonList[-1].setAttributes(attributes)
            polygonList.append(PolygonDrawer(canvas, master))

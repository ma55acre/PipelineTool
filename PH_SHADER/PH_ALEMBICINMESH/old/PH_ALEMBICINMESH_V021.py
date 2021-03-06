# -*- encoding: utf-8 -*-
import sys
import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
from pymel.core.runtime import BakeNonDefHistory
listNodesAlemb=['']
#input and output
outAttr='outPolyMesh'
inAttr='inMesh'
outMesh='outMesh'

def _startTranfer():
    aNode = _selectNode()
    newGeo= mc.ls( sl=True )[0]
    if not aNode or newGeo:
        mc.warning('No estas haciendo algo bien.')
    _oldNodeTonewNode(aNode,newGeo)

def _oldNodeTonewNode(aNode,newGeo):
    #Si el nodo tiene un outPolyMesh se conectara
    if 'outPolyMesh' in mc.listAttr(aNode,readOnly=True):
        #diccionarios
        nodoDict = {}
        trfDicTrg = {}
        nodoDictConect = {}
        #arrays
        childrenMsh=[]
        childrenT=[]
        polyMeshNumber = []
        #cantidad de polymesh en nodo alembic
        polyMeshNumber = mc.getAttr(aNode+'.'+outAttr, size=True)
        #------------------#recorro el tamaño de conexiones en el polyMesh
        for i in range(polyMeshNumber):
            #guardo la conexion completa vieja donde se conecta el nodo
            if mc.listConnections(aNode+'.'+outAttr+str([i]),plugs=1,connections=True)!= None:
                nodoDictConect[i] = mc.listConnections(aNode+'.'+outAttr+str([i]),plugs=1)[0]
            else:
                nodoDictConect[i]= 'None'
            #si esta dentro de un grupo vamos por aca
            if 'Deformed' in nodoDictConect[i]:
                #si no tiene grupo el string se le agrega
                if not '|' in nodoDictConect[i]:
                    grp=mc.listRelatives(nodoDictConect[i].split('.')[0],allParents=True,fullPath=True)[0]
                    nodoDictConect[i]=grp+'|'+nodoDictConect[i]
            #-------------------#listamos el grupo a conectar
            if len(mc.ls( sl=True )) == 1:
                #Lista de nodos a lo que voy a conectar el alembic IMPORTANTE
                padreTgt= newGeo
                #childrenT = mc.listRelatives(padreTgt, path=True)
                childrenT = mc.listRelatives(padreTgt, fullPath=True,noIntermediate=True)
                for x in range(len(childrenT)):
                    #busco el shape
                    o=mc.listRelatives(childrenT[x],fullPath=True)
                    if mc.nodeType(str(o[0])) == 'mesh':
                        if '|' in o[0]:
                            o=o[0].split('|')[-1:]
                            trfDicTrg[childrenT[x]+'|'] = o[0]
                            childrenMsh.append(str(o[0]))
                        else:
                            childrenMsh.append(o[0])
                #------------------------
            for f in childrenT:
                #Conectamos
                for k, v in trfDicTrg.items():
                    if str(v) in nodoDictConect[i]:
                        if mc.isConnected(aNode+'.'+outAttr+str([i]),nodoDictConect[i]):
                            #nonDeformerHistoryNodes = [n for n in node.history(il=1) if not isinstance(n, pm.nodetypes.GeometryFilter)] 
                            desConects = mc.disconnectAttr(aNode+'.'+outAttr+str([i]),nodoDictConect[i])
                            print str(desConects)
                            conect = mc.connectAttr(aNode+'.'+outAttr+str([i]),k+v+'.'+inAttr,force=True)
                            print str(conect)
                        else:
                            print str(aNode+'.'+outAttr+str([i])) + ' no tiene conexion.'
    else:
        print 'El script por ahora solo contempla si el nodo tiene polyMesh'
    
def _selectToAlembic():
    selA, selB=mc.ls(sl=1)
    if sel == 2:
        BakeNonDefHistory()
        mc.connectAttr(str(selB)+'.outMesh',str(selA)+'.inMesh',force=True)
        BakeNonDefHistory()
    else:
        print 'Selecciona primero el mesh shader y luego el mesh alembic.'
        
def _initGui():
        #lista de camaras en scena
        NodesAlemb = mc.ls(type='AlembicNode')
        if NodesAlemb==[]:
            mc.warning('NO EXISTE NINGUN NODO DE ALEMBIC EN ESTE FILE')
        else:
            #ordeno listas
            NodesAlemb.sort()
            for i in NodesAlemb:
                mc.textScrollList(listNodesAlemb, edit=True, append=i)
            if len(mc.textScrollList(listNodesAlemb, q=True, allItems=True)):
                mc.textScrollList(listNodesAlemb, edit=True, selectIndexedItem=1)
def _selectNode():

    selectNode = mc.textScrollList(listNodesAlemb, q=True, selectItem=True)
    return selectNode[0]
    
def _refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    mc.textScrollList(listNodesAlemb, edit=True, removeAll=True)
    _initGui();

def _makeWindow():

    winName='PH_ALEMBICINMESH'
    version=' v0.5'
    if mc.window(winName, exists=True):
        mc.deleteUI(winName)
    mc.window( winName, title=winName+version, h=200 ,w=200,s=False,resizeToFitChildren=True )
    mc.columnLayout(adjustableColumn = True)
    mc.text('LISTA DE ALEMBIC EN ESCENA',align='center',h=20 )
    mc.textScrollList(listNodesAlemb, allowMultiSelection=False, selectCommand="_selectNode()")
    mc.rowLayout( numberOfColumns=2 )
    mc.text('''
        1) SELECCIONA EL NODO DE ALEMBIC
        2) SELECCIONA EL GRUPO DEL SHADER
        3) TRANFERIR ALEMBIC
        ''',align='left')
    mc.columnLayout(columnAttach=('left',50), rowSpacing=2)
    mc.button( label='REFRESH', command="_refreshGui()", bgc=(0.1,0.5,0.1))
    mc.button( label='TRANFER ALEMBIC', command="_startTranfer()", bgc=(0.1,0.5,0.1))
    mc.showWindow()
    #inicio la lista
    _initGui()
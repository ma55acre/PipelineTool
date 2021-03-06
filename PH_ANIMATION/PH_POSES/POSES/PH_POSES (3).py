#DOCK

import maya.cmds as mc
import json
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import maya.mel
from functools import partial

def saveJSONFile(dataBlock, filePath):
	outputFile = open(filePath, 'w')
	JSONData = json.dumps(dataBlock, sort_keys=True, indent=4)
	outputFile.write(JSONData)
	outputFile.close()
def loadJSONFile(filePath):
	inputFile = open(filePath, 'r')
	JSONData = json.load(inputFile)
	inputFile.close()
	return JSONData
def writeJSONFile(dataBlock, filePath):
	f = open(filePath, 'a')
	d = json.dumps(dataBlock, sort_keys=True, indent=4)
	f.write(d)
	f.close()
def guardarPose(nombreDePose=""):
	huesos = mc.ls (sl=1 , type="hikFKJoint")
	if huesos!=[]:
		poseHIK= {}
		for hueso in huesos:
			poseHIK[hueso.split(":")[-1]+".rx"] = mc.getAttr ( hueso+".rx" )
			poseHIK[hueso.split(":")[-1]+".ry"] = mc.getAttr ( hueso+".ry" )
			poseHIK[hueso.split(":")[-1]+".rz"] = mc.getAttr ( hueso+".rz" )
		dicJSON = loadJSONFile("D:\PH_SCRIPTS\PH_ANIMATION\PH_POSES\POSES\POSES_MANO.json") #cargo dic
		dicJSON[nombreDePose.upper()]= poseHIK #agrego pose nueva al dic
		saveJSONFile( dicJSON , "D:\PH_SCRIPTS\PH_ANIMATION\PH_POSES\POSES\POSES_MANO.json") #guardo el dic modificado
	else:
		mc.warning("NO HAY SELECCION.")
	guardaImagen(nombreDePose)

def cargaPose(poseRequerida,espejar=0):
    poseHIK = loadJSONFile("D:\PH_SCRIPTS\PH_ANIMATION\PH_POSES\POSES\POSES_MANO.json")[poseRequerida.upper()]
    nameSpaceSeleccionado = ""
    nameSpaceSplit = ( mc.ls(sl=1)[0] ).split(":")
    for i in range ( len(nameSpaceSplit)-1):
        nameSpaceSeleccionado = nameSpaceSeleccionado + nameSpaceSplit[i]+":"
    if not mc.objExists( nameSpaceSeleccionado+"Ctrl_Spine"):
        objetoParaCapturarRuta = mc.ls (nameSpaceSeleccionado+"*Ctrl_Spine")[0]
        nameSpaceSeleccionado = objetoParaCapturarRuta.split ('Ctrl')[0]
    if len(mc.ls (sl=1 , type="hikFKJoint"))!=len(mc.ls (sl=1)):
        #ALGUNOS JOINTS, ALGUNOS CUALQUIER OTRA COSA. ----> CARGA TODA LA POSE GUARDADA
        #"manocerrada","agarraMango","relax_1" poseRequerida="karate_patada"
        if espejar==0:
            for hueso in poseHIK.keys():
                mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+hueso[:-3].split(":")[-1] , a=1 )
        else:
            for hueso in poseHIK.keys():
                if "Left" in hueso:
                    print nameSpaceSeleccionado + (hueso[:-3]).replace("Left","Right").split(":")[-1]
                    mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+ (hueso[:-3]).replace("Left","Right").split(":")[-1] , a=1 )
                if "Right" in hueso:
                    mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+ (hueso[:-3]).replace("Right","Left").split(":")[-1] , a=1 )
    elif len ( mc.ls (sl=1 , type="hikFKJoint") ) == len( mc.ls (sl=1) ) :
        #TODAS LAS COSAS ELEGIDAS SON JOINTS. CARGO LA POSE FILTRANDO POR SELECCION.
        if espejar==0:
            for hueso in poseHIK.keys():
                print nameSpaceSeleccionado + hueso
                if nameSpaceSeleccionado + hueso.split(".")[0] in mc.ls(sl=1):
                    mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+hueso[:-3].split(":")[-1] , a=1 )
        else:
            for hueso in poseHIK.keys():
                if "Left" in hueso:
                    print nameSpaceSeleccionado+ (hueso[:-3]).replace("Left","Right").split(":")[-1]
                    mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+ (hueso[:-3]).replace("Left","Right").split(":")[-1] , a=1 )
                if "Right" in hueso:
                    mc.rotate ( poseHIK[ hueso[:-3].split(":")[-1] +".rx"] , poseHIK[hueso[:-3].split(":")[-1] +".ry"] , poseHIK[hueso[:-3].split(":")[-1] +".rz"]  , nameSpaceSeleccionado+ (hueso[:-3]).replace("Right","Left").split(":")[-1] , a=1 )

def guardaImagen(nombreDePose=""):
	global nombreDePoseGlobal
	nombreDePoseGlobal=nombreDePose
	mc.evalDeferred('resolucion=150')
	nombrePanel = mc.modelPanel(tearOff=True)
	nombreEditor = mc.modelPanel( nombrePanel , q=1 , modelEditor=1)
	mc.modelEditor (nombreEditor   , e =1 ,activeOnly=0,displayAppearance="smoothShaded",polymeshes=1,wos=0,
	 	nurbsSurfaces=1,planes=1,lights=0,cameras=0,controlVertices=0,grid=0,hulls=0,joints=0,
	 	ikHandles=0,nurbsCurves=0,deformers=0,dynamics=1,fluids=0,hairSystems=0,follicles=0,
	 	nCloths=1,nParticles=1,	nRigids=1,dynamicConstraints=0,locators=0,manipulators=0,dimensions=0,
	 	handles=0,pivots=1,textures=0,	strokes=0,pluginShapes=1,queryPluginObjects=1,	)
	mc.modelEditor (nombreEditor  , e =1 ,activeView=1 ,p='lay_1' , activeOnly=0,displayAppearance="smoothShaded",polymeshes=1,wos=0)
	mc.evalDeferred('view=apiUI.M3dView.active3dView()')
	mc.evalDeferred('imagen=api.MImage()')
	mc.evalDeferred('view.readColorBuffer (imagen,True)')
	mc.evalDeferred('imagen.resize (resolucion,resolucion,1)')
	mc.evalDeferred('imagen.writeToFile("D:/PH_SCRIPTS/ICONS/POSES/"+nombreDePoseGlobal+".png","png")')

def posesMain():
	if mc.window('posesUI',ex=1)==True:
		mc.deleteUI('posesUI')
	if mc.dockControl('dockPosesUI',ex=1)==True:
		mc.deleteUI('dockPosesUI')
	mc.window ('posesUI' , w=320 )
	mc.formLayout ( 'lay_1' , p='posesUI')
	creaLayout('lay_1')
	allowedAreas = ['right', 'left']
	mc.dockControl( 'dockPosesUI' , label= "POSES v1.1",area='left', content='posesUI', allowedArea=allowedAreas )

def creaLayout(parentL=""):
    posesEnM = mc.getFileList( folder="D:\PH_SCRIPTS\ICONS\POSES", filespec='*.png' )
    posesEnM.sort()
    indice=0
    lay0 = mc.columnLayout  ( p = parentL )
    lay1 = mc.rowColumnLayout  (  numberOfColumns=3 , p = lay0 )
    for i in range( len(posesEnM) ):
        mc.iconTextButton (style='iconOnly', image1 = 'D:\PH_SCRIPTS\ICONS\POSES\\' + posesEnM[i] ,width=150,height=150, c=partial (cargaPose,posesEnM[i][:-4]) , dcc= partial (cargaPose,posesEnM[i][:-4],1), ann=posesEnM[i][:-4].replace("_"," "))
    lay2 = mc.columnLayout  (  p = lay0 , bgc=[0.23,0.23,0.23])
    mc.text (p=lay2 , l="""Un click izquierdo asigna pose a mano izquierda. Doble click izquierdo asigna pose a mano derecha. \nDebido a que la mano derecha esta mal riggeada, el pulgar derecho lo van a ver raro.\n
	Si todo lo seleccionado es un 'hikFKJoint', carga solamente esos huesos de la pose.\nSi lo seleccionado no es 'hikFKJoint', carga la pose entera.""")
    mc.separator (p=lay2)
posesMain()

"""
guardaImagen(nombreDePose="lelo")
guardaImagen(nombreDePose="")
guardarPose(nombreDePose="karate_patada")

"""

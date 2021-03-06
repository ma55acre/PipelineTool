# -*- encoding: utf-8 -*-
import sys
import maya.cmds as mc
import maya.mel as mel
import pymel.core.runtime as pm
global camListBox
camListBox = ['x']
global camListTrf
camListTrf = ['']
global dupliname
dupliname = ['d']
global trfCams
trfCams=['f']
#Archivos mels de Gabo S
def sequence():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_CAMERASEQUENCER.mel"')
def importrig():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_IMPORTRIG.mel"')
    refreshGui()
def lockcams():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_LOCKCAMERAS.mel"')
def playBlastShot():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_PLABLASTSHOT.mel"')    
def lockcamsprop():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_LOCKCAMERASPROP.mel"')
def upRig():
    mel.eval('source "M:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_UPDATERIG.mel"')
    refreshGui()

########Mangager Camaras#########
#selecciona el objeto dentro de la lista de hijos del grupo seleccionado
def selectChanged():
    selectCam = mc.textScrollList(camListBox, q=True, selectItem=True)
    sel= mc.ls(selectCam[0])
    if len(sel) >= 2:
        mc.warning('HAY DOS OBJETOS CON EL MISMO NOMBRE OJO:' + str(sel)+'.\nPORFAVOR RENOMBRAR BIEN.')
    else:
        if 'CAM' in selectCam:
            selectCam = mc.listRelatives(selectCam[0],children=True, fullPath=True)
            mc.select(selectCam)
        if 'CNT' in selectCam:
            mc.select(selectCam)
        if 'TRF' in selectCam:
            mc.select(selectCam)
#actualiza la lista de hijos dentro del grupo seleccionado
def selectTrf():
    global trfCams
    mc.textScrollList(camListBox, edit=True, removeAll=True)
    selectCam = mc.textScrollList(camListTrf, q=True, selectItem=True)
    cameras = mc.listRelatives(selectCam[0],type='transform',allDescendents=True)
    excludeListA=['_SCAM','__SCAM','GRP','TRFShape','_HCNS','__HCNS','TRFSH','_SCAMF','_CNTSH','_SCAMF','_SCAMSH','__SCAMH','__SCAMSH']
    excludeListC=['parentConstraint','parentConstraint1','Frustum']
    if cameras!=[]:
        #filtro trf de camaras
        for x in excludeListA+excludeListC+trfCams:
            for item in cameras:
                if item.find(x) != -1:
                    cameras.remove(item)
    cameras.sort()
    for aCam in cameras:
        mc.textScrollList(camListBox, edit=True, append=aCam)
    if haveAnim(selectCam) ==1:
        buttonAnimOn()
    else:
        buttonAnimOff()
    mc.select(selectCam)
#borra la seleccion de la lista de grupo
def delSelected():
    selectCam = mc.textScrollList(camListTrf, q=True, selectItem=True)
    for sc in selectCam:
        if sc:
            mc.delete(str(sc))
            mc.warning('SE BORRO ' + str(sc))
        else:
            mc.warning('LO SIENTO NO PUDE BORRAR ' + str(sc))
    refreshGui()
#crea una camara comun

def newCam():
    mc.camera(name='C_RENOMBRAME_RENOMBRAME__CAM')
    refreshGui()
#Enfocar la camara camara
def camLook():
    selectLook = mc.textScrollList(camListBox, q=True, selectItem=True)
    if selectLook:
        if 'CAM' in selectLook:
            mc.select(selectLook)
            mc.lookThru(selectLook) # looks through the camera I specify
            #timeAnim()
            try:
                lookThroughSelectedCamera()
            except:
                None
            mc.headsUpMessage('ESTAS VIENDO LA CAMARA ' + str(selectLook[0]) , verticalOffset=-120)
            mc.warinig('ESTAS VIENDO LA CAMARA ' + str(selectLook[0]))
        else:
            mc.warning('Solo funciona con las camaras.')
    else:
        mc.warning('No hay camaras en la escena')
#reconoces el control y le aplica el ragetimeline
def timeAnim():
    camSel = mc.textScrollList(camListTrf, q=True, selectItem=True)
    cnts=[]
    if camSel:
        for cam in camSel:
            childCam=mc.listRelatives(cam,type = "transform",allDescendents=True)
            for cnt in childCam:
                if 'CNT' in cnt:
                    cnts.append(cnt)
        _rangeTimeLine(cnts)
    else:
        mc.warning('-Necesitas seleccionar un grupo de camara.')
#pone el lookthrough de la camara
def lookThroughSelectedCamera(sel):
    panel = "modelPanel4"  
    sel = mc.ls(selection=True)

    #if camera is only selection look through it in chosen panel
    if( len(sel) == 1 ):
        if( len(mc.listRelatives(children = True, type = "camera")) == 1 ):
            mel.eval("lookThroughModelPanel "+sel[0]+" "+panel)
#remueve valores duplicados
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # Si esta lo agrego
        if value not in seen:
            output.append(value)
            seen.add(value)
#inicializa la lista de grupos
def initGui():
    global trfCams
    #lista de camaras en scena
    trfCams = mc.ls('C_E*_P*GRP',type='transform')
    #trfCams=remove_duplicates(trfCams)
    excludeListB=['_Control','_Control','Control','__CNT','__CNTSH','TRF','HCNS','_HCNS','CAMSH','CAMShape','_SCAM']
    if trfCams!=[]:
        #filtro trf de camaras
        for x in excludeListB:
            for item in trfCams:
                if item.find(x) != -1:
                    trfCams.remove(item)
        #ordeno listas
        trfCams.sort()
    
        for cTrf in trfCams:
            mc.textScrollList(camListTrf, edit=True, append=cTrf)
    
        if len(mc.textScrollList(camListTrf, q=True, allItems=True)):
            mc.textScrollList(camListTrf, edit=True, selectIndexedItem=1)
    else:
        mc.warning(('No se reconoce ninguna camara con nombres aceptables.').upper())
#refresca las listas
def refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    mc.textScrollList(camListTrf, edit=True, removeAll=True)
    mc.textScrollList(camListBox, edit=True, removeAll=True)
    initGui();
    cantidadGRP()

#Busca el control y cheque el rango de la animacion inicio y final
def _rangeTimeLine(cnts):
    keys=[]
    keys=mc.keyframe(cnts,q=1)
    sum=0
    keyAnm=[]
    cTime=mc.currentTime( query=True )
    if cnts and keys>1:
        keyAnm=keys
        keyAnm.sort()
        firstKey = keyAnm[1]
        lastKey = keyAnm[-1]
        mc.playbackOptions(min=int(firstKey),max=int(lastKey))
        mc.playbackOptions(animationStartTime=int(firstKey),animationEndTime=int(lastKey))
        mc.currentTime(cTime)
        mc.warning( 'RANGO ANIMADO DE ' + str(firstKey) + ' A ' + str(lastKey))
    else:
        mc.warning(('Lo que seleccionaste no tiene animacion.').upper())
        mc.currentTime(cTime)
#Muestra la ventana de camera sequence
def cameraSequenceShow():
    pm.SequenceEditor('CameraSequencer')
    #hacer que se cierre despues
#desactiva boton de animacion
def buttonAnimOn():
    mc.button('botonAnimacion',edit=True,enable=1,bgc=(0.5,0.7,0.1))
#desactiva boton de animacion
def buttonAnimOff():
    mc.button('botonAnimacion',edit=True,enable=0,bgc=(0.5,0.7,0.1))
#cambia la cantidad de grupos en lista
def cantidadGRP():
    global camListTrf
    mc.text('cantidadGrupos',edit=True,label=' ( '+str(len(trfCams))+' ) ')
#comprueba si tiene animacion dentro del grupo
def haveAnim(groups):
    ToF=0
    for g in groups:
        nodes = mc.keyframe(g,query=True,name=True)
        if nodes:
            ToF=1
    return ToF
#UI
def makeWindow():

    version=' v2.8'
    winName='PH_MANAGERCAM'
    winD='FIX->THAT'
    if mc.dockControl('dockCAM',exists=True):
        mc.deleteUI('dockCAM')
    if mc.window(winName, exists=True):
        mc.deleteUI(winName)
        mc.deleteUI(winD)

    winName=mc.window(s=0)
    Form = mc.formLayout( parent = winName )
    cl1=mc.columnLayout(parent=Form,adjustableColumn = True,columnOffset=['both',5])
    #grupos
    rl15=mc.rowLayout(parent=cl1,numberOfColumns=2)
    tx1=mc.text(parent=rl15,label='\nGRUPOS EN ESCENA\n',font='boldLabelFont')
    tx6=mc.text('cantidadGrupos',parent=rl15,label=' ( NONE ) ')
    tslTRF=mc.textScrollList(camListTrf,parent=cl1, deleteKeyCommand="PH_MANAGERCAM.delSelected()", allowMultiSelection=True, selectCommand="PH_MANAGERCAM.selectTrf()",h=350)
    tx3=mc.text(parent=cl1,label='\nCAMARAS\n',font='boldLabelFont')
    #box
    tslBOX=mc.textScrollList(camListBox, parent=cl1, allowMultiSelection=False, doubleClickCommand="PH_MANAGERCAM.camLook()",selectCommand="PH_MANAGERCAM.selectChanged()",h=130)
    cl2=mc.columnLayout(parent=cl1,adjustableColumn = True,rowSpacing=10)
    rl3=mc.rowLayout( parent=cl2,numberOfColumns=3,adjustableColumn3=4)
    b5=mc.button(parent=rl3, label='ACTUALIZAR',command="PH_MANAGERCAM.refreshGui()", bgc=(0.5,0.2,0.0) ,annotation='Si hay algun cambio de camaras, es neceasrio actualizar.')
    #b1=mc.button(parent=rl3, label='VER-CAM', command="PH_MANAGERCAM.camLook()", bgc=(0.5,0.1,0.5),annotation='-Te lleva a la camara seleccionada y te pone los key en el timeline.\n-Si tiene animacion la seleccion hace un fill del timeline.')
    b6=mc.button('botonAnimacion',parent=rl3, label='VER-ANM', command="PH_MANAGERCAM.timeAnim()",enable=0, bgc=(0.3,0.3,0.3),annotation='-Selecciona una grupo de camara y muestra el rango si tiene animacion.')
    b4=mc.button(parent=rl3, label='PLAYBLAST', command="PH_MANAGERCAM.playBlastShot()", bgc=(0.1,0.5,0.0) ,annotation='-Crea en tu directorio de escena un preview con los datos necesarios, con los frames que le das.')
    #Extra
    tx5=mc.text(parent=cl1,label='\n-MORE-TOOLS-\n',font='boldLabelFont')
    cl3=mc.columnLayout(parent=cl1,adjustableColumn=True,columnAttach=('left',2))
    rl2=mc.rowLayout( parent=cl3,numberOfColumns=3,columnAttach3=("both","both",'both'))
    cl4=mc.columnLayout(parent=rl2,rowSpacing=10,adjustableColumn=True)
    b6=mc.button(parent=cl4, label='IMPORTCAM', command="PH_MANAGERCAM.importrig()", bgc=(0.9,0.5,0.0) ,annotation='-Seleciona la camara la cual remplazar para importar el rig nuevo.\n*La Camara de pampa tiene que tener este nombre para importar UD??_E???_P??_CAM')
    b8=mc.button(parent=cl4, label='UPDATERIG', command="PH_MANAGERCAM.upRig()", bgc=(0.7,0.6,0.1) ,annotation='-Remplaza rigCamaras viejos por nuevos.\nEj: SCAM_ y _control')        
    cl5=mc.columnLayout(parent=rl2,rowSpacing=10,adjustableColumn=True)
    b0=mc.button(parent=cl5, label='LOCK ANM', command="PH_MANAGERCAM.lockcams()", bgc=(0.2,0.8,0.0),annotation='-Desbloquea y bloquea atributos de las camaras por seguridad.')  
    b0a=mc.button(parent=cl5, label='LOCK PRO', command="PH_MANAGERCAM.lockcamsprop()", bgc=(0.7,0.2,0.1),annotation='-Desbloquea y bloquea seteos de camaras.\nIMPORTANTE: Primero hablar con Diego.')  
    cl6=mc.columnLayout(parent=rl2,rowSpacing=10,adjustableColumn=True)
    b3=mc.button(parent=cl6, label='CREAR SEQ', command="PH_MANAGERCAM.sequence()",bgc=(0.3,0.7,1),annotation='-Crea Secuencia con las camaras de la escena.\nTiene que tener key los controles si o si.' )
    b3a=mc.button(parent=cl6, label='SHOW SEQ', command="PH_MANAGERCAM.cameraSequenceShow()",bgc=(0.3,0.7,1),annotation='-Muestra la ventana de Camera Sequencer.' )
    cl7=mc.columnLayout(parent=cl1)
    tx4=mc.text(parent=cl7,label='\nHELP: Sobre cada boton tenes mas informacion.\n\n',font='smallObliqueLabelFont')
    allowedAreas = ['right', 'left']
    sc1=mc.dockControl('dockCAM', label='PH_MANAGERCAM'+version,area='right', content=winName, allowedArea=allowedAreas)
    #fill gui with cameras
    refreshGui()
import maya.cmds
import maya.mel as mel
import pymel.core.runtime as pm
global camListBox
camListBox = ['x']
global camListTrf
camListTrf = ['']
global dupliname
dupliname = ['d']

#Archivos mels
def sequence():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_CAMERASEQUENCER.mel"')
def importrig():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_IMPORTRIG.mel"')
    refreshGui()
def lockcams():
    mel.eval('source "D:/PH_SCRIPTS/PH_RENDER/PH_MANAGERCAM/PH_LOCKCAMERAS.mel"')
def selectChanged():
    selectCam = cmds.textScrollList(camListBox, q=True, selectItem=True)
    sel= cmds.ls(selectCam[0])
    if len(sel) >= 2:
        cmds.warning('HAY DOS OBJETOS CON EL MISMO NOMBRE OJO:' + str(sel)+'.\nPORFAVOR RENOMBRAR BIEN.')
    else:
        selectCam = cmds.listRelatives(selectCam[0],children=True, fullPath=True)
        cmds.select(selectCam)

def selectTrf():
    global trfCams
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    cameras = cmds.listRelatives(selectCam[0],type='transform',allDescendents=True)
    excludeListA=['_CAM','__CAM','GRP','TRFShape','_HCNS','__HCNS','TRFSH','_SCAMF','_CNTSH','_SCAMF','_SCAMSH','__SCAMH','__SCAMSH']
    excludeListC=['parentConstraint','parentConstraint1','Frustum']
    if cameras!=[]:
        #filtro trf de camaras
        for x in excludeListA+excludeListC+trfCams:
            for item in cameras:
                if item.find(x) != -1:
                    cameras.remove(item)
    cameras.sort()
    for aCam in cameras:
        cmds.textScrollList(camListBox, edit=True, append=aCam)
    cmds.select(selectCam)

def delSelected():

    selectCam = cmds.textScrollList(camListTrf, q=True, selectItem=True)
    for sc in selectCam:
        if sc:
            cmds.delete(str(sc))
            cmds.warning('SE BORRO ' + str(sc))
        else:
            cmds.warning('LO SIENTO NO PUDE BORRAR ' + str(sc))
    refreshGui()

def newCam():
    cmds.camera(name='C_RENOMBRAME_RENOMBRAME__CAM')
    refreshGui()
def dupExist():
    badXforms = [f for f in cmds.ls(type='camera') if '|' in f]
    if badXforms:
        DupUI()
    else:
        print 'Increible no hay nombres duplicados'
def DupUI():
    global dupliname
    winD='FIX->THAT'
    # UI DUP
    if cmds.window(winD, exists=True):
        cmds.deleteUI(winD)
    winD=cmds.window(winD+'w',title=winD)
    cmds.columnLayout( adjustableColumn=True )
    cmds.text(label='¿DESEA RENOMBRAR AUTOMATICAMENTE LOS NOMBRES?')
    cmds.textScrollList(dupliname,selectCommand="dupsel()")
    cmds.button('yes',label='RENOMBRAR DUPLICADOS',command='renameDuplicates()')
    cmds.button('no',label='DEJARLO MAL',command="cmds.deleteUI(winD)")
    cmds.showWindow(winD)
    cmds.textScrollList(dupliname, edit=True, removeAll=True)
    checkdup()
def checkdup():
    global dupliname
    badXforms = [f for f in cmds.ls(type='camera') if '|' in f]
    badXforms.sort()
    if len(badXforms)>0:
        for dup in badXforms:
            cmds.textScrollList(dupliname, edit=True, append=dup)
    else:
        cmds.textScrollList(dupliname, edit=True, append='NO ENCONTRE NODOS DUPLICADOS')
        
def dupsel():
    selDup = cmds.textScrollList(dupliname, q=True, selectItem=True)
    cmds.select(selDup)
def renameDuplicates(padding=3):
    badXforms = [f for f in cmds.ls(type='camera') if '|' in f]
    badXformsUnlock = [f for f in badXforms if cmds.lockNode(f,q=1,lock=1)[0] == False]
    count = 0
    countDict = {}
    for f in badXformsUnlock:
        countDict[f] = f.count('|')
    for key,value in sorted(countDict.iteritems(),reverse=True, key=lambda (key,value): (value,key)):
        n = 1
        newObj = cmds.rename(key,key.split('|')[-1]+'_'+str(n).zfill(padding))
        while newObj.count('|') > 0:
            n += 1
            basename = newObj.split('|')[-1]
            newName = '_'.join(basename.split('_')[0:-1])+'_'+str(n).zfill(padding)
            newObj = cmds.rename(newObj,newName)
        print 'renamed %s to %s' % (key,newObj)
        count = count+1
    if count < 1:
        return 'No duplicate names found.'
    else:
        return 'Found and renamed '+str(count)+' objects with duplicate names. Check script editor for details.'
       
    
#Enfocar en esa camara
def camLook():
    global camListBox
    selectLook = cmds.textScrollList(camListBox, q=True, selectItem=True)
    if selectLook:
        cmds.select(selectLook[0])
        cmds.lookThru(selectLook[0]) # looks through the camera I specify
        lookThroughSelectedCamera(selectLook[0])
        cnts=[]
        if '|' in padreSrc[0]:
            childrenS = cmds.listRelatives(padreSrc[0].split('|')[1], path=True)
            if len(childrenS) > 0:
                for cnt in childrenS:
                    if 'Control' or 'CNT' in cnt:
                        cnts.append(cnt)
                _rangeTimeLine(cnt)
        else:
            None
        cmds.headsUpMessage('ESTAS VIENDO LA CAMARA ' + str(selectLook[0]) , verticalOffset=-120)
    else:
        cmds.warning('No hay camaras en la escena')

def lookThroughSelectedCamera(sel):
    panel = "modelPanel4"  
    sel = cmds.ls(selection=True)

    #if camera is only selection look through it in chosen panel
    if( len(sel) == 1 ):
        if( len(cmds.listRelatives(children = True, type = "camera")) == 1 ):
            mel.eval("lookThroughModelPanel "+sel[0]+" "+panel)

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # Si esta lo agrego
        if value not in seen:
            output.append(value)
            seen.add(value)
def initGui():
    global trfCams
    #lista de camaras en scena
    trfCams = cmds.ls('C_E*_P*','SCAM_*',type='transform')
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
            cmds.textScrollList(camListTrf, edit=True, append=cTrf)
    
        if len(cmds.textScrollList(camListTrf, q=True, allItems=True)):
            cmds.textScrollList(camListTrf, edit=True, selectIndexedItem=1)
    else:
        cmds.warning(('No se reconoce ninguna camara con nombres aceptables.').upper())

def refreshGui():
    # remove all existing items from the textScrollList, then repopulate it with initGui()
    cmds.textScrollList(camListTrf, edit=True, removeAll=True)
    cmds.textScrollList(camListBox, edit=True, removeAll=True)
    initGui();

#Busca el control y cheque el rango de la animacion inicio y final
def _rangeTimeLine(cnts):
    keys=cmds.keyframe(cnts, q=1)
    cTime=cmds.currentTime( query=True )
    if keys:
        keys.sort()
        firstKey = keys[1]
        lastKey = keys[-1]
        cmds.playbackOptions(min=int(firstKey),max=int(lastKey))
        cmds.playbackOptions(animationStartTime=int(firstKey),animationEndTime=int(lastKey))
        cmds.currentTime(cTime)
        cmds.warning( 'RANGO ANIMADO DE ' + str(firstKey) + ' A ' + str(lastKey))
    else:
        cmds.warning(('Lo que seleccionaste no tiene animacion.').upper())
        cmds.currentTime(cTime)
def cameraS():
    pm.SequenceEditor('CameraSequencer')
def makeWindow():

    version=' v1.0'
    winName='PH_MANAGERCAM'
    winD='FIX->THAT'
    if cmds.window(winName, exists=True):
        cmds.deleteUI(winName)
        cmds.deleteUI(winD)

    winName=cmds.window(s=1)
    Form = cmds.formLayout( parent = winName )
    cl1=cmds.columnLayout(parent=Form,adjustableColumn = True,columnOffset=['left',10])
    tx1=cmds.text(parent=cl1,label='GRUPOS\n')
    tslTRF=cmds.textScrollList(camListTrf,parent=cl1, deleteKeyCommand="delSelected()", allowMultiSelection=True, selectCommand="selectTrf()",h=350)
    tx3=cmds.text(parent=cl1,label='CAMARAS\n')
    tslBOX=cmds.textScrollList( parent=cl1, allowMultiSelection=False, selectCommand="selectChanged()",h=150)
    cl2=cmds.columnLayout(parent=cl1,adjustableColumn = True,columnOffset=['both',15])
    b1=cmds.button(parent=cl2, label='VER CAMARA', command="camLook()", bgc=(0.5,0.1,0.5),annotation='-Te lleva a la camara seleccionada y te pone los key en el timeline.\n-Si tiene animacion la seleccion hace un fill del timeline.')
    b0=cmds.button(parent=cl2, label='LOCK/UNLOCK CAMARAS', command="lockcams()", bgc=(0.2,0.8,0.0),annotation='Desbloquea y bloquea atributos de las camaras por seguridad.')
    cl3=cmds.columnLayout(parent=cl2,adjustableColumn = True,columnOffset=['both',10])
    tx5=cmds.text(parent=cl3,label='CAMARAS\n')
    b3=cmds.button(parent=cl3, label='CREAR SEQ', bgc=(0.3,0.7,1),annotation='Crea Secuencia con las camaras de la escena.' )
    b3a=cmds.button(parent=cl3, label='SHOW', bgc=(0.3,0.7,1),annotation='Muestra la ventana de Camera Sequencer.' )
    b4=cmds.button(parent=cl3, label='IMPORTCAM',  bgc=(0.9,0.5,0.0) ,annotation='Seleciona la camara la cual remplazar para importar el rig nuevo.\n*La Camara de pampa tiene que tener este nombre para importar UD??_E???_P??_CAM')
    b5=cmds.button(parent=cl3, label='ACTUALIZAR', bgc=(0.5,0.2,0.0) ,annotation='Si hay algun cambio de camaras, es neceasrio actualizar.')
    tx4=cmds.text(parent=cl3,label='HELP: Mantene puntero del raton arriba de cada\n boton para ver mas info.')
    allowedAreas = ['right', 'left']
    sc1=cmds.dockControl( label=winName+version,area='left', content=myWindow, allowedArea=allowedAreas)
    #fill gui with cameras
    dupExist()
    initGui()

makeWindow()
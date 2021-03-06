import maya.cmds as cmds
from functools import partial
from operator import itemgetter


global grupo_
global orden
global ultimoOrden


def add_light(kind):
	global contSpot
	global contDir
	global contPoint
	global contArea
	global contAmb

	if(not cmds.ls('ROOT_LGRP')):
		root = cmds.group(name='ROOT_LGRP', em=True, w=True)
		rootAts = cmds.listAttr (root , k=1 )
		for at in rootAts:
			cmds.setAttr (root+"."+at,lock=1,k=0,channelBox=0)

	if cmds.window('crearLuz',exists=True):
		cmds.deleteUI ('crearLuz')
	ventanaCreacionLuz = cmds.window ('crearLuz' , menuBar=0,w=250,title = "CREAR LUZ" )
	col_ventanaCrearLuz = cmds.columnLayout( adjustableColumn = True , p = ventanaCreacionLuz )
	cmds.textField ('nombreLuzCreacion' , text='NOMBRE' ,  p=col_ventanaCrearLuz ,ec="crearLuz()" )

	cmds.radioCollection('coleccionTodo')

	rowDeColumnas=cmds.rowLayout (nc=3,co3=[25,0,0],ct3=["left", "both","both"], p=col_ventanaCrearLuz)
	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton( 'K',label='KEY', sl=1,cl='coleccionTodo')

	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton('F', label='FILL', cl='coleccionTodo')

	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton( 'R',label='RIM', cl='coleccionTodo')

	cmds.button ('b_crearLuz' , l='CREAR', c= partial (crearLuz,kind) , p=col_ventanaCrearLuz)
	cmds.button ('b_cancelarCrearLuz' , l='CANCELAR' , c="cmds.deleteUI('crearLuz')" , p=col_ventanaCrearLuz)
	cmds.showWindow ('crearLuz')

def crearLuz(kind,*kargs):
	nombreLuz = cmds.textField('nombreLuzCreacion',q=1,text=1)+"_"+cmds.radioCollection('coleccionTodo',q=1,select=1)+"_"
	cmds.deleteUI ('crearLuz')

	if nombreLuz=="" or nombreLuz=="Nombre":
		nombreLuz = 'RENAMEMEPLEASE'
	if kind == 'spot':
		nameLight = cmds.spotLight(name=nombreLuz)
		nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
		nroLuz=1
		if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPO'):
			while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LSPO'):
				nroLuz +=1
			nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
			nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LSPO' )
		else:
			nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LSPO')
		cmds.select(nombreConSuff)
		cmds.parent(nombreConSuff, 'ROOT_LGRP')
	elif kind == 'dir':
		nameLight = cmds.directionalLight(name=nombreLuz)
		nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
		nroLuz=1
		if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LDIR'):
			while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LDIR'):
				nroLuz +=1
			nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
			nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LDIR' )
		else:
			nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LDIR')
		cmds.select(nombreConSuff)
		cmds.parent(nombreConSuff, 'ROOT_LGRP')
	elif kind == 'point':
		nameLight = cmds.pointLight(name=nombreLuz)
		nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
		nroLuz=1
		if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LPNT'):
			while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LPNT'):
				nroLuz +=1
			nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
			nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LPNT' )
		else:
			nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LPNT')
		cmds.select(nombreConSuff)
		cmds.parent(nombreConSuff, 'ROOT_LGRP')
	elif kind == 'area':
		nameLight = cmds.shadingNode('areaLight',name=nombreLuz, asLight=True).encode("utf-8")
		nombreSinSuff = cmds.listRelatives(nameLight, shapes=True, children= True, allParents=True)[0]
		nroLuz=1
		if cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LARE'):
			while cmds.objExists (nombreSinSuff+str(nroLuz).zfill(3)+'_LARE'):
				nroLuz +=1
			nombreSinSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) )
			nombreConSuff = cmds.rename(  nombreSinSuff , nombreSinSuff + '_LARE' )
		else:
			nombreConSuff=cmds.rename(  nombreSinSuff , nombreSinSuff + str(nroLuz).zfill(3) + '_LARE')
		cmds.select(nombreConSuff)
		cmds.parent(nombreConSuff, 'ROOT_LGRP')
	ordenarLuz()


#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def clearOptionMenu (optionMenu):
	optionMenuFullName = None
	try:
		menuItems = cmds.optionMenuGrp ( grupo_ , q=1 , ill=1 )
		if menuItems != None and menuItems !=[]:
			cmds.deleteUI ( menuItems )
		firstItem = menuItems[0]
		optionMenuFullName = firstItem [:-len(firstItem.split ("|")[1])-1]
	except:
		pass
	return optionMenuFullName

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def buscar():
	textoBuscador = cmds.textField ( 'buscador' , q=1 , text=True)
	try:
		if str(textoBuscador[0]).isdigit() ==1:
			recolectorBusqueda= cmds.ls("*"+textoBuscador,"*"+textoBuscador+"*", type='transform')
		else:
			recolectorBusqueda= cmds.ls(textoBuscador+"*","*"+textoBuscador,"*"+textoBuscador+"*",textoBuscador , textoBuscador.upper()+"*","*"+textoBuscador.upper(),"*"+textoBuscador.upper()+"*",textoBuscador.upper() , type='transform')
		recolectorBusqueda=list(set(recolectorBusqueda))
		for luz in recolectorBusqueda: # elimino cosas que no tengan sufijo correcto
			if (not "_LPNT" in luz) and (not "_LSPO" in luz) and (not "_LDIR" in luz) and (not "_LAMB" in luz) and (not "_LARE" in luz):
				print luz
				recolectorBusqueda.remove(luz)
		cmds.textScrollList ('listaLuces1' , e=1 , da= 1)
		cmds.textScrollList ('listaLuces2' , e=1 , da= 1)
		cmds.textScrollList ('listaLuces3' , e=1 , da= 1)

		cmds.textScrollList ('listaLuces1' , e=1 , si= recolectorBusqueda)
		indice = cmds.textScrollList ('listaLuces1' , q=1 , sii=1)
		cmds.textScrollList ('listaLuces2' , e=1 , sii=indice)
		cmds.textScrollList ('listaLuces3' , e=1 , sii=indice)

	except:
		pass
#........................................................................................................................

def borrarBuscador():
	#if cmds.textField ('buscador' , q=1 , text=1) == "Buscador":
	#	cmds.textField ('buscador' , e=1 , text="")
	cmds.warning ("~~~~~~~~~ borrarBuscador() ~~~~~~~~~")

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def seleccionarLuces():
    cmds.select ( cmds.textScrollList ('listaLuces1',q=1, si=1) )

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def filtrado(luzTipo, *args):
	imagen = cmds.iconTextButton ('b_filtro'+luzTipo,q=1, i1=1)
	if int(imagen[-5])==1:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_0.png")
	if int(imagen[-5])==0:
		cmds.iconTextButton ('b_filtro'+luzTipo , e=1 , i1="M:\PH_SCRIPTS\ICONS\\"+luzTipo+"_1.png")

	#  QUERY DE FILTROS ACTIVADOS.
	filtros = ['b_filtroLPNT','b_filtroLDIR','b_filtroLSPO','b_filtroLARE']
	filtrosActivos=[]

	for filtro in filtros:
		estadoFiltro = int  ((cmds.iconTextButton (filtro , q = 1 , i1=1))[-5])
		if estadoFiltro==1:
			filtrosActivos.append ( "*"+ filtro[-4:] + "Shape" )

	ordenarTipo( arraySufijos =filtrosActivos)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def refreshui(refrescarPor):
    global grupo_
    if refrescarPor=='luz':
        lucesSeleccionadasIndices = cmds.textScrollList('listaLuces1' ,q=1, sii=1)
        cmds.textScrollList ('listaLuces2' , e=1 ,da=1)
        cmds.textScrollList ('listaLuces3' , e=1 ,da=1)
        try:
            cmds.textScrollList ('listaLuces2' , e=1 ,sii=lucesSeleccionadasIndices)
            cmds.textScrollList ('listaLuces3' , e=1 ,sii=lucesSeleccionadasIndices)
        except:
            pass
    if refrescarPor=='tipo':
        lucesSeleccionadasIndices = cmds.textScrollList('listaLuces2' ,q=1, sii=1)
        cmds.textScrollList ('listaLuces1' , e=1 ,da=1)
        cmds.textScrollList ('listaLuces3' , e=1 ,da=1)
        try:
            cmds.textScrollList ('listaLuces1' , e=1 ,sii=lucesSeleccionadasIndices)
            cmds.textScrollList ('listaLuces3' , e=1 ,sii=lucesSeleccionadasIndices)
        except:
            pass
    if refrescarPor=='grupo':
        lucesSeleccionadasIndices = cmds.textScrollList('listaLuces3' ,q=1, sii=1)
        cmds.textScrollList ('listaLuces1' , e=1 ,da=1)
        cmds.textScrollList ('listaLuces2' , e=1 ,da=1)
        try:
            cmds.textScrollList ('listaLuces1' , e=1 ,sii=lucesSeleccionadasIndices)
            cmds.textScrollList ('listaLuces2' , e=1 ,sii=lucesSeleccionadasIndices)
        except:
            pass

    #ACTUALIZO GRUPOS
    clearOptionMenu (grupo_)
    gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
    for grp in gruposDeLuces:
        cmds.menuItem(parent=(grupo_ +'|OptionMenu'), label=grp[:-5] )

    # REFRESH DE ATRIBUTOS.
    lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
    camposAtributos = {"aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }
    camposAtributosV = {"aiExposure":0 , "aiRadius":0, "aiColorTemperature":[], "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }
    camposAtributosMinMax = {"aiExposure":0 , "aiRadius":0, "intensity":0, "aiAngle":0, "aiSamples":0 }
    camposAtributosDif = {"aiExposure":0 , "aiRadius":0, "aiColorTemperature":0, "color":0, "intensity":0, "aiAngle":0, "aiSamples":0,"emitDiffuse":0,"emitSpecular":0 }

    for luz in lucesSeleccionadas:
        for key in camposAtributos.keys():
            try:
                if (cmds.attributeQuery (key , node=luz+"Shape" , ex=1)):
                    camposAtributosMinMax[key]=cmds.getAttr ( luz+"Shape."+key ) # CAPTURO EL VALOR PARA USARLO EN COMPARACION MIN/MAX
                    camposAtributos [key] += 1
                    if cmds.getAttr ( luz+"Shape."+key ) == cmds.getAttr ( lucesSeleccionadas[0]+"Shape."+key ) and camposAtributosDif [key] != 1:
                        camposAtributosV [key] = cmds.getAttr ( luz+"Shape."+key )
                    else:
                        camposAtributosV [key] = 0
                        camposAtributosDif [key] = 1
            except:
                pass
	# VALORES
	for campo in camposAtributos.keys():
		if camposAtributos[campo] == len (lucesSeleccionadas) and camposAtributosDif[campo]!=1:
		    try:
		        cmds.floatField ( campo , e=1 , v = camposAtributosV[campo])
		    except:
		        pass
		    try:
		        cmds.checkBox ( campo , e=1 , v = camposAtributosV[campo] )
		    except:
		        pass
		    try:
		        cmds.colorSliderGrp( campo , e=1 , v = camposAtributosV[campo] )
		    except:
		        pass

	# HABILITAR O DESHABILITAR
	for campo in camposAtributos.keys():
		if camposAtributosDif [campo] ==0 and len(lucesSeleccionadas)==camposAtributos[campo]:#tienen valores iguales
			try:
				cmds.floatField ( campo , e=1 , en=1 , bgc=[0.3,0.3,0.3])
			except:
				pass
			try:
				cmds.checkBox ( campo , e=1 , en=1  , bgc=[0.3,0.3,0.3] )
			except:
				pass
			try:
				cmds.colorSliderGrp( campo , e=1 , en=1 , bgc=[0.3,0.3,0.3] )
			except:
				pass
		elif camposAtributosDif [campo] !=0 and len(lucesSeleccionadas)==camposAtributos[campo]:#tienen valores diferentes
			try:
				cmds.floatField ( campo , e=1 , en=1 , bgc=[0.863,0.808,0.529])
			except:
				pass
			try:
				cmds.checkBox ( campo , e=1 ,  en=1 , bgc=[0.863,0.808,0.529])
			except:
				pass
			try:
				cmds.colorSliderGrp( campo , e=1 ,  en=1 , bgc=[0.863,0.808,0.529] )
			except:
				pass
		elif len(lucesSeleccionadas)!=camposAtributos[campo]:# no todos tienen ese atributo
			try:
				cmds.floatField ( campo , e=1 , en=0 , bgc=[0.863,0.808,0.529])
			except:
				pass
			try:
				cmds.checkBox ( campo , e=1 ,  en=0 , bgc=[0.863,0.808,0.529])
			except:
				pass
			try:
				cmds.colorSliderGrp( campo , e=1 ,  en=0 , bgc=[0.863,0.808,0.529] )
			except:
				pass

#-------------------------------------------------------------------------------------

	intensityMin = 0
	intensityMax = 0
	aiExposureMin = 0
	aiExposureMax =	0
	aiRadiusMin = 0
	aiRadiusMax = 0
	aiAngleMin = 0
	aiAngleMax = 0
	aiSamplesMin = 0
	aiSamplesMax = 0
	intensityMin = camposAtributosMinMax ["intensity"]
	intensityMax = camposAtributosMinMax ["intensity"]
	aiExposureMin = camposAtributosMinMax ["aiExposure"]
	aiExposureMax =	camposAtributosMinMax ["aiExposure"]
	aiRadiusMin = camposAtributosMinMax ["aiRadius"]
	aiRadiusMax = camposAtributosMinMax ["aiRadius"]
	aiAngleMin = camposAtributosMinMax ["aiAngle"]
	aiAngleMax = camposAtributosMinMax ["aiAngle"]
	aiSamplesMin = camposAtributosMinMax ["aiSamples"]
	aiSamplesMax = camposAtributosMinMax ["aiSamples"]
	intensityMinL = ""
	intensityMaxL = ""
	aiExposureMinL = ""
	aiExposureMaxL = ""
	aiRadiusMinL = ""
	aiRadiusMaxL = ""
	aiAngleMinL = ""
	aiAngleMaxL = ""
	aiSamplesMinL = ""
	aiSamplesMaxL = ""
    for luz in lucesSeleccionadas:
        if (cmds.attributeQuery ("aiExposure" , node=luz+"Shape" , ex=1)):
            if cmds.getAttr ( luz + "Shape.aiExposure" ) < aiExposureMin :
                aiExposureMin = cmds.getAttr ( luz + "Shape.aiExposure" )
                aiExposureMinL = luz
            if cmds.getAttr ( luz + "Shape.aiExposure" ) > aiExposureMax :
                aiExposureMax = cmds.getAttr ( luz + "Shape.aiExposure" )
                aiExposureMaxL = luz
        if (cmds.attributeQuery ("aiRadius" , node=luz+"Shape" , ex=1)):
            if cmds.getAttr ( luz + "Shape.aiRadius" ) < aiRadiusMin :
                aiRadiusMin = cmds.getAttr ( luz + "Shape.aiRadius" )
                aiRadiusMinL = luz
            if cmds.getAttr ( luz + "Shape.aiRadius" ) > aiRadiusMax :
                aiRadiusMax = cmds.getAttr ( luz + "Shape.aiRadius" )
                aiRadiusMaxL = luz

        if cmds.attributeQuery ("intensity" , node=luz+"Shape" , ex=1):
            print intensityMin,intensityMax
            if cmds.getAttr ( luz + "Shape.intensity" ) < intensityMin :
                intensityMin = cmds.getAttr ( luz + "Shape.intensity" )
                intensityMinL =luz
            if cmds.getAttr ( luz + "Shape.intensity" ) > intensityMax :
                intensityMax = cmds.getAttr ( luz + "Shape.intensity" )
                intensityMaxL = luz
        if (cmds.attributeQuery ("aiAngle" , node=luz+"Shape" , ex=1)):
            if cmds.getAttr ( luz + "Shape.aiAngle" ) < aiAngleMin :
                aiAngleMin = cmds.getAttr ( luz + "Shape.aiAngle" )
                aiAngleMinL = luz
            if cmds.getAttr ( luz + "Shape.aiAngle" ) > aiAngleMax :
                aiAngleMax = cmds.getAttr ( luz + "Shape.aiAngle" )
                aiAngleMaxL = luz
        if (cmds.attributeQuery ("aiSamples" , node=luz+"Shape" , ex=1)):
            if cmds.getAttr ( luz + "Shape.aiSamples" ) < aiSamplesMin :
                aiSamplesMin =  cmds.getAttr ( luz + "Shape.aiSamples" )
                aiSamplesMinL = luz
            if cmds.getAttr ( luz + "Shape.aiSamples" ) > aiSamplesMax :
                aiSamplesMax =  cmds.getAttr ( luz + "Shape.aiSamples" )
                aiSamplesMaxL = luz

	if len(lucesSeleccionadas)>1:
		cmds.floatField ('intensity'  , e=1 , ann= "MIN: " + str(intensityMinL)+"  "+str(intensityMin)+"\n"+"MAX: " + str(intensityMaxL)+ "  " + str(intensityMax)+"\n"+"PROMEDIO: "+ str( (intensityMax-intensityMin)/2+intensityMin ))
		cmds.floatField ('aiExposure' , e=1 , ann= "MIN: " + str(aiExposureMinL)+"  "+str(aiExposureMin)+"\n"+"MAX: " + str(aiExposureMaxL)+ "  " + str(aiExposureMax) +"\n"+"PROMEDIO: "+ str( (intensityMax-intensityMin)/2+intensityMin ) )
		cmds.floatField ('aiRadius'   , e=1 , ann= "MIN: " + str(aiRadiusMinL)+"  "+str(aiRadiusMin)+"\n"+"MAX: " + str(aiRadiusMaxL)+ "  " + str(aiRadiusMax) +"\n"+"PROMEDIO: "+ str( (aiRadiusMax-aiRadiusMin)/2+aiRadiusMin ) )
		cmds.floatField ('aiAngle'    , e=1 , ann= "MIN: " + str(aiAngleMinL)+"  "+str(aiAngleMin)+"\n"+"MAX: " + str(aiAngleMaxL)+ "  " + str(aiAngleMax) +"\n"+"PROMEDIO: "+ str( (aiAngleMax-aiAngleMin)/2+aiAngleMin ) )
		cmds.floatField ('aiSamples'  , e=1 , ann= "MIN: " + str(aiSamplesMinL)+"  "+str(aiSamplesMin)+"\n"+"MAX: " + str(aiSamplesMaxL)+ "  " + str(aiSamplesMax) +"\n"+"PROMEDIO: "+ str( (aiSamplesMax-aiSamplesMin)/2+aiSamplesMin ) )
	else:
		cmds.floatField ('intensity'  , e=1 , ann= "")
		cmds.floatField ('aiExposure' , e=1 , ann= "")
		cmds.floatField ('aiRadius'   , e=1 , ann= "")
		cmds.floatField ('aiAngle'    , e=1 , ann= "")
		cmds.floatField ('aiSamples'  , e=1 , ann= "")

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def setInt():
	print "················SET·INTENSITY·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'Shape.intensity', cmds.floatField ('intensity',q=1,v=1) )
					print "abs"
				else:
					cmds.setAttr (luz+'Shape.intensity',  cmds.getAttr ( luz+'Shape.intensity' ) +   cmds.floatField ('intensity',q=1,v=1) )
					print "rel"
			except:
				pass
		cmds.textScrollList ('listaLuces1',e=1,si=lucesSeleccionadas)
	except:
		pass

#........................................................................................................................

def setExp():
	print "················SET·EXPOSURE·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'Shape.aiExposure', cmds.floatField ('aiExposure',q=1,v=1) )
					print "abs"
				else:
					cmds.setAttr (luz+'Shape.aiExposure',  cmds.getAttr ( luz+'Shape.aiExposure' ) +   cmds.floatField ('aiExposure',q=1,v=1) )
					print "rel"
			except:
				pass
		cmds.textScrollList ('listaLuces1',e=1,si=lucesSeleccionadas)
	except:
		pass

#........................................................................................................................

def setRad():
	print "················SET·RADIUS·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'Shape.aiRadius', cmds.floatField ('aiRadius',q=1,v=1) )
					print "abs"
				else:
					cmds.setAttr (luz+'Shape.aiRadius',  cmds.getAttr ( luz+'Shape.aiRadius' ) +   cmds.floatField ('aiRadius',q=1,v=1) )
					print "rel"
			except:
				pass
	except:
		pass

#........................................................................................................................

def setAng():
	print "················SET·ANGLE·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'Shape.aiAngle', cmds.floatField ('aiAngle',q=1,v=1) )
					print "abs"
				else:
					cmds.setAttr (luz+'Shape.aiAngle',  cmds.getAttr ( luz+'Shape.aiAngle' ) +   cmds.floatField ('aiAngle',q=1,v=1) )
					print "rel"
			except:
				pass
	except:
		pass

#........................................................................................................................

def setSamp():
	print "················SET·SAMPLES·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				if cmds.radioCollection('radioAbsRel',q=1,sl=1)=='A':
					cmds.setAttr (luz+'Shape.aiSamples', cmds.floatField ('aiSamples',q=1,v=1) )
					print "abs"
				else:
					cmds.setAttr (luz+'Shape.aiAngle',  cmds.getAttr ( luz+'Shape.aiAngle' ) +   cmds.floatField ('aiAngle',q=1,v=1) )
					print "rel"
			except:
				pass
	except:
		pass

#............................................................

def setColor():
	print "················SET·COLOR·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				cmds.setAttr (luz+'Shape.color', cmds.floatField ('color',q=1,v=1) )
			except:
				pass
	except:
		pass

#............................................................

def setilumDef():
	cmds.warning ("·")
#............................................................

def setDif():
	print "················SET·EMITDIFFUSE·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				cmds.setAttr (luz+'Shape.emitDiffuse', cmds.checkBox ('emitDiffuse',q=1,v=1) )
			except:
				pass
	except:
		pass
#............................................................

def setSpec():
	print "················SET·EMITSPECULAR·····················"
	try:
		lucesSeleccionadas = cmds.textScrollList ('listaLuces1', q=1 , si=1)
		for luz in lucesSeleccionadas:
			try:
				cmds.setAttr (luz+'Shape.emitSpecular', cmds.checkBox ('emitSpecular',q=1,v=1) )
			except:
				pass
	except:
		pass

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def borrarSeleccion():
	try:
		lucesSeleccionadas = cmds.textScrollList ( 'listaLuces1' , q=1 , si=1 )
		for luz in lucesSeleccionadas:
			cmds.delete(luz)
		ordenarLuz()
	except:
		pass

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def ordenarLuz(seleccionar=1):
	global orden
	datosOrdenados = ordenarDatos(ordenarPor='luz' , filtrado='')
	if orden["luz"]%2 == 1:
		datosOrdenados[0].reverse()
		datosOrdenados[1].reverse()
		datosOrdenados[2].reverse()

	listas = ['listaLuces1','listaLuces2','listaLuces3']
	try:
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
	except:
		pass
	for lista in listas:
		cmds.textScrollList (lista, e=1 ,ra=1)
	try:
		cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2 , si=seleccionar)
	except:
		pass
	try:
		indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
	except:
		pass
	try:
		cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii= indiceSeleccionLista1)
	except:
		pass
	try:
		cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	except:
		pass
  	orden["luz"] +=1

#··············································································································

def ordenarTipo( arraySufijos ='',seleccionar=1 ):
	global orden
	if filtrado =='':
		datosOrdenados = ordenarDatos(ordenarPor='tipo' , filtrado='')
	else:
		datosOrdenados = ordenarDatos(ordenarPor='tipo' , filtrado=arraySufijos)
	if orden["tipo"]%2 == 1:
		datosOrdenados[0].reverse()
		datosOrdenados[1].reverse()
		datosOrdenados[2].reverse()

	listas = ['listaLuces1','listaLuces2','listaLuces3']
	try:
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
	except:
		pass
	for lista in listas:
		cmds.textScrollList (lista, e=1 ,ra=1)
	cmds.textScrollList ('listaLuces1' , e=1  ,  a=datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2, si=seleccionar )
	indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
	try:
		cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	except:
		pass
	try:
		cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	except:
		pass
	orden["tipo"] +=1
	ultimoOrden="tipo"

#··············································································································

def ordenarGrupo(seleccionar=1):
	global orden
	datosOrdenados = ordenarDatos(ordenarPor='grupo', filtrado='' )
	listas = ['listaLuces1','listaLuces2','listaLuces3']
	if orden["grupo"]%2 == 1:
		datosOrdenados[0].reverse()
		datosOrdenados[1].reverse()
		datosOrdenados[2].reverse()
	try:
		seleccionar = cmds.textScrollList ('listaLuces1' , q=1 , si=1 )
	except:
		pass

	for lista in listas:
		cmds.textScrollList (lista, e=1 ,ra=1)

	cmds.textScrollList ('listaLuces1' , e=1  ,  a= datosOrdenados[0] , numberOfRows = len(datosOrdenados[0])+2, si=seleccionar)
	indiceSeleccionLista1 = cmds.textScrollList ('listaLuces1' , q=1 , sii=1 )
	cmds.textScrollList ('listaLuces2' , e=1  ,  a=datosOrdenados[1] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	cmds.textScrollList ('listaLuces3' , e=1  ,  a=datosOrdenados[2] , numberOfRows = len(datosOrdenados[0])+2, sii=indiceSeleccionLista1)
	orden["grupo"]+=1
	ultimoOrden="grupo"
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def cambiarGrupo():
	global orden
	lucesSeleccionadas = cmds.textScrollList('listaLuces1' ,q=1, si=1)
	lucesSeleccionadasInd = cmds.textScrollList('listaLuces1' ,q=1, sii=1)
	grupoSeleccionado = cmds.optionMenu ( (grupo_ +'|OptionMenu')  , q=1 , value=1)
	for luz in lucesSeleccionadas:
	    try:
	        cmds.parent ( luz , grupoSeleccionado+"_LGRP" )
	    except:
	        print "error"
	        pass
	if ultimoOrden=="luz":
		orden["luz"]+=1
		ordenarLuz(seleccionar=lucesSeleccionadasInd)
	if ultimoOrden=="tipo":
		orden["tipo"]+=1
		ordenarTipo()
	if ultimoOrden=="grupo":
		orden["grupo"]+=1
		ordenarGrupo()

#··············································································································

def crearGrupo():
	if(not cmds.ls('ROOT_LGRP')):
		cmds.group(name='ROOT_LGRP', em=True, w=True)

	pideNombreGrupo = cmds.promptDialog(title='NOMBRAR',message='NOMBRE DE GRUPO:',button=['OK', 'CANCELAR'],defaultButton='OK',cancelButton='CANCELAR',dismissString='Cancel')

	if pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==False:
		qNombreGrupo = cmds.promptDialog(query=True, text=True)
		cmds.group(name = qNombreGrupo.upper() + '_LGRP', em=True, w=True)
		cmds.parent ( qNombreGrupo.upper() + '_LGRP' , 'ROOT_LGRP' )
		#ACTUALIZO GRUPOS
		clearOptionMenu (grupo_)
		gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
		for grp in gruposDeLuces:
			cmds.menuItem(parent=(grupo_ +'|OptionMenu'), label=grp[:-5] )
	elif pideNombreGrupo == 'OK' and str(cmds.promptDialog(query=True, text=True))[0].isdigit()==True:
		cmds.warning ( "EL NOMBRE NO PUEDE COMENZAR CON UN NUMERO. TRANQUIIIILO. TE CANCELE LA CREACION, AMEO." )
	else:
		cmds.warning ( "USUARIO CANCELA" )

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def ordenarDatos(ordenarPor , filtrado=''):
    if filtrado=='':
	    luces = cmds.ls(['*_LPNTShape','*_LDIRShape','*_LAREShape','*_LAMBShape','*_LSPOShape'],lights = True)
    else:
    	luces = cmds.ls( filtrado , lights = True)
    datos_Dic={}
    for l in luces:
        name = cmds.listRelatives(l,type='transform',p=True)[0]
        grupo = cmds.listRelatives(name,type='transform',p=True)[0]
        lightType = cmds.nodeType(l)
        datos_Dic[name] = [lightType,l,grupo]
    lucesOrdenadas_=[]
    tiposOrdenados_=[]
    gruposOrdenados_=[]
    lucesTuplas=[]
    dicLuces_xTipo={}
    dicLuces_xGrupo={}
    # ORDENA POR NOMBRE
    if ordenarPor=='luz':
        lucesTuplas = sorted(datos_Dic.items(), key=itemgetter(0))
        for tupla in lucesTuplas:
            lucesOrdenadas_.append (tupla[0])
            tiposOrdenados_.append (tupla[1][0])
            gruposOrdenados_.append (tupla[1][2][:-5])
    ##########
    # ORDENA POR TIPO
    elif ordenarPor=='tipo':
        for key in datos_Dic.keys():
            dicLuces_xTipo[key] = datos_Dic [key][0]
            dicLuces_xGrupo[key] = datos_Dic [key][2]
        tuplas = sorted(dicLuces_xTipo.items(), key=itemgetter(1))
        for tupla in tuplas:
            lucesOrdenadas_.append (tupla[0])
            tiposOrdenados_.append (tupla[1])
            gruposOrdenados_.append (dicLuces_xGrupo [ tupla[0] ][:-5] )
    ##########
    # ORDENA POR GRUPO
    elif ordenarPor=='grupo':
        for key in datos_Dic.keys():
            dicLuces_xTipo[key] = datos_Dic [key][0]
            dicLuces_xGrupo[key] = datos_Dic [key][2]
        tuplas = sorted(dicLuces_xGrupo.items(), key=itemgetter(1))
        for tupla in tuplas:
            lucesOrdenadas_.append (tupla[0])
            gruposOrdenados_.append (tupla[1] [:-5])
            tiposOrdenados_.append (dicLuces_xTipo [ tupla[0] ] )
    return [lucesOrdenadas_,tiposOrdenados_,gruposOrdenados_]

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def construirScrollsConBotones( emparentarA='') :
    # ordenarPor puede ser 'luz' o 'tipo'.
    # emparentarA es el string del layout al que se quiere emparentar.
    lightList = cmds.ls(['*_LPNTShape','*_LDIRShape','*_LAREShape','*_LAMBShape','*_LSPOShape'],lights = True)
    dicLuces={}
    for l in lightList:
        name = cmds.listRelatives(l,type='transform',p=True)[0]
        grupo = cmds.listRelatives(name,type='transform',p=True)[0]
        lightType = cmds.nodeType(l)
        dicLuces[name]= [lightType,l,grupo]

    r_00 = cmds.rowLayout ('r_00', nc = 3 , p = 'row1' , h = 30 , cw3 = [ 308 , 81 , 100 ] , ct3 = ["both", "both", "both" ])
    cmds.button ( l = 'LUZ' ,   align = "center" ,  c = 'ordenarLuz()'   , p = r_00 )
    cmds.button ( l = 'TIPO' ,  align = "center" ,  c = 'ordenarTipo()'  , p = r_00 )
    cmds.button ( l = 'GRUPO' , align = "center" ,  c = 'ordenarGrupo()' ,  p = r_00 )

    r_01 = cmds.rowLayout ( nc = 3 , cw3 = [ 305 , 80 , 100 ] ,  p = emparentarA )
    c_01 = cmds.columnLayout ('c_01', p = r_01 , adjustableColumn=1 )
    c_02 = cmds.columnLayout ( p = r_01 , adjustableColumn=1)
    c_03 = cmds.columnLayout ( p = r_01 , adjustableColumn=1)

    cmds.textScrollList('listaLuces1' , w = 300 , allowMultiSelection=1, p = c_01 , deleteKeyCommand="borrarSeleccion()")
    cmds.textScrollList('listaLuces2' , w = 100 , allowMultiSelection = 1 , p = c_02 , bgc = [0.24,0.24,0.24] , deleteKeyCommand="borrarSeleccion()" )
    cmds.textScrollList('listaLuces3' , w = 100 , allowMultiSelection = 1 , p = c_03 , bgc = [0.24,0.24,0.24] , deleteKeyCommand="borrarSeleccion()")

    datosOrdenados = ordenarDatos(ordenarPor='luz' , filtrado='')
    cmds.textScrollList ('listaLuces1' , e=1 ,allowMultiSelection=1, a=datosOrdenados[0] , sc="refreshui('luz')" , dcc="seleccionarLuces()" ,  enable=1 ,h = (len(datosOrdenados[0])+2)*50)
    cmds.textScrollList ('listaLuces2' , e=1 ,allowMultiSelection=1, a=datosOrdenados[1] , sc="refreshui('tipo')" , dcc="seleccionarLuces()"  , enable=1 ,                       h = (len(datosOrdenados[0])+2)*50 )
    cmds.textScrollList ('listaLuces3' , e=1 ,allowMultiSelection=1, a=datosOrdenados[2] , sc="refreshui('grupo')" , dcc="seleccionarLuces()"  , enable=1 ,                      h = (len(datosOrdenados[0])+2)*50 )

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

def lightListPanel():
	global dicLuces
	global orden
	global grupo_
	try:
		import UTILITIES
		UTILITIES.arnoldON()
	except:
		cmds.warning ("NO SE PUDO IMPORTAR UTILITIES")
		cmds.warning ("NO SE PUDO PRENDER ARNOLD")
	lightList = cmds.ls(['*_LPNTShape','*_LDIRShape','*_LAREShape','*_LAMBShape','*_LSPOShape'],lights = True)
	arnoldLightList = []
	dicLuces={}
	if cmds.window('winMLuces',exists=True):
		cmds.deleteUI('winMLuces')
	win = cmds.window('winMLuces', title="PH_LUCES! v1.0 BETA - COMPATIBLE CON ARNOLD -", menuBar=0 , w=100 , s=0, height= 100, resizeToFitChildren=True)

	col_0 = cmds.columnLayout('col_0', p=win)
	cmds.separator(h=5,w=10,hr=0,p=col_0,st="none")
	row_0 = cmds.rowLayout ('row_0',numberOfColumns = 16 , height= 30, p=col_0 )
	cmds.separator(w=3,p=row_0,st="none")
	b_sel = cmds.iconTextButton ('b_sel',ann='(·)SELECCIONAR - (··)DESELECCIONAR',style='iconOnly',image1='selectObject.png',hi='selectObject.png', c = 'seleccionarLuces()' , dcc= 'cmds.select(cl=True)', width=25,height=25,p=row_0, bgc=(0.4,0.4,0.4),font= "fixedWidthFont")
	b_filtroSpot = cmds.iconTextButton  ('b_filtroLSPO',ann='SPOT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LSPO_1.png',hi='M:\PH_SCRIPTS\ICONS\LSPO_1.png', c = partial(filtrado,"LSPO") ,width=25,height=25,p=row_0, dcc=partial(add_light,"spot") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroPoint = cmds.iconTextButton ('b_filtroLPNT',ann='POINT',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LPNT_1.png',hi='M:\PH_SCRIPTS\ICONS\LPNT_1.png', c = partial(filtrado,"LPNT") , width=25,height=25,p=row_0, dcc=partial(add_light,"point") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroArea = cmds.iconTextButton  ('b_filtroLARE',ann='AREA',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LARE_1.png',hi='M:\PH_SCRIPTS\ICONS\LARE_1.png', c = partial(filtrado,"LARE") ,width=25,height=25,p=row_0, dcc=partial(add_light,"area") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_filtroDir = cmds.iconTextButton   ('b_filtroLDIR',ann='DIRECTIONAL',style='iconOnly',image1='M:\PH_SCRIPTS\ICONS\LDIR_1.png',hi='M:\PH_SCRIPTS\ICONS\LDIR_1.png', c = partial(filtrado,"LDIR") ,width=25,height=25,p=row_0, dcc=partial(add_light,"dir") ,bgc=(0.2,0.2,0.2),font= "fixedWidthFont")
	b_all = cmds.button  ('b_filtrotodos',ann='TOGGLE FILTROS TODOS', label="TODAS",width=55,height=25,p=row_0,c='tglTodos()',bgc=(0.2,0.2,0.2) )
	cmds.separator ( hr=0 , w=40 , p = row_0 )
	grupo_crear = cmds.button ( l="CREAR GRP" , c="crearGrupo()" , ann="CREA UN GRUPO DE LUZ CON EL NOMBRE ESPECIFICADO", bgc=[0.7,0.7,0.7] , p = row_0 )
	grupo_ = cmds.optionMenuGrp ( 'oM_grupo',    bgc = [0.1,0.1,0.1] , changeCommand = 'cambiarGrupo()' , p = row_0)
	cmds.separator ( hr=0 , w=32 , p = row_0 )
	buscador = cmds.textField ( 'buscador' , text = "Buscador" , p = row_0 , changeCommand = "buscar()" , pht="Buscador" , receiveFocusCommand = "borrarBuscador()")# vcc = "buscar()" ,
	col = cmds.columnLayout(p=win,h=30)
	row1 = cmds.rowLayout ( 'row1' , parent = col, numberOfColumns = 2 , columnWidth = [(1,200),(2,100)], height = 30  )
	cmds.separator ( p = col )
	scroll = cmds.scrollLayout( 'scroll',parent = win , childResizable = 1, width = 520 , h=200)
	columnScroll = cmds.rowLayout( 'columnScroll', rowAttach = [2, "top", 0]  , numberOfColumns = 4 ,p=scroll, nbg = 1)
	for l in lightList:
		name = cmds.listRelatives(l,type='transform',p=True)[0]
		grupo = cmds.listRelatives(name,type='transform',p=True)[0]
		lightType = cmds.nodeType(l)
		dicLuces[name]= [lightType,l,grupo]
	construirScrollsConBotones ( emparentarA=scroll )
	frame_1 = cmds.frameLayout('frame_1', label='ATRIBUTOS', borderStyle='in',collapsable=1,p=win , h=150 , w=520 )
	clearOptionMenu (grupo_)
	gruposDeLuces = cmds.ls ( '*_LGRP' , type='transform' )
	for grp in gruposDeLuces:
		cmds.menuItem(parent=(grupo_ +'|OptionMenu'), label=grp[:-5] )
	row_3 = cmds.rowLayout ( p=frame_1 , numberOfColumns=20 , h=30 )
	cmds.separator(p=row_3 ,w=40 , st= "none")
	cmds.text(label='       Int      ' , p = row_3 , ann="INTENSITY")
	cmds.text(label='     Exp    ' , p = row_3 , ann="EXPOSURE")
	cmds.text(label='       Rad     ' , p = row_3 , ann="aiRADIUS")
	cmds.text(label='     Ang   ' , p = row_3 , ann="aiANGLE")
	cmds.text(label='      Samp    ' , p = row_3, ann="aiSAMPLES")
	cmds.separator(w=10,st= "none", p=row_3 )
	cmds.text(label='  Col  ' , p=row_3 , ann="COLOR")
	cmds.separator(w=7,st= "none", p=row_3 )
	cmds.text(label='iDef ' , p=row_3 , ann="ILLUMINATES BY DEFAULT")
	cmds.separator(w=2,st= "none", p=row_3 )
	cmds.text(label='  eDif  ' , p=row_3, ann="EMIT DIFFUSE")
	cmds.text(label='  eSpe  ' , p=row_3 , ann="EMIT SPECULAR" )
	cmds.text(label=' ColT ' , ann="COLOR TEMPERATURE", p=row_3)

	row_2 = cmds.rowLayout ( p=frame_1  , numberOfColumns=18 , h=30 , bgc=[0.5,0.5,0.5])
	cmds.separator(p=row_2 ,w=40, st= "none")
	cmds.floatField( 'intensity' ,  en = 0 , precision = 1,  w = 50 , changeCommand = "setInt()"  ,  p = row_2 )
	cmds.floatField('aiExposure' , en=0, precision = 2, w=50 , changeCommand = "setExp()"  , p = row_2 )
	cmds.floatField('aiRadius' , en=0,precision = 2,  w=50 , changeCommand = "setRad()" , p = row_2 )
	cmds.floatField('aiAngle' , en=0,precision = 2, w=50 , changeCommand = "setAng()" , p= row_2 )
	cmds.floatField('aiSamples' , en=0,precision = 2,  w=50 , changeCommand = "setSamp()"  , p = row_2  )
	cmds.separator(w=10,st= "none", p=row_2 )
	cmds.colorSliderGrp( 'color' , en=0,  cw2 = (25, 0), changeCommand = "setColor()"  , p=row_2)
	cmds.separator(w=7,st= "none", p=row_2 )
	cmds.checkBox ('C_ilumDef' ,en=0, l='' , w=13 ,h=20 , changeCommand = "setilumDef()"  , p=row_2  )
	cmds.separator(w=16,st= "none", p=row_2 )
	cmds.checkBox ('emitDiffuse' ,en=0, l='' , w=13 ,h=20 , changeCommand = "setDif()"  , p=row_2 )
	cmds.separator(w=17,st= "none", p=row_2 )
	cmds.checkBox ('emitSpecular' ,en=0, l='' , w=13 ,h=20  , changeCommand = "setSpec()"   , p=row_2 )
	cmds.separator(w=13,st= "none", p=row_2 )
	cmds.colorSliderGrp( 'aiColorTemperature' , en=0, cw2 = (20, 0), changeCommand = "setSamp()" , p=row_2)

	row_5 = cmds.rowLayout ( p=frame_1  , numberOfColumns=1 , h=20 , cal=[1,"center"])
	cmds.radioCollection('radioAbsRel')
	rowDeColumnas=cmds.rowLayout (nc=2,co2=[200,0],ct2=["left", "left"], p=row_5)
	row_AbsRel = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton( 'A',label='ABS', sl=1,ann="ABSOLUTO",cl='radioAbsRel')
	row_ventanaCrearLuz = cmds.columnLayout( p = rowDeColumnas )
	cmds.radioCollection()
	cmds.radioButton('R', label='REL', ann="RELATIVO",cl='radioAbsRel')
	cmds.window('winMLuces', e=1 , height= 350, w=500,resizeToFitChildren=True)

	cmds.showWindow(win)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

ultimoOrden="luz" #VARIABLE LOCAL PARA EL SWITCH DEL ORDEN DE LAS LUCES
orden = {"luz":0,"tipo":0,"grupo":0} #DICCIONARIO PARA SABER SI LAS VECES DE TOCAR EL BOTON SON PARES O INPARES

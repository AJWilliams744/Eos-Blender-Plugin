import bpy
import eos
import numpy as np
import bmesh
from enum import Enum
import random

import random

baseLocation = "D:/Users/Alex/Documents/Personal/Uni/Diss/WorkFolder/eos/out/install/x86-Debug/"
maxSlider = 20

class ShapeKeeper(): # Create a dictionary with the path to model as key, model and value. check against mysetting property of locations 
    base = ""
    path = ""

class SliderType(Enum):
    Shape = 0
    Colour = 1
    Expression = 2

aShapeKeeper = ShapeKeeper()

def getCoefficients(o):

    shapeCount = o.my_settings.ShapeCount
    colourCount = o.my_settings.ColourCount
    expressionCount = o.my_settings.ExpressionCount

    if len(o.sliders.sliderList) < shapeCount + colourCount + expressionCount : return

    me = [[0.0]* shapeCount, [0.0]* colourCount, [0.0]* expressionCount]

    for x in range(0,shapeCount):            

        me[0][x] =  o.sliders.sliderList[x].value
       # print(me[x])

    
    for x in range(shapeCount,shapeCount + colourCount):           
        #print(x)
        me[1][x - shapeCount] =  o.sliders.sliderList[x].value
        #print(me[x])

    #print("-------------------------------------------")
    for x in range(shapeCount + colourCount,shapeCount + colourCount + expressionCount):            
        #print(x)
        me[2][x - shapeCount - colourCount] =  o.sliders.sliderList[x].value
        #print(me[x])

    return me

def refreshColours(mesh, coloursLocation, colours):

    #print(colours)

    if not mesh.vertex_colors:
        mesh.vertex_colors.new()

    colour_layer = mesh.vertex_colors['Col']

    #print(colours)
    #print(len(mesh.polygons))
    #print(len(mesh.vertices))

    i = 0
    x = 0

    ax = 0

    for poly in mesh.polygons:

        vertexLocation = coloursLocation[x]

        for loop in poly.loop_indices:
            color = [colours[vertexLocation[0]][0],colours[vertexLocation[1]][1],colours[vertexLocation[2]][2],1.0]
            colour_layer.data[i].color = color
            i += 1
            pass
        x += 1

    return None

def refreshColoursBM(mesh, coloursLocation, colours, shouldSmooth):

    bm = bmesh.new()
    bm.from_mesh(mesh)

    if not bm.loops.layers.color:
        bm.loops.layers.color.new("color")

    colour_layer =  bm.loops.layers.color['color']

    #print(colours)
    #print(len(mesh.polygons))
    #print(len(mesh.vertices))

    i = 0
    x = 0

    for face in bm.faces:

        vertexLocation = coloursLocation[x]
        face.smooth = shouldSmooth

        i = 0
        for loop in face.loops:
            color = [colours[vertexLocation[i]][0],colours[vertexLocation[i]][1],colours[vertexLocation[i]][2],1.0]
            loop[colour_layer] = color
            i += 1
           
        x += 1

    bm.to_mesh(mesh)

    return None

def createVertexMaterial():

    mat = bpy.data.materials.new(name = "VertexColourMat")

    refreshVertexMaterial(mat)

    return mat

def refreshVertexMaterial(mat):

    #bpy.data.node_groups.clear()
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    outputNode = ""

    links.clear()
    nodes.clear()

    vertexColour = nodes.new(type = "ShaderNodeVertexColor")    

    diffuse = nodes.new(type = "ShaderNodeBsdfDiffuse")
    output = nodes.new( type = "ShaderNodeOutputMaterial")

    links.new(diffuse.outputs["BSDF"], output.inputs["Surface"])
    links.new(vertexColour.outputs["Color"], diffuse.inputs["Color"])

def setMaterial(obj):
    mat = bpy.data.materials.get("VertexColourMat")

    if(mat is None):
        mat = createVertexMaterial()
    else:
        refreshVertexMaterial(mat)
        
    
    if(not obj.data.materials):
        obj.data.materials.append(mat)
        

    return

def smoothObject(mesh, shouldSmooth):
    for f in mesh.polygons:
        f.use_smooth = shouldSmooth          
    return

def changedSmooth(self, context):
    obj = bpy.context.object
    mesh = obj.data
    smoothObject(mesh, obj.my_settings.SmoothShader)
    pass

def refreshModel(sliderObj):

    #if aShapeKeeper.base == "": return

    o = bpy.context.object

    if(o.my_settings.IsReseting): return 

    shouldSmooth = o.my_settings.SmoothShader

    coofficient = getCoefficients(o)

    if not(coofficient) : return
    
    mesh = o.data

    if not(aShapeKeeper.base):
        loadFaceModel()
        return

    morphModel = aShapeKeeper.base.draw_sample(coofficient[0],coofficient[2],coofficient[1])

    if((sliderObj.sliderType == SliderType.Colour.value or not mesh.vertex_colors) and o.my_settings.ColourCount != 0):
        refreshColoursBM(mesh, morphModel.tci, morphModel.colors,shouldSmooth)

    else:       

        i = 0

        mesh.clear_geometry()

        verts = morphModel.vertices
        edges = []
        faces = morphModel.tvi

        mesh.from_pydata(verts, edges, faces) 
        
        if(o.my_settings.ColourCount == 0) :  
            smoothObject(mesh, shouldSmooth)
            
        #print(o.my_settings.ColourCount)

        refreshColoursBM(mesh, morphModel.tci, morphModel.colors,shouldSmooth)
   
def resize(self, context): 
    refreshModel(self)
    return

def createBlenderMesh(mesh):
    blendObj = bpy.data.meshes.new("Morphable Object")  # add the new mesh    
    obj = bpy.data.objects.new(blendObj.name, blendObj)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = mesh.vertices
    edges = []
    faces = mesh.tvi

    blendObj.from_pydata(verts, edges, faces)

    return obj

def loadFaceModel(modelPath, blendshapePath = ""):

    morphablemodel_with_expressions = ""

    #modelPath = "D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_blendshapes_with_colour.bin"
    #blendshapesPath = baseLocation + "share/expression_blendshapes_3448.bin"

    model = eos.morphablemodel.load_model(modelPath)

    #model = eos.morphablemodel.load_model(baseLocation + "share/sfm_shape_3448.bin")
    #morphablemodel_with_expressions = eos.morphablemodel.load_model(baseLocation + "share/sfm_shape_3448.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_with_colour.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/LYHM_global.bin")

    #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/4dfm_head_v1.2_blendshapes_with_colour.bin")

    print("HAS MODEL THING :")
    print(model.get_expression_model_type())

    modelType = model.get_expression_model_type()

    if(modelType == model.ExpressionModelType(0) and blendshapePath != ""):

        #print("I MADE IT HERE")
        blendshapes = eos.morphablemodel.load_blendshapes(blendshapePath)

        print(blendshapes)
        
        morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
                                                                        color_model=eos.morphablemodel.PcaModel(),
                                                                        vertex_definitions=None,
                                                                        texture_coordinates=model.get_texture_coordinates())




    #blendshapes = eos.morphablemodel.load_blendshapes(baseLocation + "share/expression_blendshapes_3448.bin")

    #print(blendshapes)
    #print("----------------------------------")
    
    #print(blendshapes)

    # 

    # morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes.get_expression_model(),
    #                                                                     color_model=eos.morphablemodel.PcaModel(),
    #                                                                     vertex_definitions=None,
    #                                                                     texture_coordinates=model.get_texture_coordinates())

    aShapeKeeper.base = model

    if(morphablemodel_with_expressions != ""):
        aShapeKeeper.base = morphablemodel_with_expressions
    else:
       return model
    
    return morphablemodel_with_expressions

def createBaseShape(FilePath, blendShapePath = ""):
    
    obj = bpy.context.object

    base = loadFaceModel(FilePath, blendShapePath)

    print(base)

    secondMesh = base.draw_sample([0,0,0],[0,0,0])

    obj = createBlenderMesh(secondMesh)

    modelType = base.get_expression_model_type()

    print("HAS other THING :")
    print(modelType)

    if(modelType == base.ExpressionModelType(0)):
        obj.my_settings.ExpressionCount = 0
        obj.my_settings.ShapeCount = 0
        obj.my_settings.ColourCount = 0

    elif(modelType == base.ExpressionModelType.Blendshapes):
        obj.my_settings.ExpressionCount = len(base.get_expression_model())
        obj.my_settings.ShapeCount = base.get_shape_model().get_num_principal_components()
        obj.my_settings.ColourCount = base.get_color_model().get_num_principal_components()

    else:
        obj.my_settings.ExpressionCount = base.get_expression_model().get_num_principal_components() 
        obj.my_settings.ShapeCount = base.get_shape_model().get_num_principal_components()
        obj.my_settings.ColourCount = base.get_color_model().get_num_principal_components()

    print(obj.my_settings.ColourCount)
    if(obj.my_settings.ColourCount != 0): setMaterial(obj)

    #print(obj.my_settings.ShapeCount)
    #print(obj.my_settings.ColourCount)
    #print(obj.my_settings.ExpressionCount)

    if not obj.get('_RNA_UI'):
        obj['_RNA_UI'] = {}

    for x in range(0,obj.my_settings.ShapeCount + obj.my_settings.ColourCount + obj.my_settings.ExpressionCount):
        prop = obj.sliders.sliderList.add()
        prop.value = 0

        if(x < obj.my_settings.ShapeCount) : 
            prop.sliderType = SliderType.Shape.value
           # print("Shape")
            continue

        if(x < obj.my_settings.ColourCount + obj.my_settings.ShapeCount ) :
            prop.sliderType = SliderType.Colour.value
            #print("Colour")
            continue

        #print("EXPRESS")
        prop.sliderType = SliderType.Expression.value

   

    #print(aShapeKeeper.base)

    return base

def getLabelText(showMore, sliderCount):

    if(sliderCount < maxSlider): return ""
    
    if(showMore): return "Hide More Sliders (" + str(sliderCount) + " / " + str(sliderCount) + ")"

    return "Show Extra Sliders (" + str(maxSlider) + " / " + str(sliderCount) + ")"

class MySettings(bpy.types.PropertyGroup):
   
    ExpressionCount : bpy.props.IntProperty(name = "ExpressionCount", description = "Number of Expressions",default = 0)
    ColourCount : bpy.props.IntProperty(name = "ColourCount", description = "Number of Colour",default = 0) 
    ShapeCount : bpy.props.IntProperty(name = "ShapeCount", description = "Number of Shapes",default = 0)   

    ColourShowMore : bpy.props.BoolProperty(name = "ColourShowMore", description = "Should I show more", default = False)
    ShapeShowMore : bpy.props.BoolProperty(name = "ShapeShowMore", description = "Should I show more", default = False)
    ExpressionShowMore : bpy.props.BoolProperty(name = "ExpressionShowMore", description = "Should I show more", default = False)

    SmoothShader : bpy.props.BoolProperty(name = "Smooth Shading", description  = "Should I smooth shade", default = False, update = changedSmooth)
    IsReseting : bpy.props.BoolProperty(name = "Reseting Slidser", default = False)

    FilePath : bpy.props.StringProperty(name = "File Path:", subtype = "FILE_PATH")
    BlendshapePath : bpy.props.StringProperty(name = "Blendshape Path:", subtype = "FILE_PATH")

    FileName : bpy.props.StringProperty(name = "File")

class GlobalSettings(bpy.types.PropertyGroup):
    GlobalFilePath : bpy.props.StringProperty(subtype = "FILE_PATH")
    GlobalBlendshapePath : bpy.props.StringProperty(name = "Blendshape Path:", subtype = "FILE_PATH")

class SliderProp(bpy.types.PropertyGroup):
    value : bpy.props.FloatProperty(name = "Length",min = -3, max = 3, description = "DataLength", default = 0, update = resize, options = {'ANIMATABLE'})
    #sliderType : bpy.props.EnumProperty(name = "SliderType", items = [("0", "Shape",""), ("1", "Expression",""), ("2", "Colour","")], default = "None")
    sliderType : bpy.props.IntProperty(name = "SliderType", description = "Int enum value for the slider type", default = 0)

class SliderList(bpy.types.PropertyGroup):
    sliderList : bpy.props.CollectionProperty(type=SliderProp)

class Create_New_Model(bpy.types.Operator):
    bl_idname = "view3d.create_new_model"
    bl_label = "Create New Model"
    bl_destription = "A button to create a new morphable face"

    def execute(self, context):

        scene = context.scene
        

        #print(scene.global_setting.GlobalFilePath[-3:])
        if(scene.global_setting.GlobalFilePath[-3:] != "bin") :
            self.report({"ERROR"}, "File not compatible")
            scene.global_setting.GlobalFilePath = ""
            return {'FINISHED'}

        blendshapePath = scene.global_setting.GlobalBlendshapePath

        if(blendshapePath[-3:] != "bin" and not blendshapePath == "") :
            self.report({"ERROR"}, "File not compatible")
            scene.global_setting.GlobalBlendshapePath = ""
            return {'FINISHED'}


        createBaseShape(scene.global_setting.GlobalFilePath, blendshapePath)
        obj = context.object

        obj.my_settings.FilePath = scene.global_setting.GlobalFilePath
        obj.my_settings.FileName = (scene.global_setting.GlobalFilePath.split("\\")[-1])[:-4]

        return {'FINISHED'}

class Create_Copy_Model(bpy.types.Operator):
    bl_idname = "view3d.create_copy_model"
    bl_label = "Create Copy Model"
    bl_destription = "A button to create a new morphable face"

    def execute(self, context):

        obj = context.object

        filePath = obj.my_settings.FilePath
        blendshapePath = obj.my_settings.BlendshapePath

        createBaseShape(filePath, blendshapePath)

        obj = context.object #Grab the new object

        obj.my_settings.FilePath = filePath
        obj.my_settings.FileName = (filePath.split("\\")[-1])[:-4]

        obj.my_settings.blendshapePath = blendshapePath
        

        return {'FINISHED'}

class Show_More_Colour(bpy.types.Operator):
    bl_idname = "view3d.show_more_colour"
    bl_label = "Show more colour sliders"
    bl_destription = "A button to show more colour sliders"

    def execute(self, context):

        obj = context.object

        obj.my_settings.ColourShowMore = not obj.my_settings.ColourShowMore

        return {'FINISHED'}
        
class Show_More_Shape(bpy.types.Operator):
    bl_idname = "view3d.show_more_shape"
    bl_label = "Show more shape sliders"
    bl_destription = "A button to show more shape sliders"

    def execute(self, context):

        obj = context.object

        obj.my_settings.ShapeShowMore = not obj.my_settings.ShapeShowMore

        return {'FINISHED'}

class Show_More_Expression(bpy.types.Operator):
    bl_idname = "view3d.show_more_expression"
    bl_label = "Show more expression sliders"
    bl_destription = "A button to show more expression sliders"

    def execute(self, context):

        obj = context.object

        obj.my_settings.ExpressionShowMore = not obj.my_settings.ExpressionShowMore

        return {'FINISHED'}

class Reset_Sliders(bpy.types.Operator):
    bl_idname = "view3d.reset_sliders"
    bl_label = "Resets all the sliders to zero"
    bl_destription = "A button to reset all the sliders"

    def execute(self, context):

        obj = context.object
        obj.my_settings.IsReseting = True # Stop the update being called during change

        for x in range(0, obj.my_settings.ShapeCount + obj.my_settings.ExpressionCount + obj.my_settings.ColourCount): 

            obj.sliders.sliderList[x].value = 0.0

        obj.my_settings.IsReseting = False

        obj.sliders.sliderList[0].value = 0.0 #Trigger the refresh

        return {'FINISHED'}

class Random_Sliders(bpy.types.Operator):
    bl_idname = "view3d.random_sliders"
    bl_label = "Randomizes all the sliders"
    bl_destription = "A button to radomize all the sliders"

    def execute(self, context):

        obj = context.object
        obj.my_settings.IsReseting = True # Stop the update being called during change

        for x in range(0, obj.my_settings.ShapeCount + obj.my_settings.ExpressionCount + obj.my_settings.ColourCount):             

            if x < obj.my_settings.ShapeCount + obj.my_settings.ColourCount:
                randomNum = (random.random() * 4) - 2
                obj.sliders.sliderList[x].value = randomNum
            else:
                randomNum = (random.random() * 0.5) - 0.1
                obj.sliders.sliderList[x].value = randomNum
                
        obj.my_settings.IsReseting = False

        obj.sliders.sliderList[0].value = (random.random() * 2) - 1 #Trigger the refresh

        return {'FINISHED'}

class Main_PT_Panel(bpy.types.Panel):
    bl_idname = "MORPH_PT_Panel"
    bl_label = "Morph Panel"
    bl_category = "Morph Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        box = layout.box()  

        isInObjectMode = True

        row = box.row()
        row.operator('view3d.create_new_model')  

        row = box.row()
        row.prop(scene.global_setting, "GlobalFilePath", text = "Model Path")

        row = box.row()
        row.prop(scene.global_setting, "GlobalBlendshapePath", text = "Blendshape Path")
        
        if(obj != None ):
            isInObjectMode = obj.mode == "OBJECT"   

        row = box.row()
       # row.label(text = "----------------------------------------------------------------------------------------------")

        if(obj != None):

            objType = getattr(obj, "type", "")

            if(objType == "MESH"):                             

                #ob = context.active_object
                
                row = box.row()
                row.label(text = "Object: " + obj.name)

                shapeCount = obj.my_settings.ShapeCount
                colourCount = obj.my_settings.ColourCount
                expressionCount = obj.my_settings.ExpressionCount    

                if(shapeCount > 0 or colourCount > 0 or expressionCount > 0):

                    row = box.row()
                    row.operator('view3d.create_copy_model')  
                    row.enabled = isInObjectMode

                    row = box.row()
                    row.prop(obj.my_settings, "FileName")
                    row.enabled = False
                    
                    row = box.row()
                    row.operator('view3d.random_sliders')
                    row.enabled = isInObjectMode

                    row = box.row()
                    row.operator('view3d.reset_sliders')
                    row.enabled = isInObjectMode
                    
                    row = box.row()
                    row.prop(obj.my_settings, "SmoothShader")
                    row.enabled = isInObjectMode       

                #row = box.row()
                #row.prop(obj.my_settings, "reverse")

                if(shapeCount > 0):

                    row = box.row()
                    row.label(text = "Shape: ")
                    row = box.row()           

                    labelText = getLabelText(obj.my_settings.ShapeShowMore, shapeCount)

                    showMoreCount = 0
                    if(obj.my_settings.ShapeShowMore): showMoreCount = shapeCount - maxSlider

                    if(labelText != ""):
                        row = box.row()
                        #labelText += " (" + str(maxSlider + showMoreCount) + " / " + str(cooCount) + ")"
                        row.operator('view3d.show_more_shape', text = labelText)  
                        row.enabled = isInObjectMode
                        row = box.row()

                    
                    cf = row.grid_flow(row_major = True, columns = 3, align = False)        
                    row.enabled = isInObjectMode    
                    for x in range(0,shapeCount):             
                        if x > maxSlider + showMoreCount: break
                        k = "line_%d" % x   
                        cf.prop(obj.sliders.sliderList[x], "value", text = str(x)+ ":")

                if(colourCount > 0):

                    row = box.row()
                    row.label(text = "Colour: ")
                    row = box.row()

                    labelText = getLabelText(obj.my_settings.ColourShowMore, colourCount)

                    showMoreCount = 0
                    if(obj.my_settings.ColourShowMore): showMoreCount = colourCount + shapeCount - maxSlider

                    if(labelText != ""):
                        row = box.row()
                        #labelText += " (" + str(maxSlider + showMoreCount) + " / " + str(colourCount) + ")"
                        row.operator('view3d.show_more_colour', text = labelText )  
                        row.enabled = isInObjectMode
                        row = box.row()

                    cf = row.grid_flow(row_major = True, columns = 3, align = False)    
                    row.enabled = isInObjectMode                 
                               
                    for x in range(shapeCount,shapeCount + colourCount):  
                        if(x - shapeCount) > maxSlider + showMoreCount : break
                        k = "line_%d" % x   
                        #print(k)
                        cf.prop(obj.sliders.sliderList[x], "value", text = str(x - shapeCount)+ ":")
                
                if(expressionCount > 0):

                    row = box.row()
                    row.label(text = "Expression: ")
                    row = box.row()

                    labelText = getLabelText(obj.my_settings.ExpressionShowMore, expressionCount)

                    if(labelText != ""):
                        row = box.row()
                        row.operator('view3d.show_more_expression', text = labelText)  
                        row.enabled = isInObjectMode
                        row = box.row()

                    cf = row.grid_flow(row_major = True, columns = 3, align = False)  
                    row.enabled = isInObjectMode

                    showMoreCount = 0

                    if(obj.my_settings.ExpressionShowMore): showMoreCount = shapeCount + colourCount + expressionCount - maxSlider

                    for x in range(shapeCount + colourCount, shapeCount + colourCount + expressionCount):             
                        if( x - shapeCount - colourCount > maxSlider + showMoreCount) : break
                        k = "line_%d" % x    
                        #cf.prop(obj, '["' + k + '"]')
                        cf.prop(obj.sliders.sliderList[x], "value", text = str(x - shapeCount - colourCount) + ":") 

classes = (
    Main_PT_Panel,
    Create_New_Model,
    Create_Copy_Model,
    MySettings,
    SliderProp,
    SliderList,
    Show_More_Colour,
    Show_More_Shape,
    Show_More_Expression,
    Reset_Sliders,
    Random_Sliders,
    GlobalSettings
        )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)   

    bpy.types.Object.my_settings = bpy.props.PointerProperty(type=MySettings)
    bpy.types.Object.sliders = bpy.props.PointerProperty(type=SliderList)
    bpy.types.Scene.global_setting = bpy.props.PointerProperty(type=GlobalSettings)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)             

if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()

  
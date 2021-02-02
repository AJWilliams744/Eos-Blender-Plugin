import bpy
import eos
import numpy as np
import bmesh

baseLocation = "D:/Users/Alex/Documents/Personal/Uni/Diss/WorkFolder/eos/out/install/x86-Debug/"


def getCoefficients(o):

    cooCount = base.get_shape_model().get_num_principal_components()
    colourCount = base.get_color_model().get_num_principal_components()

    print("ColourCount : %d", colourCount)
    expreCount = len(base.get_expression_model())

    me = [[0.0]* cooCount, [0.0]* colourCount, [0.0]* expreCount]

    for x in range(0,cooCount):            
        k = "line_%d" % x   
        me[0][x] =  getattr(o.my_settings, k)
       # print(me[x])

    for x in range(cooCount,cooCount + colourCount):            
        k = "line_%d" % x   
        me[1][x - cooCount] =  getattr(o.my_settings, k)
        #print(me[x])

    for x in range(cooCount + colourCount,cooCount + colourCount + expreCount):            
        k = "line_%d" % x   
        me[2][x - cooCount + colourCount] =  getattr(o.my_settings, k)
        #print(me[x])
    
    return me

def refreshModel():
    o = bpy.context.object

    coofficient = getCoefficients(o)

    mesh = o.data

   # bm = bmesh.new()
    #bm.from_mesh(mesh)  
    # 


    morphModel = base.draw_sample(coofficient[0],coofficient[2],coofficient[1])


   # difference = np.subtract(newVert, morphModel.vertices)

    #new_location = [0.0] * 3
    i = 0

    mesh.clear_geometry()

    verts = morphModel.vertices
    edges = []
    faces = morphModel.tvi

    mesh.from_pydata(verts, edges, faces)

    # for vert in newVert: 

    #     # vert.co = morphModel.vertices[i]
    #     i = i + 1
        
    #bm.to_mesh(mesh)
    #bm.free()    

def resize(self, context):
    refreshModel()
    return

    # o = bpy.context.object

    # coofficient = getCoefficients(o)

    # mesh = o.data

    # morphModel = base.draw_sample(coofficient,coofficient)

    # new_location = [0.0] * 3

    # i = 0

    # for vert in mesh.vertices:

    #     # new_location[0] = morphModel.vertices[i][0]
    #     # new_location[1] = morphModel.vertices[i][1]
    #     # new_location[2] = morphModel.vertices[i][2]        

    #     new_location = morphModel.vertices[i]
    #     vert.co = new_location
        
    #     # new_location[0] = new_location[0] + 1
    #     # new_location[1] = new_location[1] + 1
    #     # new_location[2] = new_location[2] + 1       

           

    #     i = i + 1

        

    # #o.dimensions.x = o.my_settings.length[]

def CreateBlenderMesh(mesh):
    blendObj = bpy.data.meshes.new("aNewMesh")  # add the new mesh    
    obj = bpy.data.objects.new(blendObj.name, blendObj)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    verts = mesh.vertices
    edges = []
    faces = mesh.tvi

    blendObj.from_pydata(verts, edges, faces)

def LoadFaceModel():
    model = eos.morphablemodel.load_model(baseLocation + "share/sfm_shape_3448.bin")
   #model = eos.morphablemodel.load_model("D:/Users/Alex/Documents/Personal/Uni/Diss/Not_OpenSource/LYHM_global.bin")

    print("HAS MODEL THING :")
    print(model.has_separate_expression_model())

    blendshapes = eos.morphablemodel.load_blendshapes(baseLocation + "share/expression_blendshapes_3448.bin")

    morphablemodel_with_expressions = eos.morphablemodel.MorphableModel(model.get_shape_model(), blendshapes,
                                                                        color_model=eos.morphablemodel.PcaModel(),
                                                                        vertex_definitions=None,
                                                                        texture_coordinates=model.get_texture_coordinates())

   
    return morphablemodel_with_expressions

def CreateBaseShape():
    
    base = LoadFaceModel()

    secondMesh = base.draw_sample([0,0,0],[0,0,0])

    CreateBlenderMesh(secondMesh)

# base = LoadFaceModel()
# cooCount = base.get_shape_model().get_num_principal_components()
# colourCount = base.get_color_model().get_num_principal_components()

# print("ColourCount : %d", colourCount)
# expreCount = len(base.get_expression_model())

class MySettings(bpy.types.PropertyGroup):
    #reverse : bpy.props.BoolProperty(name = "Direction", description = "Direction",default = False )    
    __annotations__ = {}

    __annotations__ =  {'line_%d' %x  : bpy.props.FloatProperty(name = "Length",min = -3, max = 3, description = "DataLength", default = 0, update = resize, options = {'ANIMATABLE'})
    for x in range(0,cooCount + colourCount + expreCount)}

class Shape_Slider(bpy.types.Operator):
    bl_idname = "view3d.add_frame"
    bl_label = "Create Model"
    bl_destription = "Able to create and manipulate shape key"

    def execute(self, context):

        CreateBaseShape()
            
        return {'FINISHED'}

class TEST_PT_Panel(bpy.types.Panel):
    bl_idname = "TEST_PT_Panel"
    bl_label = "Test Panel"
    bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object
        box = layout.box()      
        
        if(obj != None):


            objType = getattr(obj, "type", "")

            if(objType == "MESH"):

                row = box.row()
                row.operator('view3d.add_frame')              

                ob = context.active_object
                
                row = box.row()
                row.label(text = "Object: " + ob.name)

            

                #row = box.row()
                #row.prop(obj.my_settings, "reverse")

                if(cooCount > 0):

                    row = box.row()
                    row.label(text = "Shape")
                    row = box.row()

                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(0,cooCount):             

                        k = "line_%d" % x   
                        cf.prop(obj.my_settings, k)

                if(colourCount > 0):

                    row = box.row()
                    row.label(text = "Colour: ")
                    row = box.row()
                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(cooCount,colourCount):             

                        k = "line_%d" % x   
                        cf.prop(obj.my_settings, k)
                
                if(expreCount > 0):

                    row = box.row()
                    row.label(text = "Expression: ")
                    row = box.row()
                    cf = row.column_flow(columns = 3, align = False)            
                    for x in range(cooCount + colourCount, cooCount + colourCount + expreCount):             

                        k = "line_%d" % x   
                        cf.prop(obj.my_settings, k)

        else:
            row = box.row()
            row.operator('view3d.add_frame')    

classes = (
    TEST_PT_Panel,
    Shape_Slider,
    MySettings
        )

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)   
    bpy.types.Object.my_settings = bpy.props.PointerProperty(type=MySettings)

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

  
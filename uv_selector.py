bl_info = {
    "name": "X-Tools UV Selector",
    "author": "Vega Draco",
    "version": (1, 0),
    "blender": (3, 6, 1),
    "location": "3D Viewport > Right Sidebar (N-Bar)",
    "description": "Easy UV Selection",
    "warning": "Still Testing",
    "doc_url": "",
    "category": "UV",
}

import bpy
#import os

#def _clearconsole():
#    if os.name == "nt":
#        os.system("cls")
#    else:
#        os.system("clear")
#_clearconsole()   

class Input_Properties(bpy.types.PropertyGroup):
    tog_uv : bpy.props.BoolProperty(default=True)
    show_shortcuts : bpy.props.BoolProperty(name="Shortcuts", default=False, description="Show/Hide Shortcuts")
    objs_name : bpy.props.StringProperty(name="", description="Batch_Objects_Name", maxlen=32, default="NewName")
    uv0_name : bpy.props.StringProperty(name="", description="UV0_Name", maxlen=32, default="UV0")
    uv1_name : bpy.props.StringProperty(name="", description="UV0_Name", maxlen=32, default="UV1")
    
def _auto_name(active_uv):
    xt_prop = bpy.context.scene.xt_properties
    sel_objs = bpy.context.selected_objects
    list_obj = []
    
    def _set_active_render(ob):
        if active_uv == 0:
            ob.data.uv_layers[xt_prop.uv0_name].active_render = True
        if active_uv == 1:
            ob.data.uv_layers[xt_prop.uv1_name].active_render = True

    for obj in sel_objs:
        if obj.type == 'MESH':
            list_obj.append(obj)
    for ob in list_obj:
        uv_count = len(ob.data.uv_layers)
        if uv_count == 0:
            ob.data.uv_layers.new(name=xt_prop.uv0_name)
            ob.data.uv_layers.new(name=xt_prop.uv1_name)
            ob.data.uv_layers.active_index = active_uv
        if uv_count == 1:
            ob.data.uv_layers.active.name = xt_prop.uv0_name
            ob.data.uv_layers.new(name=xt_prop.uv1_name)
            ob.data.uv_layers.active_index = active_uv
        if uv_count > 1:
            if active_uv == 0:
                ob.data.uv_layers.active_index = active_uv
                ob.data.uv_layers.active.name = xt_prop.uv0_name
            if active_uv == 1:
                ob.data.uv_layers.active_index = active_uv
                ob.data.uv_layers.active.name = xt_prop.uv1_name
                 
        _set_active_render(ob)
    list_obj = []
                
class XT_PT_UVSelector(bpy.types.Panel):
    bl_label = "UV Selector"
    bl_idname = "LH_PT_UVSelector"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "UV Selector"
    
    def draw(self, context):
        layout = self.layout        
        scene = context.scene
        xt_prop = scene.xt_properties
#SHORTCUTS
        row=layout.row()
        row=layout.row()
        row.prop(xt_prop, 'show_shortcuts', icon='OPTIONS')
        if xt_prop.show_shortcuts:
            row=layout.row()
            row.operator('xt.toggleconsole', icon='CONSOLE')
            row.operator('xt.orphanclean', icon='FILE_REFRESH')
#BATCH RENAME
        row=layout.row()
        row.label(text="Batch Name:")
        row=layout.row()
        row.prop(xt_prop, 'objs_name', icon='OBJECT_DATA')
        row=layout.row()
        row.operator('batch_rename.btn_rename', icon='FILE_REFRESH')
        row.scale_y = 1.5
        row=layout.row()
        row.scale_y = 1.5
        row=layout.row()    
#UV RENAME        
        row.label(text="UV Names:")
        split = layout.split(align=True, factor = 0.4)
        col = split.column()
        col.scale_y = 1.0          
        col.label(text='UV Index 0:')
        col.label(text='UV Index 1:')
        
        col = split.column(align=True)
        
        col.prop(xt_prop, 'uv0_name')
        col.prop(xt_prop, 'uv1_name')
        
        row=layout.row()
        row.label(text="")
        row.scale_y = 0.1
        row=layout.row()
        
        row.label(text='Batch UV Slot Selection:')
        row=layout.row(align=False)
        if xt_prop.tog_uv == True:
            row.operator('xt.select_0', text=xt_prop.uv0_name, icon='GROUP_UVS', depress=True)
            row.operator('xt.select_1', text=xt_prop.uv1_name, icon='GROUP_UVS')
        else:
            row.operator('xt.select_0', text=xt_prop.uv0_name, icon='GROUP_UVS')
            row.operator('xt.select_1', text=xt_prop.uv1_name, icon='GROUP_UVS', depress=True)
        row.scale_y = 1.25
        row=layout.row()

class XT_OT_SELECT_0(bpy.types.Operator):
    bl_label = "slot0"
    bl_idname = 'xt.select_0'
    bl_description = "UV Index 0"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        xt_prop = context.scene.xt_properties
        xt_prop.tog_uv = True
        try:
            _auto_name(0)
        except KeyError:
            self.report({'WARNING'}, "UV layer names must have at least 1 character")
        return {'FINISHED'}
    
class XT_OT_SELECT_1(bpy.types.Operator):
    bl_label = "slot1"
    bl_idname = 'xt.select_1'
    bl_description = "UV Index 1"
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        xt_prop = context.scene.xt_properties
        xt_prop.tog_uv = False
        try:
            _auto_name(1)
        except KeyError:
            self.report({'WARNING'}, "UV layer names must have at least 1 character")
        return {'FINISHED'}

class XT_OT_BTN_RENAME(bpy.types.Operator):
    bl_label = "Batch Rename"
    bl_idname = 'batch_rename.btn_rename'
    bl_description = "Batch Rename"
    bl_options = {'REGISTER', 'UNDO'}   
    def execute(self, context):
        xt_prop = context.scene.xt_properties
        sel_objs = bpy.context.selected_objects
        new_name = xt_prop.objs_name
        obj_list = []
        if len(new_name) > 0:
            for obj in sel_objs:
                obj_list.append(obj.name)
                obj.name = new_name
                obj.data.name = new_name
            print(str(len(obj_list)) + " object names were changed to " + "'" + new_name + "'")
            obj_list = []
        return {'FINISHED'}
    
class XT_OT_ORPHANCLEAN(bpy.types.Operator):
    bl_label = "Clean Orphaned Data"
    bl_idname = 'xt.orphanclean'
    bl_description = "Clean ALL orphaned data from .blend file.  Use with caution!"
    bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        xt_prop = context.scene.xt_properties
        xt_prop.bool_orphan = False
        #bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        bpy.data.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {'FINISHED'}
    
class XT_OT_BTN_TOGGLECONSOLE(bpy.types.Operator):
    bl_label = "Toggle System Console"
    bl_idname = 'xt.toggleconsole'
    bl_description = "Toggle System Console Shortcut"
    #bl_options = {'REGISTER', 'UNDO'} 
    def execute(self, context):
        bpy.ops.wm.console_toggle()
        
        return {'FINISHED'}
       
classes = [Input_Properties,
            XT_OT_SELECT_0,
            XT_OT_SELECT_1,
            XT_PT_UVSelector,
            XT_OT_BTN_RENAME,
            XT_OT_ORPHANCLEAN,
            XT_OT_BTN_TOGGLECONSOLE,
            ]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)      
    bpy.types.Scene.xt_properties = bpy.props.PointerProperty(type = Input_Properties)
        
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls) 
    del bpy.types.Scene.xt_properties
        
if __name__ == '__main__':
    register()
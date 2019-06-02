bl_info = \
{
"name"        : "Onion DopeSheet",
"author"      : "okuma_10",
"blender"     : (2, 80, 0),
"description" : "Add toggle onion button in Dope Sheet",
"category"    : "User Interface",
"support"     : "COMMUNITY"
}

import bpy

def toggle_onion_skin():
    layers = []
    pencils = bpy.data.grease_pencils
    for pencil in pencils:
        for layer in pencil.layers:
            if layer.select:
                layers.append(layer)
    print(layers)
    for layer in layers:
        layer.use_onion_skinning = not layer.use_onion_skinning

class GP_OT_ToggleOnionSkin(bpy.types.Operator):
    bl_idname = 'gpn.toggle_onion'
    bl_label = 'Toggle Onion Skin for selected layer'

    def execute(self, context):
        toggle_onion_skin()
        return {'FINISHED'}

def add_button(self,context):
    st = context.space_data
    if st.mode == "GPENCIL":
        self.layout.operator('gpn.toggle_onion', text=" ", icon='ONIONSKIN_ON')

bpy.types.DOPESHEET_HT_header.append(add_button)

classes =\
    [
        GP_OT_ToggleOnionSkin,
    ]

register,unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
    register()
import bpy
import re

frame_numbers = set()

for pencil in bpy.data.grease_pencils:
    for layer in pencil.layers:
        for frame in layer.frames:
            frame_numbers.add(frame.frame_number)
frame_numbers = sorted(list(frame_numbers))

context = bpy.context.area.type

bpy.context.area.type = "VIEW_3D" 
render_path = bpy.context.scene.render.filepath
opened_file_path = bpy.data.filepath
find_file_name = re.search(r'\S\\.*\\(.*).blend$',opened_file_path)
scene_name = find_file_name.group(1)


for frame in frame_numbers:
    print(frame)
    bpy.context.scene.frame_set(frame)
    bpy.context.scene.render.filepath = render_path + str(f'_{frame:0>5}')
    print(f'{bpy.context.scene.render.filepath}')
    #bpy.ops.render.opengl(animation=False, sequencer=False, write_still=True, view_context=True)
    bpy.ops.render.render(write_still = True, use_viewport = True)

bpy.context.area.type = context
bpy.context.scene.render.filepath = render_path
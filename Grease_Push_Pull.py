import bpy

def push_pull(user_input):
	control = user_input
	pencil =  bpy.data.grease_pencils
	for pen in pencil:
		layers = [layer for layer in pen.layers]
		for layer in layers:
			all_frames = [x for x in layer.frames]
			try:
				selected_frames = [x for x in layer.frames if x.select]

				# If we have selected frame/s
				if len(selected_frames) is not 0:
					first_selected = selected_frames[0]
					first_selected_id = None
					for frame in all_frames:
						if frame.frame_number == first_selected.frame_number:
							first_selected_id = all_frames.index(first_selected)

					work_frames = [frame for frame in all_frames[first_selected_id:]]

					while work_frames:
						work_frames[0].frame_number += control
						del work_frames[0]

				# If no selected keyframe
				else:
					print('non selected')
					timeline_position = bpy.data.scenes[0].frame_current
					work_frames = [frame for frame in all_frames if frame.frame_number >= timeline_position]

					while work_frames:
						work_frames[0].frame_number += control
						del work_frames[0]
			except:
				pass
		pen.update_tag(refresh = {'TIME'})
	print(f'{" End! ":=^40}\n\n')


class GFN_OT_PushPull(bpy.types.Operator):
	"""Tooltip"""
	bl_idname = "gnudge.pushpull"
	bl_label = r"Insert Empty Frame, push/pull other frames"

	insert_input = bpy.props.FloatProperty(name="Some Floating Point", default=0.0)

	def execute(self, context):
		insert_input = self.insert_input
		push_pull(insert_input)
		print(insert_input)
		return {'FINISHED'}


class GFN_PT_Grease_Nudge_Panel(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Grease Nudge"
	bl_idname = "GNGE_PT_simple"
	bl_space_type = 'DOPESHEET_EDITOR'
	bl_region_type = 'UI'
	bl_category = 'Grease Nudge'

	bpy.types.Scene.nudge_driver = bpy.props.IntProperty(default=2,min=1,max=24)


	def draw(self, context):
		layout = self.layout

		row = layout.row()
		row.label(text=' Push/Pull ')
		row.label(text=' By Frames')
		row.label(text=' Nudge')

		row = layout.row()
		row_col = row.column(align=True)
		row_col.scale_y = 2
		row_col.operator('gnudge.pushpull',text = '+').insert_input = context.scene.nudge_driver
		row_col.operator('gnudge.pushpull',text = '-').insert_input = int("-" + str(context.scene.nudge_driver))

		row_col = row.column(align=True)
		row_col.scale_x = 2
		row_col.scale_y = 4
		row_col.prop(context.scene,'nudge_driver',text='')


classes = (
			GFN_OT_PushPull,
			GFN_PT_Grease_Nudge_Panel,
		   )
register,unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
	register()

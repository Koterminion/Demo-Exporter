bl_info = {
    "name": "Demo Exporter",
    "author": "Hannah Fantasia <instagram.com/HannahFantasia>",
    "version": (2, 0),
    "blender": (4, 1, 1),
    "category": "Pipeline",
    "location": "3D Viewport",
    "description": "I made an export to Demo button for my pipeline. Comes in handy, saves minutes.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

import bpy
import shutil
import re
import os
from pathlib import Path

class Dialog_DemoExporter(bpy.types.Operator):
    """Open Dialog Box For Demo Exporter"""
    bl_idname = "pipeline.demo_exporter_dialog"
    bl_label = "Demo Exporter"
    
    ToggleIncrementalSave: bpy.props.BoolProperty(name="Toggle Incremental Save", default=False)
    
    def execute(self, context):
        if self.ToggleIncrementalSave:
            bpy.ops.wm.save_mainfile(incremental=True)
        else:
            print("Incremental Saving is off, current version will be overwritten")
        
        bpy.ops.pipeline.demo_exporter()
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class DemoExport(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "pipeline.demo_exporter"
    bl_label = "Demo Exporter"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Save your file first!")
            return {'CANCELLED'}
        
        basepath = Path(filepath).parent
        filename = Path(filepath).name
        demopath = basepath.parent / 'Demo' / filename
        
        renderpath = demopath.with_suffix('.mp4')

        # Set render settings
        scene = bpy.context.scene
        scene.render.filepath = str(renderpath)
        scene.render.image_settings.file_format = 'FFMPEG'
        scene.render.ffmpeg.format = "MPEG4"
        scene.render.ffmpeg.codec = "H264"
        scene.render.ffmpeg.use_max_b_frames = False
        scene.render.ffmpeg.constant_rate_factor = 'NONE'
        scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'
        scene.render.ffmpeg.video_bitrate = 500
        scene.render.ffmpeg.maxrate = 500
        scene.render.ffmpeg.minrate = 0
        scene.render.ffmpeg.buffersize = 224 * 8
        scene.render.ffmpeg.packetsize = 2048
        scene.render.ffmpeg.muxrate = 10080000
        scene.render.ffmpeg.audio_codec = "MP3"
        scene.render.ffmpeg.audio_channels = "STEREO"
        scene.render.ffmpeg.audio_bitrate = 192
        scene.render.ffmpeg.audio_mixrate = 48000

        # Check if the 3D view is in camera mode
        camera_toggled = any(
            c.spaces[0].region_3d.view_perspective == "CAMERA" 
            for c in bpy.context.screen.areas if c.type == 'VIEW_3D'
        )
        
        if not camera_toggled:
            bpy.ops.view3d.view_camera()

        # Hide overlays and render animation
        bpy.context.space_data.overlay.show_overlays = False
        bpy.ops.render.opengl(animation=True)
        bpy.context.space_data.overlay.show_overlays = True

        # Now, workpath should be one folder above the current `renderpath`
        renderpath_obj = Path(scene.render.filepath)
        parent_directory = renderpath_obj.parent.parent  # Go one directory above the 'Demo' folder

        # Remove version numbers (_001, _002, etc.) from the filename
        workpath_name = re.sub(r'_\d+', '', renderpath_obj.stem) + renderpath_obj.suffix
        workpath = parent_directory / workpath_name

        # Replace or copy the file to the new workpath
        if workpath.exists():
            os.remove(workpath)
        shutil.copy(str(renderpath), str(workpath), follow_symlinks=True)

        return {'FINISHED'}


class Panel_Pipeline(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Pipeline'
    bl_label = 'Panel Pipeline'
    
    def draw(self, context):
        self.layout.operator("pipeline.demo_exporter_dialog")


def register():
    bpy.utils.register_class(Dialog_DemoExporter)
    bpy.utils.register_class(DemoExport)
    bpy.utils.register_class(Panel_Pipeline)


def unregister():
    bpy.utils.unregister_class(Dialog_DemoExporter)
    bpy.utils.unregister_class(DemoExport)
    bpy.utils.unregister_class(Panel_Pipeline)


if __name__ == "__main__":
    register()

bl_info = {
    "name": "Demo Exporter",
    "author": "Hannah Fantasia <instagram.com/HannahFantasia>",
    "version": (2,0),
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
        
        ToggleIncrementalSave: bpy.props.BoolProperty(name = "Toggle Incremental Save", default = False)
        
        def execute(self,context):
        
            
            bpy.ops.wm.save_mainfile(incremental=True) if self.ToggleIncrementalSave == True else print("Incremental Saving is off, current version will be overwritten")
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
        
        path = bpy.path.abspath("//").split("\\")
        filenumber = bpy.data.filepath.split("\\")
        path[-2] = 'Demo'
        path[-1] = filenumber[-1]
        demopath = '\\'.join(path)
        filename = Path(demopath)
        renderpath = filename.with_suffix('.mp4')
        scene = bpy.context.scene
        bpy.data.scenes["Scene"].render.filepath = str(renderpath)

        camera_toggled = []
        for c in bpy.context.screen.areas:
            if c.type == 'VIEW_3D':
                camera_toggled = c.spaces[0].region_3d.view_perspective == "CAMERA"
        if camera_toggled == True:
            pass
        else:
            bpy.ops.view3d.view_camera()

        bpy.context.space_data.overlay.show_overlays = False
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.ffmpeg.codec = "H264"
        bpy.context.scene.render.ffmpeg.use_max_b_frames = False
        bpy.context.scene.render.ffmpeg.constant_rate_factor = 'NONE'
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = 'REALTIME'
        bpy.context.scene.render.ffmpeg.video_bitrate = 500
        bpy.context.scene.render.ffmpeg.maxrate = 500
        bpy.context.scene.render.ffmpeg.minrate = 0
        bpy.context.scene.render.ffmpeg.buffersize = 224 * 8
        bpy.context.scene.render.ffmpeg.packetsize = 2048
        bpy.context.scene.render.ffmpeg.muxrate = 10080000

        bpy.context.scene.render.ffmpeg.audio_codec = "MP3"
        bpy.context.scene.render.ffmpeg.audio_channels = "STEREO"
        bpy.context.scene.render.ffmpeg.audio_bitrate = 192
        bpy.context.scene.render.ffmpeg.audio_mixrate = 48000

        bpy.ops.render.opengl(animation=True)
        bpy.context.space_data.overlay.show_overlays = True
        
        workpath = bpy.data.scenes["Scene"].render.filepath
        workpath = workpath.split("\\")
        workpath.pop(-2)
        workpath[-1] = re.sub(r'\_\d+', '', workpath[-1])
        workpath = '\\'.join(workpath)
        
        os.remove(workpath) if os.path.isfile(workpath) == True else print("Creating workfile")
        shutil.copy(renderpath,workpath,follow_symlinks = True)
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
if __name__ == "__main__":
    register()

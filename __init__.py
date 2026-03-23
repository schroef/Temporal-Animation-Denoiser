bl_info = {
    "name": "Temporal Animation Denoiser",
    "author": "Rombout Versluijs, ArtisticRender",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "Render > Denoise > Temporal Denoiser",
    "description": "Denoises render or EXR image sequence using build Temporal Denoiser",
    "wiki_url": "https://github.com/schroef/Temporal-Animation-Denoiser",
    "tracker_url": "https://github.com/schroef/Temporal-Animation-Denoiser/issues",
    "category": "Render",
}

# ArtisticRender
# https://artisticrender.com/how-to-denoise-an-animation-in-blender-using-temporal-denoising/

import bpy
import os 
import glob
from bpy.types import Panel, Menu, PropertyGroup
from bpy.props import (
    EnumProperty, StringProperty, BoolProperty, IntProperty, PointerProperty, FloatProperty, FloatVectorProperty
)

def renderTemporalAnimation(context):
    prefs = context.preferences
    scene = context.scene
    viewlayer = context.view_layer
    cycles = viewlayer.cycles
    ta_settings = context.scene.qs_TemporalAnimation

    # data = ['use_pass_vector', 'denoising_store_passes']
    # try:
    if not viewlayer.use_pass_vector:
        viewlayer.use_pass_vector = True
    if not cycles.denoising_store_passes:
        cycles.denoising_store_passes = True
    if not prefs.view.show_developer_ui:
        prefs.view.show_developer_ui = True

    # ta_settings.renderoutputpath = 
    scene.render.image_settings.use_exr_interleave = True
    path = ta_settings.renderoutputpath +'-####'
    scene.render.filepath = path
    scene.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'

    ta_settings.setupTemporal = True

    return True
    # bpy.ops.render.render(animation=True, use_viewport=True)
    # except Exception as error:
    #     return error

def denoiseTemporalAnimation(context):
    ta_settings = context.scene.qs_TemporalAnimation
    
    # try:
    inputpath = ta_settings.inputpath #"/Users/admin/Desktop/_Blender/Junkshop/"
    outputpath = ta_settings.outputpath #"/Users/admin/Desktop/_Blender/Junkshop/Denoised_"
    os.chdir(inputpath)
    myfiles=(glob.glob("*.exr"))
    for file in myfiles:
        print(inputpath + file + " to " + outputpath + file)
        bpy.ops.cycles.denoise_animation(input_filepath=(inputpath + file), output_filepath=(outputpath + 'Denoised_'+file))
    return True
    # except Exception as error:
    #     return error


class QS_OP_SetupTemporalAnimation(bpy.types.Operator):
    """This sets up the render settings so we can use Temporal Animation denoise operator. It sets the render ouput to mulit-layer exr and use vector pass and denoise data."""
    bl_idname = "qs.setup_temporal_animation"
    bl_label = "Setup Temporal"

    @classmethod
    def poll(cls, context):
        ta_settings = context.scene.qs_TemporalAnimation
        return ta_settings.renderoutputpath != ""

    def execute(self, context):
        output = renderTemporalAnimation(context)
        if output:
            self.report({'INFO'}, "Setup Temporal Animation Done! You can Render Animation")
        else:
            self.report({'ERROR'}, "Error '%s'" % output)
        return {'FINISHED'}


class QS_OP_DenoiseTemporalAnimation(bpy.types.Operator):
    """Denoise the pre-rendered images using Blenders Temporal Animation. It denoises the images using vector pass and denoise data."""
    bl_idname = "qs.denoise_temporal_animation"
    bl_label = "Denoise Temporal"

    @classmethod
    def poll(cls, context):
        ta_settings = context.scene.qs_TemporalAnimation
        return ta_settings.inputpath != "" and ta_settings.outputpath != ""

    def execute(self, context):
        output = denoiseTemporalAnimation(context)
        if output:
            self.report({'INFO'}, "Temporal Animation Done!")
        else:
            self.report({'ERROR'}, "Error '%s'" % output)
        return {'FINISHED'}


class QS_TemporalAnimation(PropertyGroup):
    setupTemporal : BoolProperty(
        name = "Setup Temporal",
        default=False)

    renderoutputpath : StringProperty(
        name = "Output Path",
        default='',
        subtype = 'FILE_PATH')

    inputpath : StringProperty(
        name = "Input Path",
        default='',
        subtype = 'DIR_PATH')

    outputpath : StringProperty(
        name = "Output Path",
        default='',
        subtype = 'DIR_PATH')


class CyclesButtonsPanel:
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "render"
    COMPAT_ENGINES = {'CYCLES'}

    @classmethod
    def poll(cls, context):
        return context.engine in cls.COMPAT_ENGINES


class CYCLES_RENDER_PT_temporal_denoiser(CyclesButtonsPanel, Panel):
    bl_label = "Temporal Animation Denoiser"
    bl_parent_id = 'CYCLES_RENDER_PT_sampling_render'
    bl_options = {'DEFAULT_CLOSED'}

    # def draw_header(self, context):
    #     scene = context.scene
    #     cscene = scene.cycles

    #     self.layout.prop(context.scene.cycles, "use_denoising", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        ta_settings = context.scene.qs_TemporalAnimation

        layout = layout.box()
        layout.label(text="Setup / Render Animation")
        col = layout.column(heading="Rendering")
        # col.label(text="Output Path")
        col.prop(ta_settings, "renderoutputpath")
        # if ta_settings.renderoutputpath != "":
        col.operator("qs.setup_temporal_animation")
        if ta_settings.setupTemporal:
            props = col.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
            props.animation = True
            props.use_viewport = True
        
        layout = self.layout
        layout.separator()

        layout = self.layout
        layout = layout.box()
        layout.label(text="Denoise Render")
        col = layout.column(heading="Denoising")
        col.prop(ta_settings, "inputpath")
        col.prop(ta_settings, "outputpath")
        layout.operator("qs.denoise_temporal_animation")


# SUing sub sub panels?!
class CYCLES_RENDER_PT_setup_temporal_denoise(CyclesButtonsPanel, Panel):
    bl_label = "Setup Temporal Denoise"
    bl_parent_id = 'CYCLES_RENDER_PT_temporal_denoiser'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        ta_settings = context.scene.qs_TemporalAnimation

        col = layout.column(heading="Rendering")
        # col.label(text="Output Path")
        col.prop(ta_settings, "renderoutputpath")
        # if ta_settings.renderoutputpath != "":
        layout.operator("qs.setup_temporal_animation")
        if ta_settings.setupTemporal:
            props = layout.operator("render.render", text="Render Animation", icon='RENDER_ANIMATION')
            props.animation = True
            props.use_viewport = True


class CYCLES_RENDER_PT_denoise_temporal_denoise(CyclesButtonsPanel, Panel):
    bl_label = "Denoise Animation"
    bl_parent_id = 'CYCLES_RENDER_PT_temporal_denoiser'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        ta_settings = context.scene.qs_TemporalAnimation

        col = layout.column(heading="Denoising")
        col.prop(ta_settings, "inputpath")
        col.prop(ta_settings, "outputpath")
        layout.operator("qs.denoise_temporal_animation")


classes = [
    QS_TemporalAnimation,
    CYCLES_RENDER_PT_temporal_denoiser,
    # CYCLES_RENDER_PT_setup_temporal_denoise,
    # CYCLES_RENDER_PT_denoise_temporal_denoise,
    QS_OP_DenoiseTemporalAnimation,
    QS_OP_SetupTemporalAnimation,
]

# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    # print("___________REGISTER WEIGHT PANEL_____________")
    for cls in classes:
        bpy.utils.register_class(cls)    
    
    bpy.types.Scene.qs_TemporalAnimation = PointerProperty(type=QS_TemporalAnimation)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)    

if __name__ == "__main__":
    register()

import bpy

from . import MainPanel


class MUSTARDSIMPLIFY_PT_Tools(MainPanel, bpy.types.Panel):
    bl_idname = "MUSTARDSIMPLIFY_PT_Tools"
    bl_label = "Tools"
    bl_options = {"DEFAULT_CLOSED"}

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        row = box.row()
        row.label(text="Mesh", icon="OUTLINER_DATA_MESH")
        row.operator("mustard_simplify.openlink", text="",
                     icon="QUESTION").url = "https://github.com/Mustard2/MustardSimplify/wiki#tools"
        box.operator("mustard_simplify.data_removal", text="Data Removal", icon="LIBRARY_DATA_BROKEN")


def register():
    bpy.utils.register_class(MUSTARDSIMPLIFY_PT_Tools)


def unregister():
    bpy.utils.unregister_class(MUSTARDSIMPLIFY_PT_Tools)

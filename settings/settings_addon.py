import bpy
from bpy.props import *
from .. import __package__ as base_package


# Addon preferences can be accessed with
# from .. import __package__ as base_package
# ...
# addon_prefs = bpy.context.preferences.addons[base_package].preferences
class MustardSimplify_AddonPrefs(bpy.types.AddonPreferences):
    bl_idname = base_package

    # Wiki links
    wiki: BoolProperty(name="Show Wiki/Help Buttons",
                       description="Show the Help buttons near the tools",
                       default=True)

    # Advanced options
    advanced: BoolProperty(name="Advanced Options",
                           description="Unlock Advanced Options",
                           default=False)

    # Experimental tools
    experimental: BoolProperty(default=False,
                               name="Experimental Tools",
                               description="Unlock Experimental Tools.\nSome tools might not work property or might "
                                           "impact viewport performance: use at your own risk")

    # Debug mode
    debug: BoolProperty(default=False,
                        name="Debug Mode",
                        description="Unlock Debug Mode.\nMore messaged will be generated in the "
                                    "console.\nEnable it only if you encounter problems, as it might "
                                    "degrade general Blender performance")

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.prop(self, "wiki")
        col.prop(self, "advanced")
        col.prop(self, "experimental")
        col.prop(self, "debug")

        col = layout.column(align=True)
        col.operator("mustard_simplify.reset_settings", icon="GHOST_DISABLED")

        col = layout.column(align=True)
        col.operator("mustard_simplify.openlink", text="Report Issue",
                     icon="URL").url = "https://github.com/Mustard2/MustardSimplify/issues"


def register():
    bpy.utils.register_class(MustardSimplify_AddonPrefs)


def unregister():
    bpy.utils.unregister_class(MustardSimplify_AddonPrefs)

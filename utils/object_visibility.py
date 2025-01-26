import bpy
from bpy.props import *
import time
from bpy_extras.view3d_utils import location_3d_to_region_2d
from mathutils import Vector
from bpy.app.handlers import persistent
from .. import __package__ as base_package


def occlusion_test_from_viewport(scene, depsgraph, region, space):
    # Get the active 3D Viewport's region_3d
    region_3d = space.region_3d

    hit_data = set()

    # Loop through all mesh objects in the scene
    for obj in scene.objects:
        if obj.type != 'MESH' or not obj.visible_get():
            continue

        # Get the object's world matrix
        obj_matrix_world = obj.matrix_world

        # Get the object's bounding box corners in world space
        bbox_corners = [obj_matrix_world @ Vector(corner) for corner in obj.bound_box]

        # Variable to check if any of the bounding box corners is in the viewport
        object_visible = False

        # Check each corner of the object's bounding box
        for corner in bbox_corners:
            # Convert the corner's world position to 2D screen coordinates (view space)
            screen_coords = location_3d_to_region_2d(region, region_3d, corner)

            if screen_coords:
                object_visible = True
                break  # If any corner is visible, the object is considered visible

        # If the object is visible, add it to the hit_data
        if object_visible:
            hit_data.add(obj)

    return hit_data


def find_3d_view_area():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            return area
    return None


@persistent
def update_object_visibility(scene):
    import time

    settings = scene.MustardSimplify_Settings
    addon_prefs = bpy.context.preferences.addons[base_package].preferences

    start = 0.
    if addon_prefs.debug:
        start = time.time()

    if not settings.object_visibility_animation_update:
        settings.object_visibility_overhead = time.time() - start
        return

    if settings.object_visibility_frames != 0:
        settings.object_visibility_frames += 1
        if settings.object_visibility_frames >= settings.object_visibility_frames_rate:
            settings.object_visibility_frames = 0
        return

    area = find_3d_view_area()

    if area:
        space = area.spaces.active
        region = bpy.context.region

        for obj in [x for x in scene.objects if x.MustardSimplify_ObjectVisibility]:
            obj.hide_viewport = False

        visible_objs = occlusion_test_from_viewport(scene, bpy.context.evaluated_depsgraph_get(), region,
                                                    space)

        for obj in visible_objs:
            if obj.hide_viewport:
                obj.hide_viewport = False
            obj.MustardSimplify_ObjectVisibility = False

        invisible_objs = {o for o in scene.objects if o.type == 'MESH' and o not in visible_objs}

        for obj in invisible_objs:
            if not obj.hide_viewport:
                obj.hide_viewport = True
            obj.MustardSimplify_ObjectVisibility = True

    settings.object_visibility_frames += 1

    if addon_prefs.debug:
        settings.object_visibility_overhead = time.time() - start


class MUSTARDSIMPLIFY_OT_UpdateObjectVisibility(bpy.types.Operator):
    """Update the report of execution for every modifier"""
    bl_idname = "mustard_simplify.update_object_visibility"
    bl_label = "Update Object Visibility"

    def execute(self, context):
        bpy.context.view_layer.update()
        update_object_visibility(context.scene)
        self.report({'INFO'}, 'Mustard Simplify - Object Visibility has been updated.')
        return {'FINISHED'}


def register():
    bpy.types.Object.MustardSimplify_ObjectVisibility = BoolProperty(default=False)

    bpy.utils.register_class(MUSTARDSIMPLIFY_OT_UpdateObjectVisibility)
    bpy.app.handlers.frame_change_pre.append(update_object_visibility)


def unregister():
    bpy.app.handlers.frame_change_pre.remove(update_object_visibility)
    bpy.utils.unregister_class(MUSTARDSIMPLIFY_OT_UpdateObjectVisibility)

    del bpy.types.Object.MustardSimplify_ObjectVisibility

import addon_updater_test.addon_updater_ops as addon_updater_ops
import bpy

bl_info = {
    "name": "Addon Updater Test",
    "description": "Author, import, and export data using the Industry Foundation Classes schema",
    "author": "IfcOpenShell Contributors",
    "blender": (2, 80, 0),
    "version": (0, 0, 35),
    "location": "File > Export, File > Import, Scene / Object / Material / Mesh Properties",
    "tracker_url": "https://github.com/IfcOpenShell/IfcOpenShell/issues",
    "category": "Import-Export",
}

class DemoUpdaterPanel(bpy.types.Panel):
    """Panel to demo popup notice and ignoring functionality"""
    bl_label = "Updater Demo Panel"
    bl_idname = "OBJECT_PT_addon_updater_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"

    def draw(self, context):
        layout = self.layout

        # Call to check for update in background.
        # Note: built-in checks ensure it runs at most once, and will run in
        # the background thread, not blocking or hanging blender.
        # Internally also checks to see if auto-check enabled and if the time
        # interval has passed.
        addon_updater_ops.check_for_update_background()

        layout.label(text="Demo Updater Addon")
        layout.label(text="")

        col = layout.column()
        col.scale_y = 0.7
        col.label(text="If an update is ready,")
        col.label(text="popup triggered by opening")
        col.label(text="this panel, plus a box ui")

        # Could also use your own custom drawing based on shared variables.
        if addon_updater_ops.updater.update_ready:
            layout.label(text="Custom update message", icon="INFO")
        layout.label(text="")

        # Call built-in function with draw code/checks.
        addon_updater_ops.update_notice_box_ui(self, context)


class DemoPreferences(bpy.types.AddonPreferences):
    """Demo bare-bones preferences"""
    bl_idname = __package__

    # Addon updater preferences.

    auto_check_update = bpy.props.BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False)

    updater_interval_months = bpy.props.IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0)

    updater_interval_days = bpy.props.IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        max=31)

    updater_interval_hours = bpy.props.IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23)

    updater_interval_minutes = bpy.props.IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59)

    def draw(self, context):
        layout = self.layout

        # Works best if a column, or even just self.layout.
        mainrow = layout.row()
        col = mainrow.column()

        # Updater draw function, could also pass in col as third arg.
        addon_updater_ops.update_settings_ui(self, context)

        # Alternate draw function, which is more condensed and can be
        # placed within an existing draw function. Only contains:
        #   1) check for update/update now buttons
        #   2) toggle for auto-check (interval will be equal to what is set above)
        # addon_updater_ops.update_settings_ui_condensed(self, context, col)

        # Adding another column to help show the above condensed ui as one column
        # col = mainrow.column()
        # col.scale_y = 2
        # ops = col.operator("wm.url_open","Open webpage ")
        # ops.url=addon_updater_ops.updater.website


classes = (
    DemoPreferences,
    DemoUpdaterPanel
)


def register():
    print('Super neat on update feature')
    addon_updater_ops.register(bl_info)
    for cls in classes:
        addon_updater_ops.make_annotations(cls)  # Avoid blender 2.8 warnings.
        bpy.utils.register_class(cls)
        

def unregister():
	addon_updater_ops.unregister()
	for cls in reversed(classes):
		bpy.utils.unregister_class(cls)
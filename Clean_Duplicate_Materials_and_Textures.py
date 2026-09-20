bl_info = {
    "name": "Clean Duplicate Materials and Textures",
    "author": "hellishfire",
    "version": (1, 2),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar (N) > Cleanup",
    "description": "Replaces .00x materials and textures with originals",
    "category": "Material",
}

import bpy

# Localization dictionary
translation_dict = {
    "ru_RU": {
        ("*", "Remove Duplicates (.00x)"): "Удалить дубликаты (.00x)",
        ("*", "Finds materials and images with .00x suffix, replaces with original and deletes the duplicate"): "Ищет материалы и изображения с суффиксом .00x, заменяет на оригинал и удаляет дубликат",
        ("*", "Project Cleanup"): "Очистка проекта",
        ("*", "Materials and Images:"): "Материалы и изображения:",
        ("*", "Cleaned: Materials - {}, Textures - {}"): "Очищено: Материалов - {}, Текстур - {}"
    }
}

class CLEANUP_OT_duplicates(bpy.types.Operator):
    """Finds materials and images with .00x suffix, replaces with original and deletes the duplicate"""
    bl_idname = "cleanup.remove_duplicates"
    bl_label = "Remove Duplicates (.00x)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        mats_replaced = 0
        imgs_replaced = 0
        
        # --- 1. CLEANUP MATERIALS ---
        mats_to_remove = []
        for mat in bpy.data.materials:
            # Check if name ends with '.' followed by 3 digits (e.g., .001)
            if len(mat.name) > 4 and mat.name[-4] == '.' and mat.name[-3:].isdigit():
                base_name = mat.name[:-4]
                
                # Check if the original material without numbers exists
                if base_name in bpy.data.materials:
                    original_mat = bpy.data.materials[base_name]
                    
                    # Remap all users (objects, nodes, etc.) to the original material
                    mat.user_remap(original_mat)
                    mats_to_remove.append(mat)
                    mats_replaced += 1
                    
        # Remove empty duplicate materials from data
        for mat in mats_to_remove:
            bpy.data.materials.remove(mat)

        # --- 2. CLEANUP TEXTURES (IMAGES) ---
        imgs_to_remove = []
        for img in bpy.data.images:
            if len(img.name) > 4 and img.name[-4] == '.' and img.name[-3:].isdigit():
                base_name = img.name[:-4]
                
                # Check if the original image exists
                if base_name in bpy.data.images:
                    original_img = bpy.data.images[base_name]
                    
                    # Remap all users (image texture nodes, etc.) to the original image
                    img.user_remap(original_img)
                    imgs_to_remove.append(img)
                    imgs_replaced += 1
                    
        # Remove empty duplicate images from data
        for img in imgs_to_remove:
            bpy.data.images.remove(img)

        # Output report
        # We use pgettext_iface to translate dynamic strings with formatting
        report_msg = bpy.app.translations.pgettext_iface(
            "Cleaned: Materials - {}, Textures - {}"
        ).format(mats_replaced, imgs_replaced)
        
        self.report({'INFO'}, report_msg)
        return {'FINISHED'}

class VIEW3D_PT_cleanup_panel(bpy.types.Panel):
    """Creates a panel in the 3D Viewport sidebar"""
    bl_label = "Project Cleanup"
    bl_idname = "VIEW3D_PT_cleanup_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cleanup'

    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Materials and Images:")
        layout.operator(CLEANUP_OT_duplicates.bl_idname, icon='BRUSH_DATA')

# Registration
classes = (
    CLEANUP_OT_duplicates,
    VIEW3D_PT_cleanup_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # Register our translation dictionary
    bpy.app.translations.register(__name__, translation_dict)

def unregister():
    # Unregister translation dictionary
    bpy.app.translations.unregister(__name__)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
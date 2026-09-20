# Clean Duplicate Materials & Textures

A Blender add-on that finds materials and image textures with the `.00x` suffix, remaps their users to the base data blocks, and deletes the duplicates. 

Compatibility: Blender 4.2+ (probably lower versions also will support it but I didn't check)

## Features

* **Data Remapping:** Uses the `user_remap()` API. If a mesh uses a material named `Metal.001`, the add-on assigns the `Metal` material to the mesh.
* **Texture Processing:** Applies the same logic to image textures in shader nodes (e.g., remaps `mpsu_atlas.dds.001` to `mpsu_atlas.dds`).
* **Deletion:** Removes the `.00x` data blocks from the `.blend` file after remapping. 
* **Validation:** Skips the `.00x` data block if the base data block is not present in the file.
* **Undo Support:** Operations can be reverted using Ctrl+Z.
* **Localization:** Contains English and Russian interface text.

## Installation

1. Download the `Clean_Duplicate_Materials_and_Textures.py` file.
2. Open Blender and navigate to Edit > Preferences > Add-ons.
3. Select Install from Disk (using the drop-down menu in the top right corner).
4. Select the downloaded `.py` file and click Install from Disk.
5. Enable the add-on by checking its checkbox.

## Usage

1. Open the 3D Viewport.
2. Press N to open the Sidebar.
3. Open the Cleanup tab.
4. Click the Remove Duplicates (.00x) button.
5. View the Info area at the bottom of the interface for the count of processed materials and textures.

Or you can run it via script panel in Blender

## License

MIT License. See the LICENSE file for details.

"""
Rename skeletal mesh bones to MetaHuman naming convention.

Pattern: strip trailing _<digits> suffix from each bone name.
Special case: _rootJoint -> root

Run this inside Blender's scripting tab with the armature selected.
"""

import bpy
import re


def strip_suffix(name: str) -> str:
    if name == "_rootJoint":
        return "root"
    # Remove trailing underscore + digits (e.g. _0106, _04, _00)
    return re.sub(r'_\d+$', '', name)


def rename_bones():
    armature_obj = None

    # Try active object first
    if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE':
        armature_obj = bpy.context.active_object
    else:
        # Fall back to first armature in the scene
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                armature_obj = obj
                break

    if armature_obj is None:
        print("ERROR: No armature found in the scene.")
        return

    print(f"Processing armature: {armature_obj.name}")

    renamed = []
    skipped = []
    conflicts = []

    armature = armature_obj.data
    existing_names = {bone.name for bone in armature.bones}

    for bone in armature.bones:
        original = bone.name
        new_name = strip_suffix(original)

        if new_name == original:
            skipped.append(original)
            continue

        if new_name in existing_names and new_name != original:
            conflicts.append((original, new_name))
            continue

        bone.name = new_name
        existing_names.discard(original)
        existing_names.add(new_name)
        renamed.append((original, new_name))

    print(f"\n--- Rename complete ---")
    print(f"Renamed : {len(renamed)}")
    for old, new in renamed:
        print(f"  {old}  ->  {new}")

    if skipped:
        print(f"\nSkipped (no suffix to strip): {len(skipped)}")
        for name in skipped:
            print(f"  {name}")

    if conflicts:
        print(f"\nConflicts (target name already exists): {len(conflicts)}")
        for old, new in conflicts:
            print(f"  {old}  ->  {new}  [SKIPPED]")


rename_bones()

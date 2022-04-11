import os
from random import random
import bpy
import bmesh
import numpy as np
from bpy.types import Operator
from bpy.props import FloatVectorProperty, IntVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from mathutils import Matrix
bpy.app.debug = True
bpyscene = bpy.context.scene

primitive = 'cone'
seed = 4
# variables
#count = np.random.randint(10,30)
count = 10

# loop through all the objects in the scene
for ob in bpyscene.objects:
    if ob.type == 'MESH':
        # make the current object active and select it
        bpyscene.objects.active = ob
        ob.select = True

ob = bpy.context.active_object




# modifier = object.modifiers.new(name="Fracture", frac_algorithm='BOOLEAN_FRACTAL')
bpy.ops.object.modifier_add(type='FRACTURE')
md = ob.modifiers["Fracture"]
md.fracture_mode = 'PREFRACTURED'
md.frac_algorithm = 'BOOLEAN_FRACTAL'
md.fractal_cuts = 2
md.fractal_iterations = 4
md.shard_count = count
md.point_seed = random()  # random seed

bpy.ops.object.fracture_refresh(reset=True)
bpy.ops.object.rigidbody_convert_to_objects()


folder = os.path.abspath("C:\\Users\\mathi\\OneDrive\\Studium\\ETH\\MA2\\3D Vision\\Project\\Old Project\\3D_learned_Object_reassembly\\object_fracturing\\data\\")
name = primitive + "_" + str(count) + "_seed_" + str(seed)
path = os.path.join(folder, name)
os.makedirs(path, exist_ok=True)

bpy.ops.object.select_all(action='DESELECT')    
scene = bpy.context.scene
for ob in scene.objects:
    scene.objects.active = ob
    ob.select = True

    if ob.type == 'MESH':
        bpy.ops.export_scene.obj(
                filepath=os.path.join(path, ob.name + '.obj'),
                use_selection=True,
                )
    ob.select = False
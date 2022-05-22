import argparse
import os
import tkinter
from tkinter import filedialog

from compas.geometry import Line

from compas_vis import compas_show
from fractured_object import FracturedObject

here = os.path.dirname(os.path.abspath(__file__))
path = "data_from_pred/"

visualize = False #True
vis_idx = (1, 3)


def full_reassembly(obj):
    obj.create_random_pose()
    obj.apply_random_transf()
    compas_show(obj.kpts, obj.fragments)
    obj.find_transformations()
    obj.create_inverse_transformations_for_existing_pairs()
    obj.tripplet_matching(1.0, 10.0)
    obj.find_final_transforms()

    if visualize:
        compas_show(obj.kpts, obj.fragments)


def pairwise_reassembly(obj):
    obj.create_random_pose()
    obj.apply_random_transf()
    print(obj.kpt_matches_gt)
    for key in obj.kpt_matches_gt:
        if vis_idx and sorted(key) != sorted(vis_idx):
            continue
        A = key[0]
        B = key[1]
        matches_AB = obj.kpt_matches_gt[key]
        if matches_AB:
            A_indices = matches_AB[0]
            B_indices = matches_AB[1]
            assert len(A_indices) == len(B_indices), "unequal length"
            line_list = []
            for i in range(0, len(A_indices)):
                line = Line(obj.kpts[A][A_indices[i]], obj.kpts[B][B_indices[i]])
                line_list.append(line)

            keypoints = {
                A: obj.kpts[A],
                B: obj.kpts[B]
            }
            fragments = {
                A: obj.fragments[A],
                B: obj.fragments[B]
            }
            if visualize or (A, B) == vis_idx or (B, A) == vis_idx:
                print(f"Visualizing {A, B}, scrambled.")
                compas_show(keypoints, fragments, line_list)
            obj.find_transformations()
            obj.apply_transf(A, B)

            line_list = []
            for i in range(0, len(A_indices)):
                line = Line(obj.kpts[A][A_indices[i]], obj.kpts[B][B_indices[i]])
                line_list.append(line)

            keypoints = {
                A: obj.kpts[A],
                B: obj.kpts[B]
            }
            fragments = {
                A: obj.fragments[A],
                B: obj.fragments[B]
            }
            if visualize or (A, B) == vis_idx or (B, A) == vis_idx:
                print(f"Visualizing {A, B}, matched.")
                compas_show(keypoints, fragments, line_list)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir')
    args = parser.parse_intermixed_args()

    if not args.data_dir:
        data_dir = tkinter.Tk()
        data_dir.withdraw()
        data_dir = filedialog.askdirectory(parent=data_dir, initialdir=os.getcwd(),
                                           title='Please select the parent directory of the fractured object folders')
    else:
        data_dir = args.data_dir

    obj = FracturedObject(path=data_dir, graph_matching_method='mst')
    obj.load_object()
    obj.load_gt()
    # full_reassembly(obj)
    pairwise_reassembly(obj)

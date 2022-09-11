"""Codete task"""
import os
import shutil
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from random import randint


def delete_and_create_output_folder(output_folder):
    """ Delete output folder and then create it once again"""
    cwd = os.getcwd()
    output_folder = os.path.join(cwd, output_folder)
    # deleting output folder if exists
    if os.path.exists(output_folder):
        print(f"Removing directory: {output_folder}")
        shutil.rmtree(output_folder, ignore_errors= True)
    # creating an output folder
    if not os.path.exists(output_folder):
        print(f"Creating directory: {output_folder}")
        os.mkdir(output_folder)


def generate_fragments(image, bounding_box, n, size, inside, output_folder, plot):
    """Generate <n> fragments of <size> from <image> into <output_folder>"""
    def compare_points(first_coords, second_coodrs):
        "Compare wheter the first rectangle is inside the second one"
        left  = second_coodrs[0] <= first_coords[0] and first_coords[0] <= second_coodrs[2]
        upper = second_coodrs[1] <= first_coords[1] and first_coords[1] <= second_coodrs[3]
        right = second_coodrs[0] <= first_coords[2] and first_coords[2] <= second_coodrs[2]
        lower = second_coodrs[1] <= first_coords[3] and first_coords[3] <= second_coodrs[3]
        return (left or right) and (upper or lower)
    
    def generate_random_box(boundaries, size):
        """ Generate random box """
        left = randint(boundaries[0], boundaries[2]-size)
        right = randint(boundaries[1], boundaries[3]-size)
        return (left, right, left+size, right+size)

    delete_and_create_output_folder(output_folder)
    
    coords_list = []
    if inside is True:
        boundaries = (bounding_box[0][0], bounding_box[1][1], bounding_box[1][0], bounding_box[0][1])
    else:
        w,h = image.size
        boundaries = (0, 0, w, h)
        coords_list.append((bounding_box[0][0], bounding_box[1][1], bounding_box[1][0], bounding_box[0][1]))
    img_gen_number = 0
    while img_gen_number < n:
        coord = generate_random_box(boundaries, size)
        unique = True
        for item in coords_list:
            if compare_points(first_coords=coord, second_coodrs=item): # checking if unique squares are created
                unique = False
                break
        if unique:
            coords_list.append(coord)
            rectangle = Rectangle((coord[0],coord[1]), coord[2]-coord[0], coord[3]-coord[1], linewidth=2, edgecolor='b', facecolor='none')
            plot.add_patch(rectangle)
            cropped_image = image.crop(generate_random_box(boundaries, size))
            save_name = f"{img_gen_number}_cropped_cat.jpg"
            save_path = os.path.join(output_folder, save_name)
            cropped_image.save(save_path)
            img_gen_number += 1


def main():
    image = Image.open('cat.jpg')
    bounding_box = ((200, 730), (630, 120))
    n = 100
    size = 30
    inside = True
    output_folder = 'output'
    fig, ax = plt.subplots()
    ax.imshow(image)
    ax.xaxis.set_ticks_position('top')
    width = bounding_box[1][0] - bounding_box[0][0]
    height = bounding_box[1][1] - bounding_box[0][1]
    rect = Rectangle(bounding_box[0], width, height, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    generate_fragments(image, bounding_box, n, size, inside, output_folder, ax)
    plt.show()


if __name__ == "__main__":
    main()

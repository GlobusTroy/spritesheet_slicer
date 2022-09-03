#!/usr/bin/env python3
import argparse
from typing import Sequence, Tuple
from PIL import Image


parser = argparse.ArgumentParser(description='Slice a grid-based spritesheet')
parser.add_argument('input_file', type=str, default=None, help='Path to input file containing spritesheet to slice')
parser.add_argument('grid_size', type=str, default=None, help='Size of grid; use comma to specify cols,rows; use a single integer for pixels per square grid cell.')
parser.add_argument('query', type=str, default=None, help='Query string to use for spritesheet cell selection')

parser.add_argument('--rows_out', type=int, default=1, help='Number of rows to use for output spritesheet')
parser.add_argument('--out', type=str, default='out.png', help='Output file containing slice of spritesheet')
args = parser.parse_args()

def construct_output_sheet(images: Sequence[Image.Image]) -> Image.Image:
    """
    Construct output image from images.
    :param images: List of images.
    :return: Output image.
    """
    assert images 
    rows = args.rows_out
    cols = len(images) // rows
    w,h = images[0].size 
    w,h = int(w),int(h)
    out = Image.new('RGBA', size=(cols*w, rows*h))
    for i, img in enumerate(images):
        out.paste(img, box=((i%cols)*w, (i//cols)*h))
    return out
   
def get_grid_cells(image: Image.Image, num_cols: int, num_rows: int) -> Sequence[Image.Image]:
    """
    Get a list of spritesheet cells for the given image.
    :param image: Image.
    :param num_cols: Number of columns.
    :param num_rows: Number of rows
    :return: List of spritesheet cells.
    """
    assert image
    images = [None for _ in range(int(num_cols) * int(num_rows))]
    image_width, image_height = image.size
    width = image_width // num_cols
    height = image_height // num_rows
    for i in range(len(images)):
        col = i % num_cols
        row = i // num_cols
        left = col * width
        upper = row * height
        right = left + width
        lower = upper + height
        coords = (left,upper,right,lower)
        images[i] = image.copy().crop(coords)
    return images

def parse_grid_size(grid_size_str: str, image_width: int, image_height: int) -> Tuple[int,int]:
    if ',' not in grid_size_str:
        pixels = int(grid_size_str)
        return int(image_width / pixels), int(image_height / pixels)
    else:
        dims = grid_size_str.split(',')
        return int(dims[0]), int(dims[1])


def parse_coord(coord_str: str, num_cols: int, to_tuple=False):    
    if ',' in coord_str:
        coords = coord_str.split(',')
        x_coord = num_cols - 1 if coords[1] == '$' else int(coords[1])
        coord_tuple = x_coord, int(coords[0])
        assert x_coord < num_cols
        return coord_tuple if to_tuple else grid_tuple_to_int(coord_tuple, num_cols)
    else:
        coord_int = int(coord_str)
        return coord_int if not to_tuple else grid_int_to_tuple(coord_int, num_cols)

def grid_int_to_tuple(i, num_cols: int):
    return i % num_cols, i // num_cols 

def grid_tuple_to_int(tuple, num_cols: int):
    return tuple[1] * num_cols + tuple[0]

def parse_grid_indices(query: str, num_cols: int) -> Sequence[int]:
    def box_select(coords, num_cols) -> Sequence[int]:
        assert coords[0][0] < coords[1][0]
        assert coords[0][1] < coords[1][1]
        out = []
        for y in range(coords[0][1], coords[1][1]+1):
            for x in range(coords[0][0], coords[1][0]+1):
                out.append(grid_tuple_to_int((x,y), num_cols)) 
        return out
    def reverse_box_select(coords, num_cols) -> Sequence[int]:
        return box_select(coords, num_cols)[::-1]
    def linear_select(coords, num_cols) -> Sequence[int]:
        start = grid_tuple_to_int(coords[0], num_cols)
        end = grid_tuple_to_int(coords[1], num_cols)
        return [i for i in range(start, end+1)]
    def reverse_linear_select(coords, num_cols) -> Sequence[int]:
        return linear_select(coords, num_cols)[::-1]
    """
    Parses a query string into a sequence of indices.
    :param query: Query string.
    :param num_cols: Number of in the image.
    :return: List of spritesheet cells by index.
    """
    out = []
    query_tokens = query.split(':')
    operations = {'%': reverse_box_select, 
                  '#': box_select,
                  '->': linear_select,
                  '<-': reverse_linear_select}
    for token in query_tokens:
        for delim, operation in operations.items():
            if not delim in token:
                continue
            coords = [parse_coord(coord, num_cols, to_tuple=True) for coord in token.split(delim)]
            out += operation(coords, num_cols)
            break
    return out


if __name__ == '__main__':
    image = Image.open(args.input_file, 'r')
    num_cols, num_rows = parse_grid_size(args.grid_size, image.width, image.height)
    indices_to_use = parse_grid_indices(args.query, num_cols)
    print(indices_to_use)
    image_grid_arr = get_grid_cells(image, num_cols, num_rows)
    images_to_use = [image_grid_arr[i] for i in indices_to_use]
    output = construct_output_sheet(images_to_use)    
    output.save(args.out, format='png')

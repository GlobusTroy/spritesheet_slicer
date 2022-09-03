# spritesheet_slicer
Take a sprite sheet as input, interpret it as a grid of images, and select images from the grid to output to a sprite sheet. Use to extract animations from a sprite sheet into their own file for easier asset loading.

## Usage
slicer.py [input_filepath] [grid_specification] [query] --out [output_filepath] --rows_out [num rows in output image (default=1)]

### grid specification
Can be either:
* an integer, specifying the number of pixels along the side of one square grid cell (rows/columns calculated automatically) 
* a pair of integers, num_cols,num_rows specifying the size of the sprite sheet grid (pixel size calculated automatically)

### query
* A string containing any number of query tokens separated by ';'.
* A query has 2 coordinates and an operator in between them. Ex: 5->8
* Coordinates can be specified as 
    * ROW,COLUMN (0-indexed integers). Grid coordinates of cell
        * '$' can be used to mean the last column in the row
    * i (0-indexed integer). Index of cell if grid is scanned from left to right starting from the top row.
* Operators:
    * '#': Select a box of grid cells scanning left to right starting from the top. Ex: 2,2#4,4
    * '%': Select a box of grid cells scanning right to left from bottom to top (reverse order '#')
    * '->': Select all grid cells in a linear scan of the whole base grid, from the start coordinate to the end coordinate.
    * '<-': Select all grid cells in a linear scan of the whole base grid, from the end coordinate to start coordinate in reverse (reverse order '->').

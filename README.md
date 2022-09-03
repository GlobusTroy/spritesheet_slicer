# spritesheet_slicer
Take a sprite sheet as input, interpret it as a grid of images, and select images from the grid to output to a sprite sheet. Use to extract animations from a sprite sheet into their own file for easier asset loading.

## Usage
slicer.py [input_filepath] [grid_specification] [query] --out [output_filepath] --rows_out [num rows in output image (default=1)]

### grid specification
Can be either:
* an integer, specifying the number of pixels along the side of one square grid cell (rows/columns calculated automatically) 
* a pair of integers, num_cols,num_rows specifying the size of the sprite sheet grid (pixel size calculated automatically)

## Query Format
* Coordinates can be specified as 
    * ROW,COLUMN (0-indexed)
        * '$' can be used to mean the last column in the row
    * i (0-indexed linear number scanning Left to right, top to bottom). 
* Separate tokens with ';'
* Each token can be of any of the following forms (C = a coordinate):
    * Excel range grid specification: C#C
    * Excel range grid reverse ordering: C%C
    * Left to right start to end: C->C
    * Right to left end to start: C<-C

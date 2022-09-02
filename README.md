# spritesheet_slicer

# QUERY FORMAT
* Coordinates can be specified as x,y or i. Grid coordinates or linear coordinate starting at the top left, left to right and down one row and back to the left side when reaching the end of the grid column-wise.
* Separate tokens with ';'
* Each token can be of any of the following forms (C = a coordinate):
* * Excel range grid specification: C#C
* * Excel range grid reverse ordering: C%C
* * Left to right start to end: C->C
* * Right to left end to start: C<-C
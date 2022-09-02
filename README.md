# spritesheet_slicer

# QUERY FORMAT
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
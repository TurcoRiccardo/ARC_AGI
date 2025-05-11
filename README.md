# ARC_AGI
My personal solution for ARK_AGI benchmark (https://arcprize.org/)
- official repo: https://github.com/fchollet/ARC-AGI

## Packages
- representation: contains the possible representations of the grid.


## Requirements
- numpy
- matplotlib
- arc-py: (https://github.com/ikamensh/arc-py) Used to convert the original .json files to numpy arrays, view them with matplotlib.

## Description
The ARC-AGI (Abstraction and Reasoning Corpus - Artificial General Intelligence) benchmark is a dataset created by François Chollet to test AI's ability for abstract reasoning. It consists of a series of tasks based on colored grids, where the AI must infer rules and transformations from a few examples without explicit instructions.
ARC is designed to assess human-like cognitive skills such as generalization, analogy, and pattern recognition, posing a challenge for traditional machine learning models. The benchmark is considered a key test for measuring progress toward Artificial General Intelligence (AGI).

### Grid dimension
A grid can have any height or width between 1x1 and 30x30 inclusive (average height is 9 and average width is 10).

### List of Colors
- 0: Black
- 1: Blue
- 2: Red
- 3: Green
- 4: Yellow
- 5: Grey
- 6: Magenta
- 7: Orange
- 8: Cyan
- 9: Brown

## Basic Geometry and Topology concepts that the algorithm knows as priors:
- **translation:**
- **color change:**
- **rotations:**
- **Copy, repeat objects:**
- **Shape upscaling or downscaling:**
- **symmetries:** ?
- **Draw lines, connection points, orthogonal projections:** ?
- **To contain or be contained within or outside a perimeter:** ?


## Representation
We can visualize our grid with different representations

### Pixel Representation: 
We represent the colored pixels of the grid as a list of pixels, pixels can be overlapped.

We can apply different types of actions to pixels: 
- **movePixel:** moves the selected pixels of one in one direction
- **changeColorPixel:** slightly changes the color of selected pixels
- **removePixel:** removes selected pixels from the list
- **duplicatePixel:** duplicates the selected pixels
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group pixels in various ways:
- based on the order of the pixel list
- based on the reverse order of the pixel list
- based on the central pixel in the pixel list
- based on the color of the pixel
- we can select all the pixel

### Row Representation
We can represent the grid as a list of rows.

We can apply different types of actions to rows: 
- **moveRow:** moves the selected row of one in one direction
- **changeColorRow:** slightly changes the color of the colored pixels in the selected row
- **changeColorRowPixel:** slightly changes the color of the selected pixel in the selected row
- **modifyRowAdd:** add a new colored pixel in the selected row
- **modifyRowDel:** delete a colored pixel in the selected row
- **modifyRowMove:** modify the selected row by swapping two pixel
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group rows in various ways:
- based on the order of the row list
- based on the reverse order of the row list
- based on the central row in the row list
- based if the row contain a certaint color
- we can select all the row

We can select or group the components of the row in various ways:
- based on the order of the components
- based on the reverse order of the components
- based on the central components in the row
- based on the color of the components in the row
- we can select all the components in the row

### Column Representation
We can represent the grid as a list of columns.

We can apply different types of actions to columns: 
- **moveColumn:** moves the selected column of one in one direction
- **changeColorColumn:** slightly changes the color of the colored pixels in the selected column
- **changeColorColumnPixel:** slightly changes the color of the secected pixel in the selected column
- **modifyColumnAdd:** add a new colored pixel in the selected column
- **modifyColumnDel:** delete a colored pixel in the selected column
- **modifyColumnMove:** modify the selected column by swapping two pixel
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group columns in various ways:
- based on the order of the column list
- based on the reverse order of the column list
- based on the central column in the column list
- based if the column contain a certaint color
- we can select all the column

We can select or group the components of the column in various ways:
- based on the order of the components
- based on the reverse order of the components
- based on the central components in the column
- based on the color of the components in the column
- we can select all the components in the column

### Color Layer Representation
We can represent the grid as a list of layer composed of all the pixels of one color, we have a layer for color.

We can apply different types of actions to layers: 
- **moveLayer:** moves the selected layer of one in one direction
- **moveLayerPixel:** moves the selected pixel in the layer of one in one direction
- **layerUnion:** move the pixel of the selected layer in another closest layer
- **delPixelLayer:** delete a pixel in the selected layer
- **addPixelLayer:** add a new pixel in the selected layer
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group layers in various ways:
- based on the order of the color that represents the layer
- we can select all the layer

We can select or group the components of the layer in various ways:
- based on the order of the pixel in the layer
- based on the reverse order of the pixel in the layer
- based on the central pixel in the layer
- we can select all the pixels in the layer

### Rectangle Representation
We can represent the grid as a group of rectangles having the same color, rectangles can be overlapped.

We can apply different types of actions to rectangles: 
- **moveRectangle:** moves the selected rectangle of one in one direction
- **changeColorRectangle:** slightly changes the color of the selected rectangle
- **removeRectangle:** delete the selected rectangle from the rectangle list
- **duplicateRectangle:** duplicate the selected rectangle
- **changeOrder:** change the display order of the rectangles
- **scaleUpRectangle:** scale up the selected rectangle in the direction direction
- **scaleDownRectangle:** scale down the selected rectangle in the direction direction
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group rectangles in various ways:
- based on the order of the rectangle list
- based on the reverse order of the rectangle list
- based on the central rectangle in the rectangle list
- based on the color of the rectangle
- we can select all the rectangle

### Figure Representation
We can represent the grid as a group of figures having the same color, figures can be overlapped.

We can apply different types of actions to figures: 
- **moveFigure:** moves the selected figure of one in one direction
- **changeColorFigure:** slightly changes the color of the selected figure
- **addElementFigure_row:** add a element in the figure in the selected row
- **addElementFigure_column:** add a element in the figure in the selected column
- **removeElementFigure_row:** remove the element in the selected figure row
- **removeElementFigure_column:** remove the element in the selected figure column
- **duplicateFigure:** duplicate the selected figure from the figure list
- **removeFigure:** remove a figure from the figure list based on the index
- **rotateFigure:** rotate the selected figure from the figure list to the right or the left
- **mergeFigure:** merge two figures that are next to each other of the same color
- **divideFigure_row:** divide the selected figure based on the selected row
- **divideFigure_column:** divide the selected figure based on the selected column
- **changeOrder:** change the display order of the figures
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group figures in various ways:
- based on the order of the figure list
- based on the reverse order of the figure list
- based on the central figure in the figure list
- based on the color of the figure
- we can select all the figure

We can select or group the components of the figure in various ways:
- based on the order of the row in the figure
- based on the reverse order of the row in the figure
- based on the central row in the figure
- we can select all the rows in the figure

- based on the order of the column in the figure
- based on the reverse order of the column in the figure
- based on the central column in the figure
- we can select all the columns in the figure

### Color Figure Representation
We can represent the grid as a group of figures composed by pixels of different color, figures can be overlapped.

We can apply different types of actions to figures: 
- **moveFigure:** moves the selected figure of one in one direction
- **changeColorFigureBorder:** changes the color of the border of the figure index based on color
- **changeColorFigureCenter:** changes the color of the center of the figure index based on color
- **fillFigureCenter:** fill the center of the figure index based on color
- **addElementFigure_row_column:** add a element in the figure in the selected row and column
- **moveElementFigure_row_column:** move a pixel in the figure based on the direction
- **removeElementFigure_row_column:** remove the element in the figure in the selected row and column
- **duplicateFigure:** duplicate the selected figure from the figure list
- **removeFigure:** remove a figure from the figure list based on the index
- **rotateFigure:** rotate the selected figure from the figure list to the right or the left
- **mergeFigure:** merge two figures that are next to each other of the same color

- **changeOrder:** change the display order of the figures
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group figures in various ways:
- based on the order of the figure list
- based on the reverse order of the figure list
- based on the central figure in the figure list
- based on whether a figure contains a certain color
- we can select all the figure

We can select or group the components of the figure in various ways:
- based on the order of the row in the figure
- based on the reverse order of the row in the figure
- based on the central row in the figure
- we can select all the rows in the figure

- based on the order of the column in the figure
- based on the reverse order of the column in the figure
- based on the central column in the figure
- we can select all the columns in the figure

### Border Representation
We can represent the grid as a group of border having the same color having an central area, we do not allow overlapping border.

We can apply different types of actions to borders: 
- **moveBorder:** moves the selected border of one in one direction
- **changeColorBorder:** slightly changes the color of the selected border
- **changeColorCenter2:** slightly changes the color of the centrel colored pixel of the selected border
- **changeColorCenter3:** slightly changes the color of the central area of the selected border
- **modifyBorderFigure:** slightly changes the dimension of the selected border
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group borders in various ways:
- based on the order of the border list
- based on the reverse order of the border list
- based on the central border in the border list
- based on the color of the center
- we can select all the border

We can select or group the components of the border in various ways:
- based on the order of the pixel in the border
- based on the reverse order of the pixel in the border
- based on the central pixel in the border
- we can select all the pixels in the border

### first Diagonal Representation
We can represent the grid as a list of diagonal. The diagonals run from the top left vertex to the bottom right vertex, and are listed from the top right vertex to the bottom left vertex.

We can apply different types of actions to diagonals: 
- **moveDiagonal:** moves the selected diagonal of one in one direction
- **changeColorDiagonal:** slightly changes the color of the colored pixel in the selected diagonal
- **changeColorDiagonalPixel:** changes the color of the selected pixel in the diagonal index based on color
- **modifyDiagonalAdd:** add a new colored pixel in the selected diagonal
- **modifyDiagonalDel:** delete a colored pixel in the selected diagonal
- **modifyDiagonalMove:** modify the selected diagonal by swapping two pixel
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group diagonals in various ways:
- based on the order of the diagonal list
- based on the reverse order of the diagonal list
- based on the central diagonal in the diagonal list
- based if the diagonal contain a certaint color
- we can select all the diagonal

We can select or group the components of the diagonal in various ways:
- based on the order of the components
- based on the reverse order of the components
- based on the central components in the diagonal
- based on the color of the components in the diagonal
- we can select all the components in the diagonal

### second Diagonal Representation
We can represent the grid as a list of diagonal. The diagonals run from the top right vertex to the bottom left vertex, and are listed from the top left vertex to the bottom right vertex.

We can apply different types of actions to diagonals: 
- **moveDiagonal:** moves the selected diagonal of one in one direction
- **changeColorDiagonal:** slightly changes the color of the colored pixel in the selected diagonal
- **changeColorDiagonalPixel:** changes the color of the selected pixel in the diagonal index based on color
- **modifyDiagonalAdd:** add a new colored pixel in the selected diagonal
- **modifyDiagonalDel:** delete a colored pixel in the selected diagonal
- **modifyDiagonalMove:** modify the selected diagonal by swapping two pixel
- **expandGrid:** expands the grid size
- **reduceGrid:** reduce the grid size

We can select or group diagonals in various ways:
- based on the order of the diagonal list
- based on the reverse order of the diagonal list
- based on the central diagonal in the diagonal list
- based if the diagonal contain a certaint color
- we can select all the diagonal

We can select or group the components of the diagonal in various ways:
- based on the order of the components
- based on the reverse order of the components
- based on the central components in the diagonal
- based on the color of the components in the diagonal
- we can select all the components in the diagonal

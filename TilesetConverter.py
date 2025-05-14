import cv2
import numpy as np
import os

import tkinter as tk
from tkinter import filedialog

#Matrix defining positions for each square in the tilemap
SquareDefinitions = [[(6, 5),    (7, 5),     (8, 5),     (9, 5),     (1, 3),     (6, 6)],
                     [(6, 10),   (7, 10),    (8, 10),    (9, 10),    (1, 4),     (7, 6)],
                     [(5, 6),    (5, 7),     (5, 8),     (5, 9),     (2, 3),     (8, 6)],
                     [(10, 6),   (10, 7),    (10, 8),    (10, 9),    (2, 4),     (9, 6)],
                     [(2, 6),    (2, 7),     (2, 8),     (2, 9),     (11, 7),    (9, 7)],
                     [(6, 2),    (7, 2),     (8, 2),     (9, 2),     (7, 4),     (9, 8)],
                     [(6, 1),    (7, 1),     (8, 1),     (9, 1),     (4, 7),     (9, 9)],
                     [(6, 3),    (7, 3),     (8, 3),     (9, 3),     (7, 11),    (8, 9)],
                     [(1, 6),    (1, 7),     (1, 8),     (1, 9),     (3, 2),     (7, 9)],
                     [(3, 6),    (3, 7),     (3, 8),     (3, 9),     (4, 2),     (6, 9)],
                     [(1, 1),    (2, 1),     (1, 2),     (2, 2),     (4, 1),     (6, 8)],
                     [(4, 4),    (5, 4),     (4, 5),     (5, 5),     (3, 1),     (6, 7)],
                     [(10, 4),   (11, 4),    (10, 5),    (11, 5),    (3, 3),     (7, 7)],
                     [(4, 10),   (5, 10),    (4, 11),    (5, 11),    (3, 4),     (8, 7)],
                     [(10, 10),  (11, 10),   (10, 11),   (11, 11),   (4, 3),     (7, 8)]]
root = tk.Tk()
root.withdraw()

#Prompt the user to import an image for the original tilemap
file_path = filedialog.askopenfilename(title="Select tilemap you want to convert", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.dib;*.tiff;*.tif;*.jpe;*.jp2;*.pbm;*.pgm;*.ppm;*.sr;*.ras")])
#all imagetypes supported by opencv imread


def import_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    return cv2.imread(file_path, flags=cv2.IMREAD_UNCHANGED)

OriginalTilemap = import_file(file_path)
#Import the image in it's original format, preserving alpha channel


cv2.imshow("Input Tilemap", cv2.resize(OriginalTilemap, (0,0), fx=4, fy=4))
cv2.waitKey(0)
cv2.destroyAllWindows()
#Shows original tilemap for reference, could have been done better with tkitner, but I'm lazy

def cut_into_squares(image, square_size=8):
    height, width, _ = image.shape
    squares = []
    for y in range(0, height, square_size):
        SquaresRow = []
        for x in range(0, width, square_size):
            squareimg = image[y:y+square_size, x:x+square_size]
            SquaresRow.append(squareimg)
        squares.append(SquaresRow)
    return squares

squares = cut_into_squares(OriginalTilemap)
#Cut the image into tiles, put tiles in matrix


def create_converted_tilemap(squares, square_definitions, grid_sizeX=23, grid_sizeY=13, square_size=8):
# Create a blank image for the grid
    tilemap = np.zeros((grid_sizeY * square_size, grid_sizeX * square_size, 4), dtype=np.uint8)
    print(len(squares))
    print(len(square_definitions))
    for CoordinateRow, SquaresRow in zip(square_definitions, squares):
        for (x, y), square in zip(CoordinateRow, SquaresRow):
            # Calculate the position in the grid
            start_x = (x) * square_size
            start_y = (y) * square_size
            end_x = start_x + square_size
            end_y = start_y + square_size
            print(start_x, start_y, end_x, end_y)
            # Place the square in the grid
            tilemap[start_y:end_y, start_x:end_x] = square
    return tilemap
#Create a blank image of the desired resolition of the new tilemap in the improved format
#then fill it in according to the positions listed in the SquareDefinitions matrix for the improved template format

def create_reverted_tilemap(squares, square_definitions, grid_sizeX=6, grid_sizeY=15, square_size=8):
# Create a blank image for the grid
    tilemap = np.zeros((grid_sizeY * square_size, grid_sizeX * square_size, 4), dtype=np.uint8)
    print(len(squares))
    print(len(square_definitions))
    for Ypos, SquaresDefRow in enumerate(square_definitions):
        for Xpos, (x, y) in enumerate(SquaresDefRow):
            # Calculate the position in the grid
            start_x = (Xpos) * square_size
            start_y = (Ypos) * square_size
            end_x = start_x + square_size
            end_y = start_y + square_size
            print(start_x, start_y, end_x, end_y)
            # Place the square in the grid
            tilemap[start_y:end_y, start_x:end_x] = squares[y][x]
    return tilemap
#Do the same thing as the previous function, but in reverse
#Uses the index of the coordinate touples in the definition matrix to place tile in correct position for original template format

height, width, _ = OriginalTilemap.shape
if(height/width == 2.5):
    NewTilemap = create_converted_tilemap(squares, SquareDefinitions)
    cv2.imshow("Converted Tilemap (Improved Template Format)", cv2.resize(NewTilemap, (0,0), fx=4, fy=4))
else:
    NewTilemap = create_reverted_tilemap(squares, SquareDefinitions)
    cv2.imshow("Converted Tilemap (Original Template Format)", cv2.resize(NewTilemap, (0,0), fx=4, fy=4))
cv2.waitKey(0)
cv2.destroyAllWindows()
#Check if the input tilemap is in the orignal or improved format using it's aspect ratio, then pass it through appropriate conversion function, then display resulting tilemap

save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
if not save_path:
    raise ValueError("No save path provided.")
    exit(0)
cv2.imwrite(save_path, NewTilemap)
#Select save location, then save file as png.




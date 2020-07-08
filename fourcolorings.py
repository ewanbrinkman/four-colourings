from random import shuffle

# all available colors to use are stored in this list. When choosing colors for
# vertices, vertices will be given numbers that represent a color. colors[0]
# will be 1, colors[1] will be 2, and so on. A color of 0 means no color has
# been chosen yet
colors = ["red", "yellow", "green", "blue"]

# dictionary to hold all the vertex's colors and their connected vertices
vertices = {
    1: {"color": 0, "connections": [2, 6, 9, 10]},
    2: {"color": 0, "connections": [1, 3, 8]},
    3: {"color": 0, "connections": [2, 4, 8]},
    4: {"color": 0, "connections": [3, 5, 7, 8, 9, 10]},
    5: {"color": 0, "connections": [4, 6, 7]},
    6: {"color": 0, "connections": [1, 5, 7]},
    7: {"color": 0, "connections": [4, 5, 6]},
    8: {"color": 0, "connections": [2, 3, 4]},
    9: {"color": 0, "connections": [1, 4, 10]},
    10: {"color": 0, "connections": [1, 4, 9]},
}

# vertices = {
#     1: {"color": 0, "connections": [3, 7, 10, 15]},
#     2: {"color": 0, "connections": [8, 11, 16]},
#     3: {"color": 0, "connections": [1, 4, 13]},
#     4: {"color": 0, "connections": [3, 5, 13]},
#     5: {"color": 0, "connections": [4, 6, 9, 10, 11, 12, 13, 14, 15, 16]},
#     6: {"color": 0, "connections": [5, 7, 12]},
#     7: {"color": 0, "connections": [6, 1, 12]},
#     8: {"color": 0, "connections": [2, 9, 14]},
#     9: {"color": 0, "connections": [5, 8, 14]},
#     10: {"color": 0, "connections": [5, 1, 15]},
#     11: {"color": 0, "connections": [5, 2, 16]},
#     12: {"color": 0, "connections": [5, 6, 7]},
#     13: {"color": 0, "connections": [5, 3, 4]},
#     14: {"color": 0, "connections": [5, 8, 9]},
#     15: {"color": 0, "connections": [5, 1, 10]},
#     16: {"color": 0, "connections": [5, 2, 11]},
# }

vertex_nums = [i for i in vertices]
shuffle(vertex_nums)
print(vertex_nums)

# color all vertices so that all connected vertices are different colors
for vertex in vertex_nums:
    # store the colors of connected vertices
    connected_colors = []
    for conn in vertices[vertex]['connections']:
        # if the color is "0", that means a color has not been chosen yet, so
        # do not add it
        if vertices[conn]['color']:
            connected_colors.append(vertices[conn]['color'])

    # get the smallest color number, if the list is empty, that means there are
    # no chosen colors for the connected vertices yet
    smallest_color = 1
    if connected_colors:
        # go through the numbers 1, 2, 3, and 4 until a number is found that is
        # not in connected colors. This number will be the smallest color to
        # use
        for i in range(1, 5):
            if i not in connected_colors:
                smallest_color = i
                break

    # assign the color
    vertices[vertex]['color'] = smallest_color

# count how many of each color there is
color_counter = {color: 0 for color in colors}

# print out each vertex's color and count how many of each color there is
print("\nVertices And Their Colors:")
for coloured_vertex in vertices:
    # get the color for the vertex
    vertex_color = colors[vertices[coloured_vertex]['color'] - 1]

    # add the vertex color to the totals count for each color
    color_counter[vertex_color] += 1

    print(coloured_vertex, vertex_color.title())

# print out the total number of each color
print("\nTotal number of each color used:")
for color, total in color_counter.items():
    print(color.title(), ": ", total)

# all available colors to use
# when choosing colors for vertices, colors will be chosen based on numbers
# colors[0] will be 1, colors[1] will be 2, and so on
# a color of 0 means no color has been chosen yet
colors = ["red", "yellow", "green", "blue"]

# dictionary to hold all the vertex's colors and their connected vertices
# vertices = {
#     1: {"color": 0, "connections": [2, 6, 9, 10]},
#     2: {"color": 0, "connections": [1, 3, 8]},
#     3: {"color": 0, "connections": [2, 4, 8]},
#     4: {"color": 0, "connections": [3, 5, 7, 8, 9, 10]},
#     5: {"color": 0, "connections": [4, 6, 7]},
#     6: {"color": 0, "connections": [1, 5, 7]},
#     7: {"color": 0, "connections": [4, 5, 6]},
#     8: {"color": 0, "connections": [2, 3, 4]},
#     9: {"color": 0, "connections": [1, 4, 10]},
#     10: {"color": 0, "connections": [1, 4, 9]},
# }

vertices = {
    1: {"color": 0, "connections": [3, 7, 10, 15]},
    2: {"color": 0, "connections": [8, 11, 16]},
    3: {"color": 0, "connections": [1, 4, 13]},
    4: {"color": 0, "connections": [3, 5, 13]},
    5: {"color": 0, "connections": [4, 5, 9, 10, 11, 12, 13, 14, 15, 16]},
    6: {"color": 0, "connections": [5, 7, 12]},
    7: {"color": 0, "connections": [6, 1, 12]},
    8: {"color": 0, "connections": [2, 9, 14]},
    9: {"color": 0, "connections": [5, 8, 14]},
    10: {"color": 0, "connections": [5, 1, 15]},
    11: {"color": 0, "connections": [5, 2, 16]},
    12: {"color": 0, "connections": [5, 6, 7]},
    13: {"color": 0, "connections": [5, 3, 4]},
    14: {"color": 0, "connections": [5, 8, 9]},
    15: {"color": 0, "connections": [5, 1, 10]},
    16: {"color": 0, "connections": [5, 2, 11]},
}

# color all vertices so that all connected vertices are different colors
for vertex in vertices:
    # store the colors of connected vertices
    connected_colors = []
    for conn in vertices[vertex]['connections']:
        # if the color is "0", that means a color has not been chosen yet, so
        # do not add it
        if vertices[conn]['color']:
            connected_colors.append(vertices[conn]['color'])

    # get the smallest color number, if the list is empty, that means there are
    # no chosen colors for the connected vertices yet
    if connected_colors:
        smallest_color = min(connected_colors)
        # make the color number 1 if it is not taken by any connected vertices
        if smallest_color > 1 and 1 not in connected_colors:
            smallest_color = 1
        # make the color number 1 more than the largest color number
        else:
            smallest_color = max(connected_colors) + 1

    # there are no chosen colors connected, make this vertex the lowest color
    else:
        smallest_color = 1

    # assign the color
    vertices[vertex]['color'] = smallest_color

# print out each vertex's color
for coloured_vertex in vertices:
    print(coloured_vertex, colors[vertices[coloured_vertex]['color'] - 1])

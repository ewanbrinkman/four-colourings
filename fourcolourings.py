from random import shuffle

# all available colours to use are stored in this list. When choosing
# colours for vertices, vertices will be given numbers that represent a
# colour. colours[0] will be 1, colours[1] will be 2, and so on. A colour of
# 0 means no colour has been chosen yet
colours = ["red", "yellow", "green", "blue"]

# dictionary to hold all the vertex's colours and their connected vertices
vertices = {
    1: {"colour": 0, "connections": [2, 6, 9, 10]},
    2: {"colour": 0, "connections": [1, 3, 8]},
    3: {"colour": 0, "connections": [2, 4, 8]},
    4: {"colour": 0, "connections": [3, 5, 7, 8, 9, 10]},
    5: {"colour": 0, "connections": [4, 6, 7]},
    6: {"colour": 0, "connections": [1, 5, 7]},
    7: {"colour": 0, "connections": [4, 5, 6]},
    8: {"colour": 0, "connections": [2, 3, 4]},
    9: {"colour": 0, "connections": [1, 4, 10]},
    10: {"colour": 0, "connections": [1, 4, 9]},
}

# uncomment this dictionary to use this set of vertices instead
# vertices = {
#     1: {"colour": 0, "connections": [3, 7, 10, 15]},
#     2: {"colour": 0, "connections": [8, 11, 16]},
#     3: {"colour": 0, "connections": [1, 4, 13]},
#     4: {"colour": 0, "connections": [3, 5, 13]},
#     5: {"colour": 0, "connections": [4, 6, 9, 10, 11, 12, 13, 14, 15, 16]},
#     6: {"colour": 0, "connections": [5, 7, 12]},
#     7: {"colour": 0, "connections": [6, 1, 12]},
#     8: {"colour": 0, "connections": [2, 9, 14]},
#     9: {"colour": 0, "connections": [5, 8, 14]},
#     10: {"colour": 0, "connections": [5, 1, 15]},
#     11: {"colour": 0, "connections": [5, 2, 16]},
#     12: {"colour": 0, "connections": [5, 6, 7]},
#     13: {"colour": 0, "connections": [5, 3, 4]},
#     14: {"colour": 0, "connections": [5, 8, 9]},
#     15: {"colour": 0, "connections": [5, 1, 10]},
#     16: {"colour": 0, "connections": [5, 2, 11]},
# }

# the vertices are made a list so they can be shuffled
vertex_nums = [i for i in vertices]
# put the vertices in a random order for colouring, comment the next two
# lines to prevent the random shuffle
shuffle(vertex_nums)
print("Random order vertices will be coloured:", vertex_nums)

# colour all vertices so that all connected vertices are different colours
for vertex in vertex_nums:
    # store the colours of connected vertices
    connected_colours = []
    for conn in vertices[vertex]['connections']:
        # if the colour is "0", that means a colour has not been chosen yet, so
        # do not add it
        if vertices[conn]['colour']:
            connected_colours.append(vertices[conn]['colour'])

    # get the smallest colour number, if the list is empty, that means
    # there are no chosen colours for the connected vertices yet
    smallest_colour = 1
    if connected_colours:
        # go through the numbers 1, 2, 3, and 4 until a number is found that is
        # not in connected colours. This number will be the smallest colour to
        # use
        for i in range(1, 5):
            if i not in connected_colours:
                smallest_colour = i
                break

    # assign the colour
    vertices[vertex]['colour'] = smallest_colour

# count how many of each colour there is
colour_counter = {colour: 0 for colour in colours}

# print out each vertex's colour and count how many of each colour there is
print("\nVertices And Their colours:")
for coloured_vertex in vertices:
    # get the colour for the vertex
    vertex_colour = colours[vertices[coloured_vertex]['colour'] - 1]

    # add the vertex colour to the totals count for each colour
    colour_counter[vertex_colour] += 1

    print(coloured_vertex, ":", vertex_colour.title())

# print out the total number of each colour
print("\nTotal number of each colour used:")
for colour, total in colour_counter.items():
    print(colour.title(), ":", total)

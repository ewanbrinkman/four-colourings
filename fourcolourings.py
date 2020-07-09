from random import shuffle

# all available colours to use are stored in this list. When choosing
# colours for vertices, vertices will be given numbers that represent a
# colour. 1 will represent colors[0], 2 will represent colors[1], and so on. A
# colour of 0 means no colour has been chosen yet
vertex_colours = ["red", "yellow", "green", "blue"]

# dictionary to hold all the vertex's colours and their connected vertices
vertices_simple = {
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

vertices_complex = {
    1: {"colour": 0, "connections": [3, 7, 10, 15]},
    2: {"colour": 0, "connections": [8, 11, 16]},
    3: {"colour": 0, "connections": [1, 4, 13]},
    4: {"colour": 0, "connections": [3, 5, 13]},
    5: {"colour": 0, "connections": [4, 6, 9, 10, 11, 12, 13, 14, 15, 16]},
    6: {"colour": 0, "connections": [5, 7, 12]},
    7: {"colour": 0, "connections": [6, 1, 12]},
    8: {"colour": 0, "connections": [2, 9, 14]},
    9: {"colour": 0, "connections": [5, 8, 14]},
    10: {"colour": 0, "connections": [5, 1, 15]},
    11: {"colour": 0, "connections": [5, 2, 16]},
    12: {"colour": 0, "connections": [5, 6, 7]},
    13: {"colour": 0, "connections": [5, 3, 4]},
    14: {"colour": 0, "connections": [5, 8, 9]},
    15: {"colour": 0, "connections": [5, 1, 10]},
    16: {"colour": 0, "connections": [5, 2, 11]},
}


def order_vertices(vertex_numbers, random):
    if random:
        # put the vertices in a random order for colouring
        shuffle(vertex_numbers)
        print("The Vertices Will Be Coloured In A Random Order:",
              ", ".join([str(i) for i in vertex_numbers]))
    else:
        print("No Random Order Will Be Chosen For Colouring Vertices")

    return vertex_numbers


def count_colours(vertices):
    # count how many of each colour there is
    colour_counter = {i: 0 for i in range(1, 5)}
    for vertex in vertices:
        colour_counter[vertices[vertex]['colour']] += 1

    return colour_counter


def colour_vertices(vertices, random):
    # colour all vertices so that all connected vertices are different colours
    vertex_order = order_vertices(list(vertices.keys()), random)
    for vertex_number in vertex_order:
        # store the colours of connected vertices
        connected_colours = []
        for conn in vertices[vertex_number]['connections']:
            # if the colour is "0", that means a colour has not been chosen
            # yet, so do not add it
            if vertices[conn]['colour']:
                connected_colours.append(vertices[conn]['colour'])

        # get the smallest colour number, if the list is empty, that means
        # there are no chosen colours for the connected vertices yet
        smallest_colour = 1
        if connected_colours:
            # go through the numbers 1, 2, 3, and 4 until a number is found
            # that is not in connected colours. This number will be the
            # smallest colour to use
            for i in range(1, 5):
                if i not in connected_colours:
                    smallest_colour = i
                    break

        # assign the colour
        vertices[vertex_number]['colour'] = smallest_colour

    colour_counter = count_colours(vertices)

    return vertices, colour_counter


def print_vertex_colours(coloured_vertices_nums, colour_total_nums):
    # print out each vertex's colour
    print("\nVertices And Their Colours:")
    for vertex_number in coloured_vertices_nums:
        # get the colour for the vertex
        vertex_colour = vertex_colours[coloured_vertices_nums[vertex_number][
                                           'colour'] - 1]
        print(vertex_number, ":", vertex_colour.title())

    # print out the total number of each colour
    print("\nTotal Number Of Each Colour Used:")
    for colour, total in colour_total_nums.items():
        print(vertex_colours[colour - 1].title(), ":", total)


# colour the vertices so adjacent vertices all have different colours
coloured_vertices, colour_total = colour_vertices(vertices_simple, False)
# print out the result
print_vertex_colours(coloured_vertices, colour_total)


with open('day8.txt') as f:
    puzzle_image = [int(d) for d in f.read().strip()]

# reutrns [1,1,1,1,1,] into [layer,] where layer is [cols] where cols is [1,1,1,]
def layers_from(data, width, height):
    layers_out = []
    layer_start = 0
    data_index = 0
    while data_index < len(data):
        layer = [[0 for x in range(width)] for y in range(height)]
        for x in range(width):
            for y in range(height):
                layer[y][x] = data[data_index+x+(y*width)]
        data_index += width*height
        layers_out.append(layer)
    return layers_out

def count_in_layer(layer, target):
    return sum([sum(pixel == target for pixel in row) for row in layer])

def find_layer_with_fewest_zeros(layers):
    fewest_zeros = len(layers[0]) * len(layers[0][0]) + 1;
    fewest_layer = 0;
    for layer in layers:
        layer_zero_count = count_in_layer(layer, 0)
        if layer_zero_count < fewest_zeros:
            fewest_zeros = layer_zero_count
            fewest_layer = layer
    return fewest_layer
            

test_image = [1,2,3,4,5,6,7,8,9,0,1,2]
test_layers = layers_from(test_image, 3, 2)

puzzle_layers = layers_from(puzzle_image, 25, 6)
print(len(puzzle_layers))
zero_layer = find_layer_with_fewest_zeros(puzzle_layers)
print(zero_layer)
print(count_in_layer(zero_layer, 1)*count_in_layer(zero_layer, 2))

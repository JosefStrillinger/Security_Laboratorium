def disrupted_columnar_cipher(message, key):
    # Create the grid by filling it with empty spaces
    grid = [[' ' for j in range(len(key))] for i in range(len(message)//len(key) + 1)]
    # Fill the grid with the message
    for i, char in enumerate(message):
        row = i // len(key)
        col = i % len(key)
        grid[row][col] = char
    # Rearrange the columns according to the key
    new_grid = [[' ' for j in range(len(key))] for i in range(len(message)//len(key) + 1)]
    for i, col in enumerate(key):
        for j, char in enumerate(grid):
            new_grid[j][i] = char[col-1]
    # Flatten the grid to create the ciphertext
    ciphertext = ''.join([''.join(row) for row in new_grid]).replace(' ','')
    return ciphertext

#Example
message = "This is a secret message"
key = [2, 3, 4, 1]
ciphertext = disrupted_columnar_cipher(message, key)
print("Ciphertext:",ciphertext)

pltxt = disrupted_columnar_cipher(ciphertext, key)
print("test: ",pltxt)
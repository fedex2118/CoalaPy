from PIL import Image

# desired dimension of combined image
output_width = 2000  # width
output_height = 1800  # height

# image of desired size
output_image = Image.new("RGB", (output_width, output_height))

# input list
images = ["Benchmark/Load Tree (Execution Time).png",
          "Benchmark/Load Tree (Memory Usage).png",
          "Benchmark/Pre-order Traversal.png",
          "Benchmark/In-order Traversal.png",
          "Benchmark/Post-order Traversal.png",
          "Benchmark/Level-order Traversal.png"]

# dimension of each image on grid
image_width = output_width // 2
image_height = output_height // 3

for index, file in enumerate(images):
    # open image
    img = Image.open(file)
    # resize image
    img = img.resize((image_width, image_height), Image.ANTIALIAS)
    # position on grid
    x = index % 2 * image_width
    y = index // 2 * image_height
    # paste image on output
    output_image.paste(img, (x, y))

# save output
output_image.save("Benchmark/merged_diagrams.png")
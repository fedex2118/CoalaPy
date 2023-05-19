from PIL import Image

# Dimensioni desiderate per l'immagine finale
output_width = 1920  # da adattare alle tue esigenze
output_height = 1080  # da adattare alle tue esigenze

# Crea un'immagine vuota della dimensione desiderata
output_image = Image.new("RGB", (output_width, output_height))

# Lista dei file immagine
images = ["Benchmark/Load Tree (Execution Time).png",
          "Benchmark/Load Tree (Memory Usage).png",
          "Benchmark/Pre-order Traversal.png",
          "Benchmark/In-order Traversal.png",
          "Benchmark/Post-order Traversal.png",
          "Benchmark/Level-order Traversal.png"]

# Imposta le dimensioni di ciascuna immagine nella griglia
image_width = output_width // 2
image_height = output_height // 3

for index, file in enumerate(images):
    # Apre l'immagine
    img = Image.open(file)
    # Ridimensiona l'immagine
    img = img.resize((image_width, image_height))
    # Calcola la posizione dell'immagine nella griglia
    x = index % 2 * image_width
    y = index // 2 * image_height
    # Incolla l'immagine nell'immagine di output
    output_image.paste(img, (x, y))

# Salva l'immagine di output
output_image.save("Benchmark/merged_diagrams.png")
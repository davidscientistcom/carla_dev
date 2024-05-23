import pygame

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cuatro Cuadrantes")

# Cargar las imágenes
image1 = pygame.image.load("image1.jpg")
image2 = pygame.image.load("image2.jpg")
image3 = pygame.image.load("image3.jpg")
image4 = pygame.image.load("image4.jpg")

# Definir los cuadrantes
quad1 = pygame.Rect(0, 0, screen_width // 2, screen_height // 2)
quad2 = pygame.Rect(screen_width // 2, 0, screen_width // 2, screen_height // 2)
quad3 = pygame.Rect(0, screen_height // 2, screen_width // 2, screen_height // 2)
quad4 = pygame.Rect(screen_width // 2, screen_height // 2, screen_width // 2, screen_height // 2)

# Función para redimensionar las imágenes
def resize_image(image, rect):
    return pygame.transform.scale(image, (rect.width, rect.height))

# Bucle principal del juego
running = True
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limpiar la pantalla
    screen.fill((0, 0, 0))

    # Redimensionar y dibujar las imágenes en los cuadrantes
    screen.blit(resize_image(image1, quad1), quad1)
    screen.blit(resize_image(image2, quad2), quad2)
    screen.blit(resize_image(image3, quad3), quad3)
    screen.blit(resize_image(image4, quad4), quad4)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
import cv2
import multiprocessing

def show_image(image, window_name):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Lee las imágenes
    image1 = cv2.imread('image1.jpg')
    image2 = cv2.imread('image2.jpg')
    image3 = cv2.imread('image3.jpg')
    image4 = cv2.imread('image4.jpg')

    # Define los procesos para mostrar imágenes
    processes = [
        multiprocessing.Process(target=show_image, args=(image1, 'Image 1')),
        multiprocessing.Process(target=show_image, args=(image2, 'Image 2')),
        multiprocessing.Process(target=show_image, args=(image3, 'Image 3')),
        multiprocessing.Process(target=show_image, args=(image4, 'Image 4'))
    ]

    # Inicia los procesos
    for p in processes:
        p.start()

    # Espera a que todos los procesos terminen
    for p in processes:
        p.join()

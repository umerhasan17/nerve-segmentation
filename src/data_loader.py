import cv2
from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import load_img

from config import debug

from augmentation import get_random_affine_transformation


class VagusDataLoader(keras.utils.Sequence):
    """Helper to iterate over the data (as Numpy arrays)."""

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        """Returns tuple (input, target) correspond to batch #idx."""
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")

        for j, (img_path, target_path) in enumerate(zip(batch_input_img_paths, batch_target_img_paths)):
            img = load_img(img_path, target_size=self.img_size)
            annotation = np.load(target_path)
            current_transform = get_random_affine_transformation()
            augmented_img = current_transform(img)
            augmented_annotation = current_transform(annotation)
            x[j] = augmented_img
            y[j] = augmented_annotation

        # for j, path in enumerate(batch_target_img_paths):
        #     img = load_img(path, target_size=self.img_size, color_mode="grayscale")
        #     y[j] = np.expand_dims(img, 2)
        #     # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
        #     # TODO what?
        #     # y[j] -= 1
        #     annotation = y[j]
        #     threshold = 127
        #     _, annotation = cv2.threshold(annotation, threshold, 255, cv2.THRESH_BINARY)
        #     annotation = annotation.astype(float) / 255
        #     annotation = np.expand_dims(annotation, axis=2)
        #     y[j] = 1 - annotation

        if i == 0 and debug:
            print(f'Data loader first x, y pair - x shape: {x.shape}, x min max: {np.min(x)}, {np.max(x)}, y shape: {y.shape}, y values: {np.unique(y, return_counts=True)}')

        return x, y
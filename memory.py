import numpy as np

class recall:
    def __init__(self) -> None:
        labels = np.eye(3)
        images = np.array([[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 0, 0]])

        # Initialize weights for memory system
        weights = np.zeros((labels.shape[1], images.shape[1]))

        # Hebbian learning rule to store associations
        for i in range(labels.shape[0]):
            weights += np.outer(labels[i], images[i])

        # Function to recall image based on label
        def recall(label):
            return np.dot(label, weights)

        # Test recall for the first label
        reconstructed_image = recall(labels[0])
        print(reconstructed_image)

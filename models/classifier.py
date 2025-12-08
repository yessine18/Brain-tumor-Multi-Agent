"""
Brain Tumor Classification Model
Extracted from binary_classification.ipynb
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import cv2
import matplotlib.pyplot as plt
from typing import Tuple, Dict
import os

class BrainTumorClassifier:
    """Brain tumor classification using VGG19 model"""
    
    def __init__(self, model_path: str):
        """
        Initialize the classifier
        
        Args:
            model_path: Path to the trained Keras model
        """
        self.model_path = model_path
        self.model = None
        self.img_size = (224, 224)
        self.class_names = ['Normal', 'Tumor']
        
    def load_model(self):
        """Load the trained model"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        self.model = keras.models.load_model(self.model_path)
        print(f"Model loaded successfully from {self.model_path}")
        
    def preprocess_image(self, img_path: str) -> np.ndarray:
        """
        Preprocess image for model prediction
        
        Args:
            img_path: Path to the image file
            
        Returns:
            Preprocessed image array
        """
        img = image.load_img(img_path, target_size=self.img_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize to [0, 1]
        return img_array
    
    def predict(self, img_path: str) -> Dict:
        """
        Predict brain tumor classification
        
        Args:
            img_path: Path to the MRI image
            
        Returns:
            Dictionary containing prediction results
        """
        if self.model is None:
            self.load_model()
        
        # Preprocess and predict
        img_array = self.preprocess_image(img_path)
        prediction = self.model.predict(img_array, verbose=0)
        
        # Get class and confidence
        pred_class = int(prediction[0][0] > 0.5)
        confidence = float(prediction[0][0] if pred_class == 1 else 1 - prediction[0][0])
        
        result = {
            'class': self.class_names[pred_class],
            'confidence': confidence,
            'tumor_detected': pred_class == 1,
            'raw_prediction': float(prediction[0][0])
        }
        
        return result
    
    def generate_gradcam(self, img_path: str, last_conv_layer_name: str = None) -> np.ndarray:
        """
        Generate Grad-CAM heatmap for explainability
        
        Args:
            img_path: Path to the MRI image
            last_conv_layer_name: Name of the last convolutional layer
            
        Returns:
            Heatmap overlay on original image
        """
        if self.model is None:
            self.load_model()
        
        # Default layer name for VGG19
        if last_conv_layer_name is None:
            last_conv_layer_name = 'block5_conv4'
        
        # Load and preprocess image
        img_array = self.preprocess_image(img_path)
        
        # Create a model that maps the input image to the activations of the last conv layer
        grad_model = keras.models.Model(
            [self.model.inputs],
            [self.model.get_layer(last_conv_layer_name).output, self.model.output]
        )
        
        # Compute gradient of the predicted class with respect to the output feature map
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)
            loss = predictions[:, 0]
        
        # Extract gradients
        grads = tape.gradient(loss, conv_outputs)
        
        # Global average pooling
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Weight the channels by the corresponding gradients
        conv_outputs = conv_outputs[0]
        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        heatmap = heatmap.numpy()
        
        # Load original image
        original_img = cv2.imread(img_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        
        # Resize heatmap to match image size
        heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        
        # Apply colormap
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
        
        # Overlay heatmap on original image
        superimposed_img = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
        
        return superimposed_img
    
    def save_gradcam(self, img_path: str, output_path: str) -> str:
        """
        Generate and save Grad-CAM visualization
        
        Args:
            img_path: Path to the input MRI image
            output_path: Path to save the Grad-CAM visualization
            
        Returns:
            Path to the saved visualization
        """
        gradcam_img = self.generate_gradcam(img_path)
        
        plt.figure(figsize=(10, 10))
        plt.imshow(gradcam_img)
        plt.axis('off')
        plt.title('Grad-CAM: Brain Regions Influencing Classification')
        plt.tight_layout()
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        return output_path


# Convenience function for quick predictions
def classify_brain_mri(img_path: str, model_path: str) -> Dict:
    """
    Quick function to classify a brain MRI image
    
    Args:
        img_path: Path to the MRI image
        model_path: Path to the trained model
        
    Returns:
        Classification results
    """
    classifier = BrainTumorClassifier(model_path)
    return classifier.predict(img_path)

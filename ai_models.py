import numpy as np
import cv2
import tensorflow as tf
from PIL import Image

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def run_lung_inference(image):
    img = np.array(image.convert("L"))
    img = cv2.resize(img, (512, 512)).astype(np.float32) / 255.0
    img = img[np.newaxis, ..., np.newaxis]
    interpreter.set_tensor(input_details[0]["index"], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]["index"])
    return output[0, 0, :, :]

def overlay_heatmap(image, heatmap, alpha=0.5):
    heatmap = cv2.resize(heatmap, image.size)
    heatmap = np.uint8(255 * heatmap)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(np.array(image.convert("RGB")), 1 - alpha, heatmap_color, alpha, 0)
    return Image.fromarray(overlay)

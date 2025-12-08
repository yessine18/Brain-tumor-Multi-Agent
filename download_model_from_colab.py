"""
Run this in Google Colab to download your trained model
Then transfer it to your local machine
"""

# Add this cell to your Google Colab notebook and run it:
print("""
Copy and run this code in your Google Colab notebook:

# Download the trained model
from google.colab import files
import os

model_path = '/content/best_modelVGG19_brain_tumor.keras'

if os.path.exists(model_path):
    print(f"Model found at: {model_path}")
    print(f"Model size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    files.download(model_path)
    print("✅ Download started! Save it to your Desktop/MULTI-AGENT/models/ folder")
else:
    print("❌ Model not found. You may need to retrain it.")
    print("The model should be saved during training with ModelCheckpoint callback.")
""")

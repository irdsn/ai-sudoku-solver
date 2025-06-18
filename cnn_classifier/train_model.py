##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script trains an enhanced CNN model for Sudoku digit recognition using grayscale cell     #
# readme_images labeled into digits 1–9 and empty cells. It integrates data augmentation, batch         #
# normalization, and regularization techniques to improve generalization.                        #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from utils.logs_config import logger
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import CSVLogger

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "digit_model.keras")
OUTPUT_PATH = os.path.join(BASE_DIR, "results", "training")
CSV_LOG_PATH = os.path.join(OUTPUT_PATH, "training_log.csv")
PLOT_PATH = os.path.join(OUTPUT_PATH, "training_plot.png")
METRICS_PATH = os.path.join(OUTPUT_PATH, "training_metrics.json")

TRAIN_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "datasets", "train"))
VAL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "datasets", "val"))

IMG_SIZE = 64
BATCH_SIZE = 32
EPOCHS = 100

##################################################################################################
#                                TRAINING OUTPUT CONFIGURATION                                   #
#                                                                                                #
# Creates the output directory if it doesn't exist.                                              #
# Initializes a CSVLogger to record training progress epoch-by-epoch into a CSV file.            #
#                                                                                                #
# Outputs:                                                                                       #
# - training_log.csv (contains per-epoch accuracy/loss values)                                   #
# - stdout message with timestamp to indicate training start                                     #
##################################################################################################

os.makedirs(OUTPUT_PATH, exist_ok=True)

# Logs training metrics to a CSV for inspection
csv_logger = CSVLogger(CSV_LOG_PATH, append=False)

logger.info(f"🕒 Training started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

##################################################################################################
#                                     DATA PREPARATION                                           #
#                                                                                                #
# Loads training and validation readme_images from their respective directories. Images are             #
# automatically rescaled and converted to grayscale.                                             #
#                                                                                                #
# Output:                                                                                        #
# - `train_data` and `val_data`: Keras iterators for feeding the model during training.          #
##################################################################################################

# Augmentation increases the robustness of the model to small spatial and intensity variations
train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=0.1,
    shear_range=0.1
)

val_gen = ImageDataGenerator(rescale=1./255)

train_data = train_gen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_data = val_gen.flow_from_directory(
    VAL_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    color_mode="grayscale",
    class_mode="categorical",
    batch_size=BATCH_SIZE,
    shuffle=False
)

num_classes = len(train_data.class_indices)
logger.info(f"📊 Detected classes: {train_data.class_indices}")

##################################################################################################
#                                      MODEL DEFINITION                                          #
#                                                                                                #
# Defines a sequential Convolutional Neural Network (CNN) architecture with:                     #
# - Two convolutional layers followed by max-pooling                                             #
# - A dense hidden layer with dropout regularization                                             #
# - A final output layer with softmax activation for multi-class classification                  #
#                                                                                                #
# The model is compiled with:                                                                    #
# - Adam optimizer                                                                               #
# - Categorical crossentropy loss                                                                #
# - Accuracy as the evaluation metric                                                            #
##################################################################################################

# Enhanced CNN with Batch Normalization and increased depth for better generalization
model = Sequential([
    Conv2D(32, (3, 3), activation="relu", padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation="relu", padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation="relu", padding='same'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(256, activation="relu"),
    Dropout(0.5),
    Dense(num_classes, activation="softmax")
])

model.compile(optimizer=Adam(learning_rate=1e-4),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

##################################################################################################
#                                     TRAINING LOGIC                                             #
#                                                                                                #
# Trains the CNN model using the training and validation datasets.                               #
# Includes callbacks for:                                                                        #
# - ModelCheckpoint: saves the best model based on val_loss                                      #
# - EarlyStopping: stops training if no improvement in val_loss after N epochs                   #
# - CSVLogger: logs training/validation metrics to CSV                                           #
#                                                                                                #
# Output:                                                                                        #
# - Trained model saved to disk                                                                  #
# - Training history stored in `history` object                                                  #
##################################################################################################

checkpoint = ModelCheckpoint(
    MODEL_PATH,
    monitor="val_loss",
    save_best_only=True,
    verbose=1
)

early_stop = EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

history = model.fit(
    train_data,
    epochs=EPOCHS,
    validation_data=val_data,
    callbacks=[checkpoint, early_stop, csv_logger]
)

##################################################################################################
#                                     PLOT TRAINING RESULTS                                      #
#                                                                                                #
# Saves a PNG plot visualizing accuracy over epochs for both training and validation.            #
# Also writes final metrics (accuracy and loss) to a JSON file for future reference.             #
#                                                                                                #
# Outputs:                                                                                       #
# - training_plot.png: Line plot of accuracy over time                                           #
# - training_metrics.json: Final epoch summary (acc/loss, val_acc/val_loss, model path)                   #
##################################################################################################

# Save training plot
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(PLOT_PATH)
plt.close()
logger.info(f"📈 Training accuracy plot saved: {PLOT_PATH}")

# Save final metrics as JSON
metrics = {
    "epochs_trained": len(history.history['loss']),
    "final_train_accuracy": round(history.history['accuracy'][-1], 4),
    "final_val_accuracy": round(history.history['val_accuracy'][-1], 4),
    "final_train_loss": round(history.history['loss'][-1], 4),
    "final_val_loss": round(history.history['val_loss'][-1], 4),
    "model_path": MODEL_PATH
}

# Save training metrics
with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

logger.info(f"📊 Training metrics saved to: {METRICS_PATH}")
logger.info(f"🕒 Training completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

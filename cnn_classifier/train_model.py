##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script trains a Convolutional Neural Network (CNN) to classify digits 1–9 and empty cells #
# from Sudoku cell images. It uses labeled images stored in datasets/train and datasets/val,     #
# organized into class folders.                                                                  #
# The trained model is saved to cnn_classifier/model/digit_model.keras                           #
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
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import CSVLogger

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

IMG_SIZE = 64
BATCH_SIZE = 32
EPOCHS = 20
MODEL_PATH = "../cnn_classifier/model/digit_model.keras"

TRAIN_DIR = "../datasets/train"
VAL_DIR = "../datasets/val"

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

output_path = "../cnn_classifier/results/training"
os.makedirs(output_path, exist_ok=True)

# Setup CSVLogger
csv_log_path = os.path.join(output_path, "training_log.csv")
csv_logger = CSVLogger(csv_log_path, append=False)

logger.info(f"🕒 Training started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

##################################################################################################
#                                     DATA PREPARATION                                           #
#                                                                                                #
# Loads training and validation images from their respective directories. Images are             #
# automatically rescaled and converted to grayscale.                                             #
#                                                                                                #
# Output:                                                                                        #
# - `train_data` and `val_data`: Keras iterators for feeding the model during training.          #
##################################################################################################

train_gen = ImageDataGenerator(rescale=1./255)
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

model = Sequential([
    Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(128, activation="relu"),
    Dropout(0.4),
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

early_stop = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)

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
# - metrics.json: Final epoch summary (acc/loss, val_acc/val_loss, model path)                   #
##################################################################################################

# Save training plot
output_path = "..../cnn_classifier/results/training"
os.makedirs(output_path, exist_ok=True)
plot_path = os.path.join(output_path, "training_plot.png")

plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(plot_path)
plt.close()
logger.info(f"📈 Training accuracy plot saved: {plot_path}")

# Save final metrics as JSON
metrics = {
    "epochs_trained": len(history.history['loss']),
    "final_train_accuracy": round(history.history['accuracy'][-1], 4),
    "final_val_accuracy": round(history.history['val_accuracy'][-1], 4),
    "final_train_loss": round(history.history['loss'][-1], 4),
    "final_val_loss": round(history.history['val_loss'][-1], 4),
    "model_path": MODEL_PATH
}

metrics_path = os.path.join(output_path, "metrics.json")
with open(metrics_path, "w") as f:
    json.dump(metrics, f, indent=4)

logger.info(f"📊 Training metrics saved to: {metrics_path}")


logger.info(f"🕒 Training completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

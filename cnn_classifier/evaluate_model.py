##################################################################################################
#                                        SCRIPT OVERVIEW                                         #
#                                                                                                #
# This script loads the trained CNN model and evaluates its performance on the test dataset.     #
# It generates final metrics (loss, accuracy), a detailed predictions report (CSV),              #
# and a confusion matrix heatmap for visual inspection.                                          #
# Outputs are saved under cnn_classifier/results/test/                                           #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from utils.logs_config import logger
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

##################################################################################################
#                                      CONFIGURATION                                             #
#                                                                                                #
# Sets the image size, batch size, and relevant file paths for model and dataset locations.      #
# Creates the output directory to store test evaluation results and visualizations.              #
##################################################################################################

IMG_SIZE = 64
BATCH_SIZE = 32
MODEL_PATH = "model/digit_model.keras"
TEST_DIR = "../datasets/test"
OUTPUT_DIR = "results/test"

os.makedirs(OUTPUT_DIR, exist_ok=True)

##################################################################################################
#                                     EVALUATION FUNCTION                                        #
##################################################################################################

def run_evaluation():

    ##################################################################################################
    #                                      LOAD TEST DATA                                            #
    #                                                                                                #
    # Initializes an ImageDataGenerator to rescale pixel values.                                     #
    # Loads labeled test images from the test dataset directory using `flow_from_directory`.         #
    #                                                                                                #
    # Output:                                                                                        #
    # - `test_data`: batched generator of grayscale images with categorical labels.                  #
    ##################################################################################################

    test_gen = ImageDataGenerator(rescale=1./255)

    test_data = test_gen.flow_from_directory(
        TEST_DIR,
        target_size=(IMG_SIZE, IMG_SIZE),
        color_mode="grayscale",
        class_mode="categorical",
        batch_size=BATCH_SIZE,
        shuffle=False  # Important to match order
    )

    ##################################################################################################
    #                                     LOAD TRAINED MODEL                                         #
    #                                                                                                #
    # Loads the trained CNN model from the specified path.                                           #
    # This model is used to make predictions and evaluate performance on the test set.               #
    ##################################################################################################

    model = load_model(MODEL_PATH)
    logger.info(f"Loaded model from {MODEL_PATH}")

    ##################################################################################################
    #                                    EVALUATE ON TEST SET                                        #
    #                                                                                                #
    # Evaluates the model on the test dataset using Keras `.evaluate()` method.                      #
    # Saves the test loss and accuracy to a JSON file for easy reference.                            #
    #                                                                                                #
    # Output:                                                                                        #
    # - Console output of test loss and accuracy                                                     #
    # - `test_metrics.json` with structured results                                                  #
    ##################################################################################################

    loss, accuracy = model.evaluate(test_data)
    logger.info(f"💥 Test Loss: {loss:.4f}")
    logger.info(f"🎯 Test Accuracy: {accuracy:.4f}")

    # Save to JSON
    metrics = {
        "test_loss": round(loss, 4),
        "test_accuracy": round(accuracy, 4)
    }

    with open(os.path.join(OUTPUT_DIR, "test_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    ##################################################################################################
    #                              PREDICTIONS & CONFUSION MATRIX                                    #
    #                                                                                                #
    # Predicts classes for the entire test dataset and compares them with true labels.               #
    # Generates a confusion matrix to visualize performance per class.                               #
    # Creates a CSV with filename, true label, and predicted label for detailed analysis.            #
    #                                                                                                #
    # Outputs:                                                                                       #
    # - `confusion_matrix.png`: heatmap of prediction performance across all classes                 #
    # - `predictions_report.csv`: file-by-file classification summary                                #
    ##################################################################################################

    # Get true and predicted labels
    true_labels = test_data.classes
    class_labels = list(test_data.class_indices.keys())

    # Get model predictions
    pred_probs = model.predict(test_data)
    pred_labels = np.argmax(pred_probs, axis=1)

    # Confusion matrix
    cm = confusion_matrix(true_labels, pred_labels)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_labels, yticklabels=class_labels)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "confusion_matrix.png"))
    plt.close()
    logger.info("🧩 Saved confusion matrix.")


    #Prediction report CSV
    report_data = {
        "filename": test_data.filenames,
        "true_label": [class_labels[i] for i in true_labels],
        "predicted_label": [class_labels[i] for i in pred_labels]
    }

    df = pd.DataFrame(report_data)
    df.to_csv(os.path.join(OUTPUT_DIR, "predictions_report.csv"), index=False)
    logger.info("📁 Saved predictions report CSV.")

##################################################################################################
#                                       EXECUTION ENTRY POINT                                     #
##################################################################################################

if __name__ == "__main__":
    run_evaluation()

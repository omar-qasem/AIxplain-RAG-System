import csv
import os

kaggle_dataset_path = os.path.join(os.path.expanduser("~"), ".cache", "kagglehub", "datasets", "mpwolke", "cusersmarildownloadscompliancecsv", "versions", "1", "compliance.csv")

try:
    with open(kaggle_dataset_path, "r", encoding="latin1") as f:
        reader = csv.reader(f, delimiter=";")
        for i, row in enumerate(reader):
            if i < 10 or i > 150 and i < 165:
                print(f"Line {i+1}: {row}")
            elif i == 10:
                print("...")
except FileNotFoundError:
    print(f"Error: Kaggle dataset not found at {kaggle_dataset_path}")
except Exception as e:
    print(f"Error inspecting Kaggle dataset: {e}")


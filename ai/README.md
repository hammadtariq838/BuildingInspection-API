Information about setting up datasets and pretrained models for the crack detection models.

# Concrete Crack Classification Model
  Built upon the model from the repository: [Concrete-Crack-Detection-Segmentation](https://github.com/konskyrt/Concrete-Crack-Detection-Segmentation)

# Crack Segmentation Model
  Built upon the model from the repository: [Concrete-Crack-Detection-Segmentation](https://github.com/khanhha/crack_segmentation)


# Crack Detection YOLOv8 Model
  Built upon the model from the repository: [Roboflow](https://universe.roboflow.com/individual-work/crack_detect-u54px)
  [Github Repo](https://github.com/JayachandranSM/Crack_detection_DL)

  ```
  from ultralytics import YOLO
  model = YOLO()
  model.train(data='./ valid data.yaml file path ', epochs=100)
  ```
  Recommendation -> Train the model on a GPU machine for faster training.
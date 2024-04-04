import os
from typing import Any
from torch import load, device, cuda, no_grad, exp
from torchvision import transforms
from cv2 import addWeighted
from cv2.typing import MatLike
import numpy as np
from PIL import Image

# dataset_path = './datasets/concrete_crack_classification'
# dataset_path_positive = './datasets/concrete_crack_classification/Positive'
# dataset_path_negative = './datasets/concrete_crack_classification/Negative'
# pretrained_model_path = './pretrained/concrete_crack_classification.pt'
current_directory = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(current_directory, 'datasets/concrete_crack_classification')
dataset_path_positive = os.path.join(current_directory, 'datasets/concrete_crack_classification/Positive')
dataset_path_negative = os.path.join(current_directory, 'datasets/concrete_crack_classification/Negative')
pretrained_model_path = os.path.join(current_directory, 'pretrained/concrete_crack_classification.pt')


# create a singleton architecture class for the concrete crack classification model
class ConcreteCrackClassification:
  __instance = None
  __model: Any = None
  # means and standard deviations for the model input - RGB images of size 227x227
  __mean_nums = [0.485, 0.456, 0.406]
  __std_nums = [0.229, 0.224, 0.225]
  __transform = {
    'train': transforms.Compose([
      transforms.RandomResizedCrop(size=227),
      transforms.RandomRotation(degrees=10),
      transforms.RandomHorizontalFlip(),
      transforms.RandomVerticalFlip(),
      transforms.ColorJitter(brightness=0.15, contrast=0.15),
      transforms.ToTensor(),
      transforms.Normalize(__mean_nums, __std_nums)
    ]),
    'val': transforms.Compose([
      transforms.Resize(227),
      transforms.CenterCrop(227),
      transforms.ToTensor(),
      transforms.Normalize(__mean_nums, __std_nums)
    ])
  }
  __classes = ['Negative', 'Positive']


  @property 
  def model(self):
    return self.__model
  @model.setter
  def model(self, value):
    if value is not self.__model:
      raise ValueError("Cannot change the model once it is set!")
    return self.__model
  @model.getter
  def model(self):
    return self.__model



  def __new__(cls, *args, **kwargs):
    if cls.__instance is None:
      cls.__instance = super().__new__(cls, *args, **kwargs)
      pretrained_model_exists = os.path.exists(pretrained_model_path)
      dataset_exists = os.path.exists(dataset_path) and os.path.exists(dataset_path_positive) and os.path.exists(dataset_path_negative)
      if pretrained_model_exists:
        cls.__load_model(cls.__instance)
      else:
        print("Pretrained model not found!")
    return cls.__instance

  def __init__(self):
    pass

  def __load_model(self):
    if not os.path.exists(pretrained_model_path):
      return False
    self.__model = load(pretrained_model_path)
    self.__model = self.__model.to(device('cuda' if cuda.is_available() else 'cpu'))
    return True
  
  def predict(self, image: Image.Image):
    transform = self.__transform['val']
    image_tensor = transform(image)
    # image_tensor = self.__transform['val'](image)
    if cuda.is_available():
      image_tensor = image_tensor.view(1, 3, 227, 227).cuda()
    else:
      image_tensor = image_tensor.view(1, 3, 227, 227)
    with no_grad():
      self.__model.eval()
      out = self.__model(image_tensor)
      ps = exp(out)
      topk, topclass = ps.topk(1, dim=1)
      if topclass.cpu().numpy()[0][0] == 0:
        class_name = self.__classes[0]
      elif topclass.cpu().numpy()[0][0] == 1:
        class_name = self.__classes[1]
      else:
        class_name = "Unknown"
    return class_name
  
  def predict_on_crops(self, image: MatLike):
    img_height, img_width = image.shape[:2]
    k = 0
    output_image = np.zeros_like(image)
    for i in range(0, img_height, img_height//10):
      for j in range(0, img_width, img_width//10):
        crop = image[i:i+img_height//10, j:j+img_width//10]
        class_name = self.predict(Image.fromarray(crop))
        if class_name == 'Positive':
          color = (0, 0, 255)
        else:
          color = (0, 0, 0)
        k += 1
        colorBox = np.zeros_like(crop, dtype=np.uint8)
        colorBox[:] = color
        added_image = addWeighted(crop, 0.7, colorBox, 0.3, 0)
        output_image[i:i+img_height//10, j:j+img_width//10] = added_image
    return output_image

  def get_model(self):
    return self.model


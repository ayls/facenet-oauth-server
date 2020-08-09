from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import os
import io
from PIL import Image

DETECTION_THRESHOLD = 1

class Detection:

  def __init__(self):  
    self.workers = 0 if os.name == 'nt' else 4

    self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print('Running on device: {}'.format(self.device))

    self.stored_embeddings = torch.load('embeddings.pt')
    self.stored_names = np.load('names.npy')

    # face detection pipeline
    self.mtcnn = MTCNN(
      image_size=160, margin=0, min_face_size=20,
      thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
      device=self.device
    )

    # facenet pipeline
    self.resnet = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)

  def collate_fn(self, x):
    return x[0]

  def detect(self, image_bytes):
    # read image
    x = Image.open(io.BytesIO(image_bytes))

    # run mtcnn pipeline
    aligned = []
    x_aligned, prob = self.mtcnn(x, return_prob=True)
    if x_aligned is not None:
      # print('Face detected with probability: {:8f}'.format(prob))
      aligned.append(x_aligned)

    # run facenet
    aligned = torch.stack(aligned).to(self.device)
    embeddings = self.resnet(aligned).detach().cpu()

    # calculate distances and return detection results
    result = None
    e1 = embeddings[0]
    minDiff = 100
    minDiffIdx = -1
    for idx, e2 in enumerate(self.stored_embeddings):
      diff = (e1 - e2).norm().item()
      print(diff)
      if diff < minDiff and diff < DETECTION_THRESHOLD:
        minDiff = diff
        minDiffIdx = idx
    if minDiffIdx >= 0:
      result = self.stored_names[minDiffIdx]

    return result


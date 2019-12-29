from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import os

DETECTION_THRESHOLD = 1

workers = 0 if os.name == 'nt' else 4

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

stored_embeddings = torch.load('embeddings.pt')
stored_names = np.load('names.npy')

# face detection pipeline
mtcnn = MTCNN(
  image_size=160, margin=0, min_face_size=20,
  thresholds=[0.6, 0.7, 0.7], factor=0.709, post_process=True,
  device=device
)

# facenet pipeline
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# read images
def collate_fn(x):
  return x[0]

dataset = datasets.ImageFolder('./test_images')
dataset.idx_to_class = {i:c for c, i in dataset.class_to_idx.items()}
loader = DataLoader(dataset, collate_fn=collate_fn, num_workers=workers)

# run mtcnn pipeline
aligned = []
for x, y in loader:
  x_aligned, prob = mtcnn(x, return_prob=True)
  if x_aligned is not None:
    print('Face detected with probability: {:8f}'.format(prob))
    aligned.append(x_aligned)

# run facenet
aligned = torch.stack(aligned).to(device)
embeddings = resnet(aligned).detach().cpu()

# calculate distances and display detection results
results = []
for e1 in embeddings:
  minDiff = 100
  minDiffIdx = -1
  for idx, e2 in enumerate(stored_embeddings):
    diff = (e1 - e2).norm().item()
    if diff < minDiff and diff < DETECTION_THRESHOLD:
      minDiff = diff
      minDiffIdx = idx
  if minDiffIdx >= 0:
    results.append(stored_names[minDiffIdx])
  else:
    results.append(None)    

print(results)


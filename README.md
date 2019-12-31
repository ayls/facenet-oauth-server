# Oauth Server with FaceNet identification

A PoC OAuth server that uses face detection (based on FaceNet) instead of username/password to identify users.

## Setup

### Python (3.7) environment Setup

``` bash
# install PyTorch
pip install torch===1.3.1 torchvision===0.4.2 -f https://download.pytorch.org/whl/torch_stable.html

# install other requirements
pip install -r requirements.txt
```

### Generate embedding vectors
``` bash
# cd into training directory
cd training

# copy one training image per person into training_images directory
# the structure should look something like
training_images
└───John
│   │   image.jpg
|
└───Jane
    │   image.jpg

# copy one test image per person (should be different that the one used for training) into test_images directory
# the structure should look something like
test_images
└───John
│   │   alternative_image.jpg
|
└───Jane
    │   alternative_image.jpg    

# generate embeddings and names
python set_embeddings.py

# test embeddings and names
python test_detection.py

# copy embeddings and names to server directory
cp embeddings.pt ../server/embeddings.pt
cp names.npy ../server/names.npy
```

### Generate RSA keys
``` bash
cd server

# prepare private key (do not specify passphrase)
openssl genrsa -out private.pem 2048

# prepare public key
openssl rsa -in private.pem -pubout -outform PEM -out public.pem

# prepare jwk file
npm install -g pem-jwk
pem-jwk public.pem > public.jwk

# serve with hot reload at 127.0.0.1:5001
python server.py
```

### Sample Client Setup

``` bash
# cd into client directory
cd client

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev
```

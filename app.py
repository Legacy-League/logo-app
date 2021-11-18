import streamlit as st
import fastai
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import open_image, load_learner, image, torch
import numpy as np4
import urllib.request
import PIL.Image
from io import BytesIO
import torchvision.transforms as T
from PIL import Image
import requests
from io import BytesIO
import fastai
from fastai.vision import *
from fastai.utils.mem import *
from fastai.vision import open_image, load_learner, image, torch
import numpy as np
import urllib.request
from urllib.request import urlretrieve
import PIL.Image
from io import BytesIO
import torchvision.transforms as T
import torchvision.transforms as tfms


class FeatureLoss(nn.Module):
    def __init__(self, m_feat, layer_ids, layer_wgts):
        super().__init__()
        self.m_feat = m_feat
        self.loss_features = [self.m_feat[i] for i in layer_ids]
        self.hooks = hook_outputs(self.loss_features, detach=False)
        self.wgts = layer_wgts
        self.metric_names = ['pixel',] + [f'feat_{i}' for i in range(len(layer_ids))
              ] + [f'gram_{i}' for i in range(len(layer_ids))]

    def make_features(self, x, clone=False):
        self.m_feat(x)
        return [(o.clone() if clone else o) for o in self.hooks.stored]
    
    def forward(self, input, target):
        out_feat = self.make_features(target, clone=True)
        in_feat = self.make_features(input)
        self.feat_losses = [base_loss(input,target)]
        self.feat_losses += [base_loss(f_in, f_out)*w
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.feat_losses += [base_loss(gram_matrix(f_in), gram_matrix(f_out))*w**2 * 5e3
                             for f_in, f_out, w in zip(in_feat, out_feat, self.wgts)]
        self.metrics = dict(zip(self.metric_names, self.feat_losses))
        return sum(self.feat_losses)
    
    def __del__(self): self.hooks.remove()
    
st.set_page_config(layout="wide")
#st.image(os.path.join('Images','2.jpg'), use_column_width  = True)
st.markdown("<h1 style='text-align: center; color: white;'>Legacy League</h1>", unsafe_allow_html=True)
Image = st.file_uploader('Upload your picture here',type=['jpg','jpeg','png'])
if Image is not None:
  col1, col2 = st.beta_columns(2)
  img = PIL.Image.open(Image).convert("RGB")
  #Image = Image.read()
  #Image = tf.image.decode_image(Image, channels=3).numpy()                  
  #Image = adjust_gamma(Image, gamma=gamma)
  Image1 = np.array(img)
  with col1:
        st.image(Image1,width = 400, height =400)
  #imageLocation = st.empty()
  #imageLocation.image(img, width = 400)
  MODEL_URL = "https://www.dropbox.com/s/daf70v42oo93kym/Legacy_best.pkl?dl=1"
  urlretrieve(MODEL_URL, "Legacy_best.pkl")
  path = Path(".")
  learn=load_learner(path, 'Legacy_best.pkl')
  im1 = img.save("test.jpg")
  img_fast = open_image("test.jpg")
  #img_t = T.ToTensor()(img)
  #img_fast = Image(img_t)
  _, img_hr, _ = learn.predict(img_fast)
  img_np=image2np(img_hr)
  with col2:
    st.image(img_np, width=400,clamp=True)

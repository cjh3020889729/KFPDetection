# Copyright (c) 2022 Jinghui Cai. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np

from visualizes import visualize_img
from visualizes import visualize_bbox
from visualizes import visualize_det

image = np.random.randint(low=0, high=2, size=(512, 512, 3)).astype(np.float32)
print('image shape:', image.shape)

bboxs = np.asarray([[0, 0.9,24, 94, 212, 164], [1, 0.3, 11, 63, 89, 112]])

visualize_img(img=image, save_path='test.png')
visualize_bbox(bboxs=bboxs, draw_board=image, labels={0:'cls1', 1:'cls2'},
               use_rgb=False, save_path='test.png')

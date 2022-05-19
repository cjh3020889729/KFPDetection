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
# Test logger functions
import os
import sys
import numpy as np

# 设置当前KFPDetection包路径:
# 保证visualizes正常调用
sys.path.append( os.getcwd() )

from loggers import create_logger
from loggers import get_created_logger_names

logger = create_logger(logger_name='test', save_path=None)
logger2 = create_logger(logger_name='test.2', save_path=None)

logger.warning('hello logging!')
logger.info('hello logging!')
logger.error('hello logging!')
# logger level==info > debug, 无法记录该级别的信息
# 因此，处理器无法接收到该信息
logger.debug('hello logging!')

logger.info(get_created_logger_names())
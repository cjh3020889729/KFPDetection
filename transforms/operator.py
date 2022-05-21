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
import sys

from typing import Dict, List, Union, Sequence, Any

from loggers import create_logger, error_traceback
logger = create_logger(logger_name=__name__)

__all__ = ['Transform']


class Transform(object):
    def __init__(self) -> None:
        """预处理继承基类
            desc:
                Parameters:
                    None
                Returns:
                    None
                other:
                    通过继承后实现apply方法，完成样本数据的预处理
        """
        super(Transform, self).__init__()
        # 记录当前类的名字
        self.name=self.__class__.__name__
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return self.name

    def apply(self,
              sample: Dict[str, Any]) -> Dict[str, Any]:
        """预处理实现接口(需要继承后实现)
            desc:
                Parameters:
                    samples: 处理的样本数据(dict)
                Returns:
                    None
        """
        try:
            raise NotImplementedError()
        except:
            error_traceback(logger=logger,
                            lasterrorline_offset=14,
                            num_lines=11)
            logger.error("Summary: The apply function of"
            "'{0}' class should be reload or implement.".format(self.name))
            sys.exit(1)
    
    def __call__(self,
                 samples: Union[Dict[str, Any],
                 List[Dict[str, Any]]]) -> Union[Dict[str, Any],
                                           List[Dict[str, Any]]]:
        """预处理调用接口
            desc:
                Parameters:
                    samples: 采样的样本数据/批量样本数据[dict, list(dict)]
                Returns:
                    None
        """
        # 当输入为批量样本时，进行遍历
        if isinstance(samples, Sequence):
            for idx, sample in enumerate(samples):
                samples[idx] = self.apply(sample)
            return samples
        
        # 单样本处理
        samples = self.apply(samples)
        return samples


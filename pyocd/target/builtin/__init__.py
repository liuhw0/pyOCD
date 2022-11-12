# pyOCD debugger
# Copyright (c) 2013-2021 Arm Limited
# SPDX-License-Identifier: Apache-2.0
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

from ...coresight.coresight_target import CoreSightTarget
from . import target_FM33LC02X
from . import target_FM33LG04X
from . import target_STM32F103XB
from . import target_STM32L073XB

## @brief Dictionary of all builtin targets.
#
# @note Target type names must be a valid C identifier, normalised to all lowercase, using _underscores_
#   instead of dashes punctuation. See pyocd.target.normalise_target_type_name() for the code that
#   normalises user-provided target type names for comparison with these.
BUILTIN_TARGETS = {
          'cortex_m': CoreSightTarget,
          'fm33lc02x': target_FM33LC02X.FM33LC02X,
          'fm33lg04x': target_FM33LG04X.FM33LG04X,
          'stm32f103xb': target_STM32F103XB.STM32F103XB,
          'stm32l073xb': target_STM32L073XB.STM32L073XB,
         }

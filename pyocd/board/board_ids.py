# pyOCD debugger
# Copyright (c) 2017-2020 Arm Limited
# Copyright (c) 2021 Chris Reed
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

from typing import (NamedTuple, Optional)

class BoardInfo(NamedTuple):
    name: str
    target: Optional[str] = None
    binary: Optional[str] = None
    vendor: Optional[str] = None

BOARD_ID_TO_INFO = {
  # Note: please keep board list sorted by ID!
  #
  # Board ID            Board Name              Target              Test Binary
  # "0700": BoardInfo(  "NUCLEO-F103RB",        "stm32f103rb",      "ST-Nucleo-F103RB.bin", ),
}

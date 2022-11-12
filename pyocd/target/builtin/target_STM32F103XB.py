# pyOCD debugger
# Copyright (c) 2022 PyOCD Authors
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
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

DBGMCU_CR = 0xE0042004
#0111 1110 0011 1111 1111 1111 0000 0000
DBGMCU_VAL = 0x7E3FFF00

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0x4603b510, 0x4c442000, 0x48446020, 0x48446060, 0x46206060, 0xf01069c0, 0xd1080f04, 0x5055f245,
    0x60204c40, 0x60602006, 0x70fff640, 0x200060a0, 0x4601bd10, 0x69004838, 0x0080f040, 0x61104a36,
    0x47702000, 0x69004834, 0x0004f040, 0x61084932, 0x69004608, 0x0040f040, 0xe0036108, 0x20aaf64a,
    0x60084930, 0x68c0482c, 0x0f01f010, 0x482ad1f6, 0xf0206900, 0x49280004, 0x20006108, 0x46014770,
    0x69004825, 0x0002f040, 0x61104a23, 0x61414610, 0xf0406900, 0x61100040, 0xf64ae003, 0x4a2120aa,
    0x481d6010, 0xf01068c0, 0xd1f60f01, 0x6900481a, 0x0002f020, 0x61104a18, 0x47702000, 0x4603b510,
    0xf0201c48, 0xe0220101, 0x69004813, 0x0001f040, 0x61204c11, 0x80188810, 0x480fbf00, 0xf01068c0,
    0xd1fa0f01, 0x6900480c, 0x0001f020, 0x61204c0a, 0x68c04620, 0x0f14f010, 0x4620d006, 0xf04068c0,
    0x60e00014, 0xbd102001, 0x1c921c9b, 0x29001e89, 0x2000d1da, 0x0000e7f7, 0x40022000, 0x45670123,
    0xcdef89ab, 0x40003000, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000037,
    'pc_program_page': 0x200000c1,
    'pc_erase_sector': 0x20000083,
    'pc_eraseAll': 0x20000049,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000128,
    'begin_stack' : 0x20001930,
    'end_stack' : 0x20000930,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x400,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x20000130,
        0x20000530
    ],
    'min_program_length' : 0x400,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x128,
    'rw_start': 0x12c,
    'rw_size': 0x4,
    'zi_start': 0x130,
    'zi_size': 0x0,

    # Flash information
    'flash_start': 0x8000000,
    'flash_size': 0x20000,
    'sector_sizes': (
        (0x0, 0x400),
    )
}

class STM32F103XB(CoreSightTarget):

    VENDOR = "STMicroelectronics"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x08000000,  length=0x20000,      blocksize=0x200, is_boot_memory=True,
            algo=FLASH_ALGO),
        RamRegion(      start=0x20000000,  length=0x5000)
        )

    def __init__(self, session):
        super(STM32F103XB, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("STM32F103.svd")

    def post_connect_hook(self):
        self.write_memory(DBGMCU_CR, DBGMCU_VAL)




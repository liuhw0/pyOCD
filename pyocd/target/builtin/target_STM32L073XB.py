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

DBGMCU_CR = 0x40015804
DBGMCU_VAL = 0x00000000

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xd0012a01, 0xd1172a02, 0x6981483b, 0x0212220f, 0x61814311, 0x60c14939, 0x60c14939, 0x61014939,
    0x61014939, 0x02c069c0, 0x4839d406, 0x60014937, 0x60412106, 0x60814937, 0x47702000, 0xd0012801,
    0xd1082802, 0x6841482c, 0x43112202, 0x68416041, 0x43112201, 0x20006041, 0xb5304770, 0x684a4926,
    0x4322154c, 0x684a604a, 0x432a2508, 0x2200604a, 0x48296002, 0xe0004a26, 0x698b6010, 0xd1fb07db,
    0x43a06848, 0x68486048, 0x604843a8, 0xbd302000, 0x47702001, 0x4c18b5f0, 0x15252300, 0x313f2608,
    0x468c0989, 0x6861e024, 0x60614329, 0x43316861, 0x21406061, 0xc080ca80, 0x29001f09, 0x4916d1fa,
    0x07ff69a7, 0x4f12d002, 0xe7f96039, 0x050969a1, 0xd0060f09, 0x210f69a0, 0x43080209, 0x200161a0,
    0x6861bdf0, 0x606143a9, 0x43b16861, 0x1c5b6061, 0xd8d8459c, 0xbdf02000, 0x40022000, 0x89abcdef,
    0x02030405, 0x8c9daebf, 0x13141516, 0x00005555, 0x40003000, 0x00000fff, 0x0000aaaa, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000041,
    'pc_program_page': 0x20000099,
    'pc_erase_sector': 0x2000005f,
    'pc_eraseAll': 0x120000003,

    'static_base' : 0x20000000 + 0x00000004 + 0x0000011c,
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
    'ro_size': 0x11c,
    'rw_start': 0x120,
    'rw_size': 0x4,
    'zi_start': 0x124,
    'zi_size': 0x0,

    # Flash information
    'flash_start': 0x8000000,
    'flash_size': 0x20000,
    'sector_sizes': (
        (0x0, 0x80),
    )
}

class STM32L073XB(CoreSightTarget):

    VENDOR = "STMicroelectronics"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x08000000,  length=0x20000,      blocksize=0x200, is_boot_memory=True,
            algo=FLASH_ALGO),
        RamRegion(      start=0x20000000,  length=0x5000)
        )

    def __init__(self, session):
        super(STM32L073XB, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("STM32L073.svd")

    def post_connect_hook(self):
        self.write_memory(DBGMCU_CR, DBGMCU_VAL)




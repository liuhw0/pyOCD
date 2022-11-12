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

DBGMCU_CR = 0x40000004
DBGMCU_VAL = 0x00003D03

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xe0052200, 0xbf002100, 0x29391c49, 0x1c52d3fb, 0xd3f74282, 0x48664770, 0x22206ac1, 0x62c14311,
    0x31404963, 0x03436b0a, 0x630a431a, 0x61012101, 0x08c968c1, 0x60c100c9, 0x47702000, 0x6ac1485c,
    0x43912220, 0x485a62c1, 0x6b013040, 0x43910452, 0x20006301, 0xb5f04770, 0x4d562400, 0x69692601,
    0x02002003, 0x61694381, 0x61686968, 0x20026969, 0x61694381, 0x43306968, 0x484f6168, 0x484f61a8,
    0x026061a8, 0x2300494e, 0x01bf2719, 0xe0056001, 0xd20642bb, 0x1c5b2001, 0xffb2f7ff, 0x07c06a28,
    0x622ed0f6, 0x27ff2300, 0xe0053791, 0xd20642bb, 0x1c5b2001, 0xffa4f7ff, 0x07c06a28, 0x2000d1f6,
    0x1c6461a8, 0xd9ca2cff, 0xb570bdf0, 0x69614c39, 0x02122203, 0x61614391, 0x61616961, 0x22026961,
    0x61614391, 0x26016961, 0x61614331, 0x61a14932, 0x61a14932, 0x23004932, 0x359125ff, 0xe0056001,
    0xd20642ab, 0x1c5b2001, 0xff7af7ff, 0x07c06a20, 0x6226d0f6, 0xe0052300, 0xd20642ab, 0x1c5b2001,
    0xff6ef7ff, 0x07c06a20, 0x2000d1f6, 0xbd7061a0, 0x4616b5f0, 0x4604468c, 0x4f1e2500, 0x6978e034,
    0x00400840, 0x69786178, 0x43082102, 0x481d6178, 0x481d61b8, 0x787061b8, 0x02007831, 0x78b14308,
    0x04092300, 0x78f04301, 0x43080600, 0x1d36c401, 0x2b0ae005, 0x2001d206, 0xf7ff1c5b, 0x6a38ff41,
    0xd5f60780, 0x21026a38, 0x62384308, 0xe0052300, 0xd2062b0a, 0x1c5b2001, 0xff32f7ff, 0x07806a38,
    0x2000d4f6, 0x1d2d61b8, 0xd3c84565, 0xbdf02000, 0x40000200, 0x40001000, 0x96969696, 0xeaeaeaea,
    0x1234abcd, 0xa5a5a5a5, 0xf1f1f1f1, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x2000001b,
    'pc_unInit': 0x20000041,
    'pc_program_page': 0x20000135,
    'pc_erase_sector': 0x200000cf,
    'pc_eraseAll': 0x2000005b,

    'static_base' : 0x20000000 + 0x00000004 + 0x000001cc,
    'begin_stack' : 0x200019e0,
    'end_stack' : 0x200009e0,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x400,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x200001e0,
        0x200005e0
    ],
    'min_program_length' : 0x400,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x1cc,
    'rw_start': 0x1d0,
    'rw_size': 0x4,
    'zi_start': 0x1d4,
    'zi_size': 0x0,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x20000,
    'sector_sizes': (
        (0x0, 0x200),
    )
}

class FM33LC02X(CoreSightTarget):

    VENDOR = "FMSH"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x00000000,  length=0x20000,      blocksize=0x200, is_boot_memory=True,
            algo=FLASH_ALGO),
        RamRegion(      start=0x20000000,  length=0x6000)
        )

    def __init__(self, session):
        super(FM33LC02X, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("FM33LC0XX.svd")

    def post_connect_hook(self):
        self.write_memory(DBGMCU_CR, DBGMCU_VAL)




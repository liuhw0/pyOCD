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
DBGMCU_VAL = 0x0001FF03

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xe0052200, 0xbf002100, 0x29391c49, 0x1c52d3fb, 0xd3f74282, 0x48544770, 0x22206b81, 0x63814311,
    0x31404951, 0x050368ca, 0x60ca431a, 0x60412101, 0x08c96801, 0x600100c9, 0x47702000, 0x6b81484a,
    0x43912220, 0x48486381, 0x68c13040, 0x43910602, 0x200060c1, 0xb5f04770, 0x4d442400, 0x69692601,
    0x02002003, 0x61694381, 0x20026969, 0x61694381, 0x43306968, 0x483e6168, 0x483e61a8, 0x026061a8,
    0x2300493d, 0x379127ff, 0xe0056001, 0xd20642bb, 0x1c5b2001, 0xffb4f7ff, 0x07c06a28, 0x622ed0f6,
    0x61a82000, 0x02402001, 0x42841c64, 0x2000d3d7, 0xb570bdf0, 0x69614c2d, 0x02122203, 0x61614391,
    0x22026961, 0x61614391, 0x25016961, 0x61614329, 0x61a14927, 0x61a14927, 0x23004927, 0x369126ff,
    0xe0056001, 0xd20642b3, 0x1c5b2001, 0xff88f7ff, 0x07c06a20, 0x6225d0f6, 0x61a02000, 0xb5f0bd70,
    0x468c4616, 0x25004604, 0xe0294f18, 0x08406978, 0x61780040, 0x21026978, 0x61784308, 0x61b84817,
    0x61b84817, 0x78317870, 0x43080200, 0x230078b1, 0x43010409, 0x060078f0, 0xc4014308, 0xe0071d36,
    0x309120ff, 0xd2064283, 0x1c5b2001, 0xff58f7ff, 0x07806a38, 0x2002d5f4, 0x20006238, 0x1d2d61b8,
    0xd3d34565, 0xbdf02000, 0x40002400, 0x40001000, 0x96969696, 0xeaeaeaea, 0x1234abcd, 0xa5a5a5a5,
    0xf1f1f1f1, 0x00000000
    ],

    # Relative function addresses
    'pc_init': 0x2000001b,
    'pc_unInit': 0x20000041,
    'pc_program_page': 0x20000103,
    'pc_erase_sector': 0x200000b7,
    'pc_eraseAll': 0x2000005b,

    'static_base' : 0x20000000 + 0x00000004 + 0x00000184,
    'begin_stack' : 0x20001990,
    'end_stack' : 0x20000990,
    'begin_data' : 0x20000000 + 0x1000,
    'page_size' : 0x400,
    'analyzer_supported' : False,
    'analyzer_address' : 0x00000000,
    # Enable double buffering
    'page_buffers' : [
        0x20000190,
        0x20000590
    ],
    'min_program_length' : 0x400,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x184,
    'rw_start': 0x188,
    'rw_size': 0x4,
    'zi_start': 0x18c,
    'zi_size': 0x0,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x40000,
    'sector_sizes': (
        (0x0, 0x200),
    )
}

class FM33LG04X(CoreSightTarget):

    VENDOR = "FMSH"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x00000000,  length=0x40000,      blocksize=0x200, is_boot_memory=True,
            algo=FLASH_ALGO),
        RamRegion(      start=0x20000000,  length=0x8000)
        )

    def __init__(self, session):
        super(FM33LG04X, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("FM33LG0XX.svd")

    def post_connect_hook(self):
        self.write_memory(DBGMCU_CR, DBGMCU_VAL)




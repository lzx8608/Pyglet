#!/usr/bin/env python

'''Testing hex map debug rendering.

You should see a checkered hex map.

Press escape or close the window to finish the test.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import unittest
from render_base import RenderBase
import scene2d
from scene2d.debug import gen_hex_map

class HexFlatDebugTest(RenderBase):
    def test_main(self):
        self.init_window(256, 256)
        self.set_map(gen_hex_map([[{}]*10]*10, 32), resize=True)
        self.view.allow_oob = False
        self.run_test()

if __name__ == '__main__':
    unittest.main()

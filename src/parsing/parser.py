# -*- coding: utf-8 -*-

"""
Parser to parse protocols of the German Bundestag.
"""

# STD
import codecs

# PROJECT
from misc.helpers import get_config_from_py_file


class BundesParser(object):

    def __init__(self, config, path):
        # Init parser args from config
        self.block_divider = config.get("PROTOCOL_BLOCK_DIVIDER", ("\r\n", ))

        print u"Loading file from {}...".format(path)
        lines = [line for line in codecs.open(path, "r", "utf-8")]
        print len(lines)
        self.blockify(lines)

    def blockify(self, lines):
        """
        Turn adjacent lines into blocks.
        """
        blocks = []
        current_block = []
        size = len(lines)

        for index, line in enumerate(lines):
            if index < size - len(self.block_divider):
                # Check if block ended
                potential_divider = tuple(
                    [
                        lines[j] for j in range(
                            index+1, index+1+len(self.block_divider)
                        )
                    ]
                )

                if potential_divider == self.block_divider:
                    if current_block:
                        blocks.append(current_block)
                    current_block = []
                else:
                    if line.strip():
                        current_block.append(line.strip())

        print len(blocks)
        for block in blocks:
            print block[0]

if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    print config
    bp = BundesParser(config, "../../data/samples/sample.txt")

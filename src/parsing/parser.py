# -*- coding: utf-8 -*-

"""
Parser to parse protocols of the German Bundestag.
"""

# STD
from abc import abstractmethod
import codecs

# PROJECT
from misc.helpers import get_config_from_py_file


class Parser(object):

    def __init__(self, rules, config, parser_input):
        self.rules = rules
        self.config = config
        self.parser_input = parser_input

    @abstractmethod
    def process(self):
        """
        Where the main parsing happens. Overwrite this in subclasses.
        """
        pass


class BundesParser(Parser):
    """
    "Meta"-parser that partitions the parliament protocol into blocks and
    applies a specific parser to each of them.
    """
    def __init__(self, rules, config, input_path):
        # Init parser args from config
        self.block_divider = config.get("PROTOCOL_BLOCK_DIVIDER", ("\r\n", ))

        super(BundesParser, self).__init__(rules, config, input_path)

    def process(self):
        input_path = self.parser_input
        print u"Loading file from {}...".format(input_path)
        lines = [line for line in codecs.open(input_path, "r", "utf-8")]
        print len(lines)
        blocks = self._blockify(lines)
        parsers = self._assign_parsers(blocks)

        # Parse sections
        reports = [parser.process() for parser in parsers]
        return reports

    def _blockify(self, lines):
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
        return blocks

    def _assign_parsers(self, blocks):
        from constants import SECTIONS_TO_PARSERS  # Avoid circular imports
        parsers = []

        for block in blocks:
            # TODO: Magically figure out which parser is the right one
            pass

        return parsers


class HeaderParser(Parser):
    pass


class AgendaItemsParser(Parser):
    pass


class SessionHeaderParser(Parser):
    pass


class DiscussionsParser(Parser):
    pass


class AttachmentsParser(Parser):
    pass


class FooterParser(Parser):
    pass


if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    print config
    bp = BundesParser(config, "../../data/samples/sample.txt")

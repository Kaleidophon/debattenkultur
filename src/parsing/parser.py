# -*- coding: utf-8 -*-

"""
Parser to parse protocols of the German Bundestag.
"""

# STD
from abc import abstractmethod
import codecs

# PROJECT
from misc.helpers import get_config_from_py_file, ProtocolParsingException


class Parser(object):
    position = None

    def __init__(self, rules, parser_config, parser_input):
        self.rules = rules
        self.config = parser_config
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
    def __init__(self, rules, parser_config, input_path):
        # Init parser args from config
        self.block_divider = config.get("PROTOCOL_BLOCK_DIVIDER", ("\r\n", ))

        super(BundesParser, self).__init__(rules, parser_config, input_path)

    def process(self):
        input_path = self.parser_input
        print u"Loading file from {}...".format(input_path)
        lines = [line for line in codecs.open(input_path, "r", "utf-8")]
        print len(lines)
        blocks = self._blockify(lines)
        parsers, blocks = self._assign_parsers(blocks)

        print len(blocks)
        print len(parsers)
        print parsers

        # Parse sections
        #reports = [parser.process() for parser in parsers]
        #return reports

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
        parsers = [
            SECTIONS_TO_PARSERS[section](
                self.rules, self.config, self.parser_input
            )
            for section in self.config["PROTOCOL_SECTIONS"]
        ]

        # Perform some consistency checks
        if len(parsers) > len(blocks):
            raise ProtocolParsingException(
                u"There are more parsers {} than blocks {} found within the "
                u"document.".format(len(parsers), len(blocks))
            )
        self._check_parser_positions(parsers, len(blocks))

        block_parsers = [None] * len(blocks)
        for parser in parsers:
            block_parsers[parser.position] = parser

        # Merge remaining blocks
        _block_parsers = []
        _blocks = []
        for index, block_parser in enumerate(block_parsers):
            if block_parser is None:
                _blocks[-1].extend(blocks[index])
            else:
                _block_parsers.append(block_parser)
                _blocks.append(blocks[index])

        return _block_parsers, _blocks

    @staticmethod
    def _check_parser_positions(parsers, number_of_blocks):
        parser_positions = [parser.position for parser in parsers]

        for position in parser_positions:
            if parser_positions.count(position) > 1:
                raise ProtocolParsingException(
                    u"At least two parsers are occupying position {}".format(
                        position
                    )
                )

            # Check if negative positions are already being occupied
            if position < 0:
                if (number_of_blocks + position) in parser_positions:
                    raise ProtocolParsingException(
                        u"At least two parsers are occupying position {}".format(
                            position
                        )
                    )


class HeaderParser(Parser):
    position = 0


class AgendaItemsParser(Parser):
    position = 1


class SessionHeaderParser(Parser):
    position = 2


class DiscussionsParser(Parser):
    position = 3


class AttachmentsParser(Parser):
    position = -1


if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    print config
    bp = BundesParser([], config, "../../data/samples/sample.txt")
    bp.process()

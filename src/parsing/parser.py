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

        print u"Partitioning protocol into blocks, assigning parsers..."
        blocks = self._blockify(lines)
        parsers, blocks = self._assign_parsers(blocks)
        print u"Created {} blocks: {}.".format(
            len(blocks), ", ".join(self.config["PROTOCOL_SECTIONS"].keys())
        )

        # Parse sections
        results = [parser.process() for parser in parsers]
        return results

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
        block_parsers = [None] * len(blocks)
        protocol_sections = self.config["PROTOCOL_SECTIONS"]

        for section, position in protocol_sections.iteritems():
            block_parsers[position] = SECTIONS_TO_PARSERS[section]

        self._check_positions(protocol_sections, len(blocks))

        # Merge remaining blocks
        _block_parsers = []
        _blocks = []
        for index, block_parser in enumerate(block_parsers):
            if block_parser is None:
                _blocks[-1].extend(blocks[index])
            else:
                _block_parsers.append(block_parser)
                _blocks.append(blocks[index])

        for index, block_parser in enumerate(_block_parsers):
            _block_parsers[index] = _block_parsers[index](
                self.rules, self.config, _blocks[index]
            )

        return _block_parsers, _blocks

    @staticmethod
    def _check_positions(protocol_sections, number_of_blocks):
        positions = protocol_sections.values()

        for position in positions:
            if positions.count(position) > 1:
                raise ProtocolParsingException(
                    u"At least two sections are occupying position {}".format(
                        position
                    )
                )

            # Check if negative positions are already being occupied
            if position < 0:
                if (number_of_blocks + position) in positions:
                    raise ProtocolParsingException(
                        u"At least two sections are occupying position {}".format(
                            position
                        )
                    )


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


if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    bp = BundesParser([], config, "../../data/samples/sample.txt")
    bp.process()

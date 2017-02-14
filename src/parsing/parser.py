# -*- coding: utf-8 -*-

"""
Parser to parse protocols of the German Bundestag.
"""

# STD
import codecs

# PROJECT
from misc.helpers import (
    get_config_from_py_file,
    ProtocolParsingException,
    RuleApplicationException,
    ParsingException
)

from parsing.rules import HeaderRule
from models.model import Empty


class Parser(object):
    def __init__(self, rules, parser_config, parser_input):
        self.rules = rules
        self.config = parser_config
        self.parser_input = parser_input

    def process(self):
        """
        Main processing.
        """
        try:
            return self.apply_rules()
        except Exception, ex:
            return Empty(ex)

    def apply_rules(self):
        """
        Apply parsing rules to the parser's input.
        """
        self._check_parser_coherence()

        results = []
        rule_input = self.parser_input
        was_applied = False

        while len(results) != 1:
            results = []

            for rule in self.rules:
                try:
                    results.append(rule(rule_input).apply())
                    was_applied = True
                except RuleApplicationException:
                    pass

            # If no rules were applied, raise exception
            if not was_applied:
                raise ParsingException(
                    u"No rule could be applied to the following temporary "
                    u"results:\n{}\n\nFollowing rules were at disposal:\n{}".format(
                        u", ".join([unicode(result) for result in results]),
                        u", ".join([rule.__name__ for rule in self.rules])
                    )
                )

            # Prepare for next iteration
            rule_input = results
            was_applied = False

        return results[0]

    def _check_parser_coherence(self):
        """
        Check if the arguments given during the initialization actually make
        sense.
        """
        if len(self.rules) == 0:
            raise ParsingException(
                u"{} doesn't possess any rules to utilize.".format(
                    self.__class__.__name__
                )
            )

        if len(self.parser_input) == 0 or not self.parser_input:
            raise ParsingException(
                u"{} doesn't have any input to parse.".format(
                    self.__class__.__name__
                )
            )


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
        """
        Process the protocol.
        """
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
        print results
        for result in results:
            print result.attributes
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
        """
        Assign parsers to the "blocks" within the protocol. Some blocks might
        be merged.
        """
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
                self.config, _blocks[index]
            )

        return _block_parsers, _blocks

    @staticmethod
    def _check_positions(protocol_sections, number_of_blocks):
        """
        Check if the relative and absolute positions of the pre-defined
        sections actually line up with the blocks found in the protocol.
        """
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
    """
    Special parser to parser the protocol's header.
    """
    def __init__(self, parser_config, parser_input):
        super(HeaderParser, self).__init__(
            [HeaderRule], parser_config, parser_input
        )


class AgendaItemsParser(Parser):

    def __init__(self, parser_config, parser_input):
        super(AgendaItemsParser, self).__init__(
            [], parser_config, parser_input  # TODO: Add actual rules
        )


class SessionHeaderParser(Parser):

    def __init__(self, parser_config, parser_input):
        super(SessionHeaderParser, self).__init__(
            [], parser_config, parser_input  # TODO: Add actual rules
        )


class DiscussionsParser(Parser):

    def __init__(self, parser_config, parser_input):
        super(DiscussionsParser, self).__init__(
            [], parser_config, parser_input  # TODO: Add actual rules
        )


class AttachmentsParser(Parser):

    def __init__(self, parser_config, parser_input):
        super(AttachmentsParser, self).__init__(
            [], parser_config, parser_input  # TODO: Add actual rules
        )

if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    bp = BundesParser([], config, "../../data/samples/sample.txt")
    bp.process()

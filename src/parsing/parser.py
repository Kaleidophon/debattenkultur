# -*- coding: utf-8 -*-

"""
Parser to parse protocols of the German Bundestag.
"""
# TODO (Documentation): Write explanation about how parsers work [DU 14.04.17]
# Include:
# * How one "meta parser" divides the protocol up into blocks
# * Then assigns specific parsers to each block
# * How parsers contain rules containing rule triggers
# * How parser then actually parse
#   * Lexing
#   * Rule expansion
#   * Combination to RuleTargets
#   * Combinaton to ParserTarget
# * Combination of ParserTargets within the "meta parser" to final object

# STD
import codecs

# PROJECT
from misc.helpers import get_config_from_py_file
from misc.custom_exceptions import (
    CustomException,
    ProtocolParserAssignmentException,
    ParserCoherenceException
)

from parsing.rules import (
    Rule,
    HeaderRule,
    AgendaRule,
    AgendaItemRule,
    AgendaAttachmentRule,
    AgendaCommentRule
)
from models.model import Empty, Filler
from models.agenda_item import Agenda, Protocol
from models.header import Header


class Parser:
    lexed_parser_input = None

    def __init__(self, rule_classes, parser_config, parser_input, parser_target):
        self.rule_classes = rule_classes
        self.config = parser_config
        self.parser_input = parser_input
        self.parser_target = parser_target

    def process(self):
        """
        Main processing.
        """
        try:
            self.lex()
            return self.apply_rules()
        except Exception as ex:
            if isinstance(ex, CustomException):
                return Empty(ex)
            else:
                raise

    def lex(self):
        """
        Divide up lines into either

        a) Parsing rules that trigger for a certain line (a specific regex
           matches and indicates the beginning of a certain new block)
        b) A filler line that will be attributed to the most recent triggered
           rule in the next step
        """
        self.lexed_parser_input = []

        for line in self.parser_input:
            for rule_class in self.rule_classes:
                rule = rule_class(line)
                if rule.triggers(line):
                    self.lexed_parser_input.append(rule)
                    break
            else:
                self.lexed_parser_input.append(Filler(line))

    def apply_rules(self):
        """
        Apply parsing rules to the parser's input.
        """
        self._check_parser_coherence()

        # 1. Add filler lines to most recent rules
        reduced_parser_input = []
        current_rule = None
        for lexed_input in self.lexed_parser_input:
            # Lexed input is rule
            if isinstance(lexed_input, Rule):
                if current_rule:
                    reduced_parser_input.append(lexed_input)
                current_rule = lexed_input
            # Lexed input is filler
            else:
                current_rule.expand(lexed_input)

        # 2. Let rules apply their logic to their new, expanded input and
        # turn them into their target models, depending on the kind of block
        modeled_parser_output = []
        for rule in reduced_parser_input:
            modeled_parser_output.append(rule.apply())

        # 3. Combine all of these targets into the parsers target model
        return self.parser_target(*modeled_parser_output)

    def _check_parser_coherence(self):
        """
        Check if the arguments given during the initialization actually make
        sense.
        """
        if len(self.rule_classes) == 0:
            raise ParserCoherenceException(
                "{} doesn't possess any rules to utilize.".format(
                    self.__class__.__name__
                )
            )

        if len(self.parser_input) == 0 or not self.parser_input:
            raise ParserCoherenceException(
                "{} doesn't have any input to parse.".format(
                    self.__class__.__name__
                )
            )


class BundesParser(Parser):
    """
    "Meta"-parser that partitions the parliament protocol into blocks and
    applies a specific parser to each of them.
    """

    def __init__(self, rule_classes, parser_config, input_path):
        # Init parser args from config
        self.block_divider = config.get("PROTOCOL_BLOCK_DIVIDER", ("\r\n", ))

        super().__init__(
            rule_classes, parser_config, input_path, parser_target=Protocol
        )

    def process(self):
        """
        Process the protocol.
        """
        input_path = self.parser_input
        print("Loading file from {}...".format(input_path))
        lines = [line for line in codecs.open(input_path, "r", "utf-8")]

        print("Partitioning protocol into blocks, assigning parsers...")
        blocks = self._blockify(lines)
        parsers, blocks = self._assign_parsers(blocks)
        print("Created {} blocks: {}.".format(
            len(blocks), ", ".join(self.config["PROTOCOL_SECTIONS"].keys())
        ))

        # Parse sections
        results = [parser.process() for parser in parsers]
        print(results)
        for result in results:
            print(result.attributes)
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
                raise ProtocolParserAssignmentException(
                    "At least two sections are occupying position {}".format(
                        position
                    )
                )

            # Check if negative positions are already being occupied
            if position < 0:
                if (number_of_blocks + position) in positions:
                    raise ProtocolParserAssignmentException(
                        "At least two sections are occupying position {}".format(
                            position
                        )
                    )


class HeaderParser(Parser):
    """
    Special parser to parser the protocol's header.
    """
    # TODO (Refactor): Add parser target
    def __init__(self, parser_config, parser_input):
        super().__init__(
            [HeaderRule], parser_config, parser_input
        )


class AgendaParser(Parser):
    # TODO (Refactor): Add missing documentation
    def __init__(self, parser_config, parser_input):
        super().__init__(
            [
                AgendaItemRule
                #AgendaRule,
                #AgendaAttachmentRule
                #AgendaCommentRule  # TODO: Re-add this rule
            ],
            parser_config,
            parser_input,
            parser_target=Agenda
        )


class SessionHeaderParser(Parser):
    # TODO (Refactor): Add missing documentation
    def __init__(self, parser_config, parser_input):
        super().__init__(
            [],  # TODO: Add actual rules
            parser_config,
            parser_input,
            parser_target=Header
        )


class SessionParser(Parser):
    # TODO (Refactor): Add missing documentation
    # TODO (Refactor): Add parser target
    def __init__(self, parser_config, parser_input):
        super().__init__(
            [],  # TODO: Add actual rules
            parser_config,
            parser_input
        )


class AttachmentsParser(Parser):
    # TODO (Refactor): Add missing documentation
    # TODO (Refactor): Add parser target
    def __init__(self, parser_config, parser_input):
        super().__init__(
            [],  # TODO: Add actual rules
            parser_config,
            parser_input
        )

if __name__ == "__main__":
    config = get_config_from_py_file("../../config.py")
    bp = BundesParser([], config, "../../data/samples/sample.txt")
    bp.process()

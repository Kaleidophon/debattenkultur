# General config
SUPPRESS_EXCEPTIONS = False

PROTOCOL_BLOCK_DIVIDER = ("\r\n", "\r\n")

# Sections of the parliaments protocol and their index
PROTOCOL_SECTIONS = {
	"HEADER": 0,
	"AGENDA_ITEMS": 1,
	"SESSION_HEADER": 2,
	"DISCUSSIONS": 3,
	"ATTACHMENTS": -1  # Everything before belongs to DISCUSSIONS
}
PROTOCOL_DATE_FORMAT = '%A, den %d. %B %Y'
PROTOCOL_AGENDA_SUBITEM_PATTERN = r"\w\)\t.+"
PROTOCOL_AGENDA_SUBITEM_ITEMTYPE = "Untertagesordnungspunkt"

# Rule triggers
HEADER_RULE_TRIGGER = "Deutscher Bundestag"

AGENDA_ATTACHMENT_TRIGGER = r"Anlage ^\d+"
AGENDA_ITEM_TRIGGER = r"(Zusatzt|T)agesordnungspunkt \d+:"
# TODO (Refactor): Add more triggers [DU 11.06.17]
AGENDA_COMMENT_TRIGGER = r"^Glückw"

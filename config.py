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
PROTOCOL_AGENDA_ITEM_PATTERN = r"(Zusatzt|T)agesordnungspunkt \d+:"
PROTOCOL_AGENDA_SUBITEM_PATTERN = r"\w\)\t.+"
PROTOCOL_AGENDA_SUBITEM_ITEMTYPE = "Untertagesordnungspunkt"
PROTOCOL_AGENDA_ATTACHMENT_PATTERN = r"Anlage \d+"

# Rule triggers
# TODO (Feature): Add rule triggers here

# String common constants AND nexusReader constants
NUM_OF_TREES = 2        # Number of trees allowed
NUM_HOST_TREES = 1      # Number of Host trees allowed
NUM_PARASITE_TREES = 1  # Number of Parasyte tress allowed

EQUAL = "="
COLONS = ":"
SEMICOLONS = ";"
NEW_LINE = "\n"
TAB = "\t"
SPACE = " "
COMMA = ","
NEX = ".nex"
NUM_OF_NEW_LINES_ALLOWED = 1 # How many single '\n' lines are permitted before throwing an assertion!

ASSERT_WRONG_STRUCTURE = "The Nexus file structure is wrong, check AmoCoala documentation on 'input files' section."

BEGIN = "BEGIN"
HOST = "HOST"
PARASITE = "PARASITE"
PARASYTE = "PARASYTE"
TREE_HOST = "Host"
TREE_HOSTS = "Hosts"
HOST_WORDS_ALLOWED = [TREE_HOST, TREE_HOSTS]
TREE_PARASYTE = "Parasyte"
TREE_PARASYTES = "Patasytes"
TREE_PARASITE = "Parasite"
TREE_PARASITES = "Parasites"
PARASYTE_WORDS_ALLOWED = [TREE_PARASITE, TREE_PARASITES, TREE_PARASYTE, TREE_PARASYTES]
BEGIN_DISTRIBUTION = BEGIN + " DISTRIBUTION"
RANGE = "RANGE"
ENDBLOCK = "ENDBLOCK;"
END = "END;"
NEXUS = "#NEXUS"
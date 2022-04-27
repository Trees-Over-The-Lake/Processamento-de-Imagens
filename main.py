from frontend import front
from backend import os as backos
from backend import back


# Current working dir
cwd = backos.getCurrentWorkingDirectory()
# JPEG and PNG types
types = back.SUPPORTED_TYPES

front.drawGUI(cwd, types)

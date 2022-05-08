from frontend import front
from backend import os as backos


# Current working dir
cwd = backos.getCurrentWorkingDirectory()
# JPEG and PNG types
types = [('Images', '*.jpeg *.png *.jpg')]

front.drawGUI(cwd, types)

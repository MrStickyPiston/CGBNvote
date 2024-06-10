import bottle
import os
import sys

project_home = '/home/CGBNvote/CGBNvote/'
os.chdir(project_home)

if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# make sure the default templates directory is known to Bottle
templates_dir = os.path.join(project_home, 'views/')
if templates_dir not in bottle.TEMPLATE_PATH:
    bottle.TEMPLATE_PATH.insert(0, templates_dir)

application = bottle.default_app()

import lib
application = lib.web.app
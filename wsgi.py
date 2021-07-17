import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/")

from main import app
application = app

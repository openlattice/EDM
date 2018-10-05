import openapi_client
import json
import yaml
import os

from utils import utils


edm = utils.grab_edm()

utils.write_edm(edm)

"""
Should output a json file in the format described here:
http://developer.runkeeper.com/healthgraph/fitness-activities#newly-completed-activities
"""
import argh
import json
import logging

from .tcx import get_tcx_activity_from_file
from .conversion import convert_tcx_to_healthgraph

logging.basicConfig()
logger = logging.getLogger(__name__)


@argh.arg('input-file', help='The TCX file to convert')
@argh.arg('output-file', help='The file to output the json file to')
@argh.arg('--notes', help='Notes to attach to this activity')
@argh.arg('--detect-pauses',
          help='If specified then runkeeper should interpret periods of no '
               'entries as pauses')
def main(input_file, output_file, notes=None, detect_pauses=False):
    """
    Converts TCX files to the format expected by the RunKeeper HealthGraph API
    """
    tcx = get_tcx_activity_from_file(input_file)
    healthgraph = convert_tcx_to_healthgraph(
        tcx, notes=notes, detect_pauses=detect_pauses)
    with open(output_file, 'w') as out_buffer:
        json.dump(healthgraph, out_buffer)

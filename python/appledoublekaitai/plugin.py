from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginId, PluginInfo
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger

import kaitai_utils

log = Logger(__name__)

BYTE_ARRAY_LENGTH = 256


class Plugin(ExtractionPlugin):

    def plugin_info(self):
        file_format = kaitai_utils.get_plugin_title_from_metadata()
        plugin_description = f'Extracts "{file_format}" files and attaches its low-level data structure as a JSON text to the trace.'
        plugin_info = PluginInfo(
            id=PluginId(domain='nfi.nl', category='extract', name='apple_double_kaitai_plugin'),
            version='1.1.0',
            description=plugin_description,
            author=Author('Team Formats', 'formats@nfi.nl', 'Netherlands Forensic Institute'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='',  # e.g. url to the code repository of your plugin
            matcher='$data.fileType=AppleDouble',
            license='Apache License 2.0'
        )
        return plugin_info

    def process(self, trace, data_context):
        # byte arrays shorter than byte_array_length are written as hex in the resulting JSON, longer ones are written
        # to child traces. Change it if necessary!

        kaitai_utils.write_kaitai_to_trace(trace, BYTE_ARRAY_LENGTH)


if __name__ == '__main__':
    # optional main method to run your plugin with Hansken.py
    # see detail at:
    #  https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/dev/python/hanskenpy.html
    run_with_hanskenpy(Plugin)

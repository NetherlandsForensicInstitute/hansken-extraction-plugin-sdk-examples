from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginId, PluginInfo
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger

import kaitai_utils
from structs.apple_single_double import AppleSingleDouble


log = Logger(__name__)


class Plugin(ExtractionPlugin):

    def plugin_info(self):
        plugin_info = PluginInfo(
            id=PluginId(domain='nfi.nl', category='extract', name='apple_double_kaitai_plugin'),
            version='0.0.1',
            description='Parses Apple double files using Kaitai',
            author=Author('Team Formats', 'formats@nfi.nl', 'Netherlands Forensic Institute'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='',  # e.g. url to the code repository of your plugin
            matcher='$data.fileType=AppleDouble',  # add the query for the types of traces your plugin should match
            license='Apache License 2.0'
        )
        return plugin_info

    def process(self, trace, data_context):
        with trace.open(data_type='text', mode='wb') as writer:
            kaitai_utils.write_to_json(trace.open(), writer, AppleSingleDouble)


if __name__ == '__main__':
    # optional main method to run your plugin with Hansken.py
    # see detail at:
    #  https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/dev/python/hanskenpy.html
    run_with_hanskenpy(Plugin)

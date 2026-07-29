from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginId, PluginInfo, PluginResources
from hansken_extraction_plugin.decorators.transformer import transformer
from hansken_extraction_plugin.runtime.extraction_plugin_runner import run_with_hanskenpy
from logbook import Logger

log = Logger(__name__)


class Plugin(ExtractionPlugin):

    def plugin_info(self):
        plugin_info = PluginInfo(
            id=PluginId(domain='nfi.nl', category='extract', name='testbulkmodepython'),
            version='1.0.0',
            description='Reads file and sets a property related to the file size',
            author=Author('NFI', 'tester@holmes.nl', 'NFI'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='https://hansken.org',
            matcher='type:file',
            license='Apache License 2.0',
            resources=PluginResources(maximum_cpu=1, maximum_memory=512, maximum_workers=1),
            bulk_mode=True,
        )
        return plugin_info

    def process(self, trace, data_context):
        data = trace.open()
        if data_context.data_size < 400:
            data.read(data_context.data_size)
            trace.update("event.misc.bulk_data_size", "Smaller than 400 B")
        else:
            data.read(400)
            trace.update("event.misc.bulk_data_size", "Larger than 400 B")


if __name__ == '__main__':
    # Optional main method to run your plugin with Hansken.py
    # See detail at:
    #  https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/dev/python/hanskenpy.html
    run_with_hanskenpy(Plugin)


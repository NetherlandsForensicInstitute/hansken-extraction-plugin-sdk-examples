from typing import Generator

from hansken_extraction_plugin.api.extraction_plugin import DeferredMetaExtractionPlugin
from hansken_extraction_plugin.api.extraction_trace import SearchTrace
from hansken_extraction_plugin.api.plugin_info import Author, MaturityLevel, PluginId, PluginInfo, PluginResources
from hansken_extraction_plugin.api.trace_searcher import TraceSearcher
from logbook import Logger

log = Logger(__name__)


class ChatConversationMessageCountPlugin(DeferredMetaExtractionPlugin):

    def plugin_info(self):
        plugin_info = PluginInfo(
            id=PluginId(domain='nfi.nl', category='chat', name='metadeferredchatconversation'),
            version='1.1.0',
            description='Count number of messages in a chatConversation',
            author=Author('The Externals', 'tester@holmes.nl', 'NFI'),
            maturity=MaturityLevel.PROOF_OF_CONCEPT,
            webpage_url='https://hansken.org', 
            matcher='type:chatConversation',
            license='Apache License 2.0',
            resources=PluginResources(maximum_cpu=2, maximum_memory=512, maximum_workers=6),
        )
        return plugin_info

    def process(self, trace, searcher):
        log.info(f"processing trace {trace.get('id')} {trace.get('name')}")

        message_count = chat_messages(trace.get('id'), searcher)

        trace.update('chatConversation.misc.metaDeferredMessageCount', str(message_count))


def chat_messages(conversation_trace_id: str, searcher: TraceSearcher) -> int:
    query = f'id:{conversation_trace_id}-* AND type:chatMessage'
    log.info(f"querying chat messages: {query}")

    results = searcher.search(query, 20)
    log.info(f"total results: {results.total_results()}")

    return results.total_results()

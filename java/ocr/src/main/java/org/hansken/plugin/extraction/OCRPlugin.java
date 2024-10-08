package org.hansken.plugin.extraction;

import java.io.IOException;

import org.hansken.plugin.extraction.api.Author;
import org.hansken.plugin.extraction.api.DataContext;
import org.hansken.plugin.extraction.api.ExtractionPlugin;
import org.hansken.plugin.extraction.api.MaturityLevel;
import org.hansken.plugin.extraction.api.PluginId;
import org.hansken.plugin.extraction.api.PluginInfo;
import org.hansken.plugin.extraction.api.PluginResources;
import org.hansken.plugin.extraction.api.Trace;
import org.hansken.plugin.extraction.engine.TesseractOCREngine;
import org.hansken.plugin.extraction.settings.TesseractSettings;

public class OCRPlugin implements ExtractionPlugin {
    private final TesseractOCREngine _ocrEngine;

    private static final String TOOL_DOMAIN = "nfi.nl";
    private static final String TOOL_CATEGORY = "document";
    private static final String TOOL_NAME = "OCRPlugin";
    private static final String TOOL_LICENSE = "Apache License, Version 2.0";

    public OCRPlugin() {
        _ocrEngine = new TesseractOCREngine(new TesseractSettings());
    }

    @Override
    public PluginInfo pluginInfo() {
        final Author author = Author.builder()
            .name("The Externals")
            .email("tester@holmes.nl")
            .organisation("NFI")
            .build();

        /*
         Maximum CPU cores is currently set at 4 cores, because Tesseract uses up to four CPU threads while processing a page,
         see https://tesseract-ocr.github.io/tessdoc/FAQ.html#can-i-increase-speed-of-ocr.

         Running the integration test with a different number of cores gives the following result:

         +------+-------------+
         | CPUs | Time to run |
         +------+-------------+
         | 1    | 02m10s      |
         +------+-------------+
         | 2    | 01m00s      |
         +------+-------------+
         | 4    | 00m51s      |
         +------+-------------+
         | 8    | 00m50s      |
         +------+-------------+
         | 12   | 00m49s      |
         +------+-------------+

         The duration does not decrease significantly with more than 4 CPU cores.

         The maximum memory usage is set to 4096 MB.
         The integration test fails with an Out of Memory Exception if the maximum memory usage is less than 4096 MB.
        */
        final PluginResources resources = PluginResources.builder()
            .maximumCpu(4f)
            .maximumMemory(4096)
	    .maximumWorkers(2)
            .build();

        return PluginInfo.builderFor(this)
            .pluginVersion("1.0.0")
            .description("Example Extraction Plugin: Extracting text from documents and pictures by applying OCR")
            .author(author)
            .maturityLevel(MaturityLevel.PROOF_OF_CONCEPT)
            .webpageUrl("https://hansken.org")
            .hqlMatcher("$data.mimeType=image\\/* OR $data.mimeType=application\\/pdf")
            .id(new PluginId(TOOL_DOMAIN, TOOL_CATEGORY, TOOL_NAME))
            .license(TOOL_LICENSE)
            .resources(resources)
            .build();
    }

    @Override
    public void process(final Trace trace, final DataContext dataContext) throws IOException {
        trace.setData("ocr", outputStream -> {
            final String mimeType = trace.get("data." + dataContext.dataType() + ".mimeType");
            _ocrEngine.process(dataContext.data(), mimeType, outputStream);
        });
    }
}

# Java Extraction Plugin SDK

This package contains a couple of example Extraction Plugins to show you how simple the API operates.

# Table of Contents
1. [Chat plugin (basic extraction plugin usage)](#chatplugin)
2. [Location plugin (basic meta processing)](#locationplugin)
3. [Quicklook plugin (basic deferred extraction)](#quicklookplugin)
4. [Secrets plugin (basic data writing)](#secretsplugin)
5. [OCR plugin (basic data writing)](#ocrplugin)
6. [DataTransformationPlugin (basic data transformations)](#DataTransformationPlugin)
7. [DataDigestPlugin (basic data reading)](#DataDigestPlugin)
8. [VectorPlugin (basic vectors)](#VectorPlugin)

## ChatPlugin

This plugin parses a simple made-up chat logs into a message tree.

The package contains the following:

- `main/.../ChatPlugin.java`: the actual Java implementation of the chat tool using the Extraction Plugin API.
- `test/.../ChatPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/*.raw`: a couple of sample chatlogs
    - `test/resources/integration/inputs/*.trace`: these are the properties that allows FLITS to run under the
      assumption that like Hansken, the input trace(chat logs in this case), were already enriched by a different tool
      in the previous extraction round.
    - `test/resources/integration/results`: the expected result traces of running the sample logs through
      our `ChatPlugin.java` Extraction Plugin.


## LocationPlugin

This plugin processes the traces produced by the chatplugin. It tries to detect pseudonymized locations
contained in the chat messages. If one is found, the trace is enhanced with GPS information of that location.
Note that this is not a 'normal' ExtractionPlugin, but a MetaExtractionPlugin. The latter only processes trace
metadata itself, and as such only receives a trace (see `MetaExtractionPlugin.process(Trace)`).
This is different compared to an ExtractionPlugin, which also receives a data stream of that trace
(see `ExtractionPlugin.process(Trace, ExtractionContext)`).

The package contains the following:

- `main/.../ChatLocationPlugin.java`: the actual Java implementation of the location tool using the Meta Extraction Plugin API.
- `test/.../ChatLocationPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/*.trace`: a subset of the traces generated by the chatplugin, which contain
      chat messages which the locationplugin will try to parse
    - `test/resources/integration/results`: the expected result traces of running the traces through
      our `ChatLocationPlugin.java` Meta Extraction Plugin.


## QuickLookPlugin

This plugin extracts thumbnails from thumbnail.data and index.sqlite found in com.apple.QuickLook.thumbnailcache.
This plugin demonstrates how to create a deferred extraction plugin, and how to search for related traces during
the `process(...)`ing of a trace.

The package contains the following:

- `main/.../QuickLookPlugin.java`: the actual Java implementation of the QuickLook tool using the Deferred Extraction Plugin API.
- `test/.../QuickLookPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/thumbnails.trace`: an example thumbnail cache file
        - `test/resources/integration/inputs/thumbnails/searchtraces/.trace`: additional traces which are searched for
          by the plugin.
    - `test/resources/integration/results`: the expected result traces of running the traces through
      our `QuickLookPlugin.java` Deferred Extraction Plugin.


## SecretsPlugin

This plugin is an example for how to add data streams to a trace.  It parses a made up file format which first contains
multiple non-empty lines which represent a single data stream. We add this `text` data stream to the input trace itself
(note that the trace already contains a `raw` stream, namely the file data itself). After the single empty line, there
are multiple base 64 encoded pictures. We create a child trace for each of these and add a `preview` data stream, which
contains the decoded binary data, to each child trace.

The package contains the following:

- `main/.../SecretsPlugin.java`: the actual Java implementation of the secrets plugin
- `test/.../SecretsPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/*.raw`: two example files of previously described format
    - `test/resources/integration/inputs/*.trace`: accompanying traces which already have the file extension property,
      as this is what Hansken would have done as well, and where our plugin matcher triggers on
    - `test/resources/integration/results`: the expected result traces of running the traces through
      our `SecretsPlugin.java`

For the result files, note that more files have been generated than only the result trace file (containing the
fully created trace tree) of each test case. Each new data stream is also written to the result output, both for
the input trace, and the created child traces. The name of each file will contain the id of the trace to which the
data stream belongs, and will have the type of the stream as extension.


## OCRPlugin

This plugin is an example for how to apply OCR on images and PDF files. This plugin uses the Tesseract library (v4) to
recognize text in images. Before this plugin can be used, Tesseract must be installed with the following command (on
Ubuntu):

```commandline
sudo apt-get install tesseract-ocr
```

Instead of installing Tesseract on your system, the plugin can also be run in Docker. The `Dockerfile` file can be
found at `java/ocrplugin/Dockerfile`. To run the plugin via docker the following command can be used:

```commandline
docker build -t ocr-plugin . && docker run -it ocr-plugin
```

The plugin uses images and PDF files as input. Then OCR is applied on these files. If any text is recognized,
the `ocr` data stream will be added to the input trace itself.

The package contains the following:

- `main/.../OCRPlugin.java`: the actual Java implementation of the OCR plugin
- `test/.../OCRPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/*.raw`: multiple test images and PDF files
    - `test/resources/integration/inputs/*.trace`: accompanying traces which already have the mime type property,
      as this is what Hansken would have done as well, and where our plugin matcher triggers on
    - `test/resources/integration/results`: the expected result traces of running the traces through
      our `OCRPlugin.java`


## DataTransformationPlugin

This plugin creates a child trace with a ranged data transformation for each line of a simple made-up chat log.

The package contains the following:

- `main/.../DataTransformationPlugin.java`: the actual Java implementation of the chat tool using the Extraction Plugin API.
- `test/.../DataTransformationPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/*.raw`: a couple of sample chatlogs
    - `test/resources/integration/inputs/*.trace`: these are the properties that allows FLITS to run under the
      assumption that like Hansken, the input trace(chat logs in this case), were already enriched by a different tool
      in the previous extraction round.
    - `test/resources/integration/results`: the expected result traces of running the sample logs through
      our `DataTransformationPlugin.java` Extraction Plugin.


## DataDigestPlugin

This plugin reads data in chunks and calculates an SHA-256 hash over the entire data.

The package contains the following:

- `main/.../DataDigestPlugin.java`: the actual Java implementation of the data digest tool using the Extraction Plugin API.
- `test/.../DataDigestPluginIT.java`: a simple Integration test using the FLITS testing framework. This allows us to
  **test/validate** the plugin input/output without having a running Hansken instance.
    - `test/resources/integration/inputs/picture.jpg`: a sample picture
    - `test/resources/integration/inputs/picture.trace`: the properties that allows FLITS to run under the
      assumption that like Hansken, the input trace (a picture in this case), were already enriched by a different tool
      in the previous extraction round.
    - `test/resources/integration/results`: the expected result traces of running the sample logs through
      our `DataDigestPlugin.java` Extraction Plugin.


## VectorPlugin

This plugin assigns vectors to pictures, so we can find similar pictures by sorting on these vectors.
The implementation is very basic: it will add a vector consisting of the dimensions of the image.
Once indexed, the vectors can be used to find pictures of similar size (by sorting on euclidean or manhattan distance)
or similar aspect ratio (by sorting on cosine similarity).

The package contains the following:

- `main/.../VectorPlugin.java`: the Java implementation of the tool using the Extraction Plugin API.
- `test/.../VectorPluginIT.java`: a basic Integration test using the FLITS testing framework.

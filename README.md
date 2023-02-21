## zyte-api-convertor

A Python module to convert Zyte API Json payload to [Scrapy ZyteAPI](https://github.com/scrapy-plugins/scrapy-zyte-api) project.
It uses Scrapy and scrapy-zyte-api plugin to generate the project, also it uses black to format the code.

### Requirements
```
Python 3.6+
Scrapy
scrapy-zyte-api
black
```

### Documentation

[Zyte API Documentation](https://docs.zyte.com/zyte-api/get-started/index.html)

Test the Zyte API payload using postman or curl. Once it gives the desired response, use the same payload with this module to convert it to a Scrapy ZyteAPI project.

### Installation

`pip install zyte-api-convertor`

### Usage

```shell
    Usage: zyte-api-convertor <payload> --project-name <project_name> --spider-name <spider_name>
    Example: zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project --spider-name sample_spider

    Usage: zyte-api-convertor <payload> --project-name <project_name>
    Example: zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project

    Usage: zyte-api-convertor <payload> --spider-name <spider_name>
    Example: zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --spider-name sample_spider

    Usage: zyte-api-convertor <payload>
    Example: zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}'
```

### Example

zyte-api-convertor expects a valid json payload at the least. But it does have other options as well. You can use the `--project-name` and `--spider-name` options to set the project and spider name. If you don't use these options, it will use the default project and spider name. 

```shell
zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project --spider-name sample_spider
```

Output:

```shell
mukthy@Mukthys-MacBook-Pro % zyte-api-convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project --spider-name sample_spider
Code Generated!
Writing to file...
Writing Done!
reformatted sample_project/sample_project/spiders/sample_project.py

All done! ✨ 🍰 ✨
1 file reformatted.
Formatting Done!
```


Project Created Successfully.

```shell
mukthy@Mukthys-MacBook-Pro %  sample_project % tree
.
├── sample_project
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders
│       ├── __init__.py
│       └── sample_project.py
└── scrapy.cfg

3 directories, 8 files
```

Sample Spider Code:

```python
import scrapy


class SampleQuotesSpider(scrapy.Spider):
    name = "sample_spider"

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "YOUR_API_KEY",
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://httpbin.org/ip",
            meta={
                "zyte_api": {
                    "javascript": False,
                    "screenshot": True,
                    "browserHtml": True,
                    "actions": [],
                    "requestHeaders": {},
                    "geolocation": "US",
                    "experimental": {"responseCookies": False},
                }
            },
        )

    def parse(self, response):
        print(response.text)
```

### Example for POST request

```shell
mukthy@ubuntu:~$ zyte-api-convertor '{

    "url": "https://example.com",
    "httpResponseBody": true,
    "httpRequestMethod": "POST",
    "httpRequestBody": "WyJCV0kiLCAiRkxMIl0=",
    "customHttpRequestHeaders": 

[

        {
            "name": "Content-Type",
            "value": "application/json"
        }
    ]

}'
```

### Output
```python
import scrapy


class SampleQuotesSpider(scrapy.Spider):
    name = "sample_zyte_api"

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
            "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
        },
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000
        },
        "REQUEST_FINGERPRINTER_CLASS": "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "ZYTE_API_KEY": "YOUR-API-KEY",
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://example.com",
            meta={
                "zyte_api": {
                    "customHttpRequestHeaders": [
                        {"name": "Content-Type", "value": "application/json"}
                    ],
                    "geolocation": "US",
                    "httpResponseBody": True,
                    "httpResponseHeaders": True,
                    "experimental": {"responseCookies": False},
                    "httpRequestMethod": "POST",
                    "httpRequestBody": "WyJCV0kiLCAiRkxMIl0=",
                }
            },
        )

    def parse(self, response):
        print(response.text)
```
Please note that the `ZYTE_API_KEY` is not set in the `custom_settings` of the spider. You need to set it before running it.

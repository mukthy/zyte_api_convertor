import json
import subprocess
import sys


def payload_to_zyte(spider_name):
    
    if os.name != 'nt':
        data = sys.argv[1]
        # print(data)
        data = data.replace(',}', '}')
        data = data.replace(',]', ']')
        data = json.loads(data)
        # print(data)

    else:
        print("Windows Detected!, Please enter the payload again.")
        data = input("Enter the JSON Payload with quotes (only): ")
        # print(data)
        data = data.replace(',}', '}')
        data = data.replace(',]', ']')
        data = data.replace("'{", "{")
        data = data.replace("}'", "}")
        data = json.loads(data)
        # print(data)

    url = data['url']
    if 'actions' in data:
        actions = data['actions']
    else:
        actions = []

    # Post request with custom headers
    if 'httpRequestMethod' in data and data['httpRequestMethod'] == "POST" and ('customHttpRequestHeaders' in data):

        httpRequestMethod = data['httpRequestMethod']
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True

        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        if 'customHttpRequestHeaders' in data:
            customHttpRequestHeaders = data['customHttpRequestHeaders']
        else:
            customHttpRequestHeaders = []

        httpRequestBody = data['httpRequestBody']

        meta = {"zyte_api": {"customHttpRequestHeaders": customHttpRequestHeaders, "geolocation": geolocation,
                             "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental, "httpRequestMethod": httpRequestMethod,
                             "httpRequestBody": httpRequestBody}}

    # Post request with request headers
    elif ('httpRequestMethod' in data and data['httpRequestMethod'] == "POST") and ('requestHeaders' in data):

        httpRequestMethod = data['httpRequestMethod']
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True

        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        if 'requestHeaders' in data:
            requestHeaders = data['requestHeaders']
        else:
            requestHeaders = {}

        httpRequestBody = data['httpRequestBody']

        meta = {"zyte_api": {"requestHeaders": requestHeaders, "geolocation": geolocation,
                             "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental, "httpRequestMethod": httpRequestMethod,
                             "httpRequestBody": httpRequestBody}}

    # Post request without request headers
    elif 'httpRequestMethod' in data and data['httpRequestMethod'] == "POST":

        httpRequestMethod = data['httpRequestMethod']
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True

        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        httpRequestBody = data['httpRequestBody']

        meta = {"zyte_api": {"geolocation": geolocation,
                             "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental, "httpRequestMethod": httpRequestMethod,
                             "httpRequestBody": httpRequestBody}}

    # Get request with custom headers
    elif ('httpResponseBody' in data and data['httpResponseBody'] == True) and ('customHttpRequestHeaders' in data):
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True

        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        if 'customHttpRequestHeaders' in data:
            customHttpRequestHeaders = data['customHttpRequestHeaders']
        else:
            customHttpRequestHeaders = []

        meta = {"zyte_api": {"customHttpRequestHeaders": customHttpRequestHeaders, "geolocation": geolocation,
                             "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental}}

    # Get request with request headers
    elif ('httpResponseBody' in data and data['httpResponseBody'] == True) and ('requestHeaders' in data):
        httpResponseBody = data['httpResponseBody']
        httpResponseHeaders = True

        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        if 'requestHeaders' in data:
            requestHeaders = data['requestHeaders']
        else:
            requestHeaders = {}

        meta = {"zyte_api": {"requestHeaders": requestHeaders, "geolocation": geolocation,
                             "httpResponseBody": httpResponseBody, "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental}}

    # BrowserHtml set to True
    elif 'browserHtml' in data and data['browserHtml'] == True:
        browserHtml = data['browserHtml']

        if 'javascript' in data:
            javascript = data['javascript']
        else:
            javascript = False

        if 'screenshot' in data:
            screenshot = data['screenshot']
        else:
            screenshot = False

        if 'requestHeaders' in data:
            requestHeaders = data['requestHeaders']
        else:
            requestHeaders = {}

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        if 'experimental' in data:
            experimental = data['experimental']
        else:
            experimental = {
                "responseCookies": False,
            }

        meta = {"zyte_api": {"javascript": javascript, "screenshot": screenshot,
                             "browserHtml": browserHtml, "actions": actions,
                             "requestHeaders": requestHeaders, "geolocation": geolocation,
                             "experimental": experimental}}

    # Get request without any request headers
    else:
        httpResponseBody = True
        httpResponseHeaders = True
        if 'experimental' in data:
            experimental = data['experiment']
        else:
            experimental = {
                "responseCookies": False,
            }

        if 'geolocation' in data:
            geolocation = data['geolocation']
        else:
            geolocation = "US"

        meta = {"zyte_api": {"geolocation": geolocation, "httpResponseBody": httpResponseBody,
                             "httpResponseHeaders": httpResponseHeaders,
                             "experimental": experimental}}

    formatter = {
        'url': url
    }

    custom_settings = {
        'DOWNLOAD_HANDLERS': {"http": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler",
                              "https": "scrapy_zyte_api.ScrapyZyteAPIDownloadHandler"},
        'DOWNLOADER_MIDDLEWARES': {"scrapy_zyte_api.ScrapyZyteAPIDownloaderMiddleware": 1000},
        'REQUEST_FINGERPRINTER_CLASS': "scrapy_zyte_api.ScrapyZyteAPIRequestFingerprinter",
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'ZYTE_API_KEY': "YOUR_API_KEY"
    }

    data = """
import scrapy
class SampleQuotesSpider(scrapy.Spider):
    name = "{spider_name}"

    custom_settings = {custom_settings}

    def start_requests(self):
        yield scrapy.Request(url="{url}", meta={meta})

    def parse(self, response):
        print(response.text)
""".format(**formatter, meta=meta, custom_settings=custom_settings, spider_name=spider_name)

    return data


def create_scrapy_project(code, project_name):
    subprocess.run(["scrapy", "startproject", f"{project_name}"],
                   stdout=subprocess.DEVNULL)  # create a new scrapy project.
    with open(f"{project_name}/{project_name}/spiders/{project_name}.py",
              "w") as f:  # write the code to a file.
        f.write(code)
    print("Writing Done!")
    subprocess.run(["black",
                    f"{project_name}/{project_name}/spiders/{project_name}.py"])  # format the code using black.
    print("Formatting Done!")


def main():
    try:

        args = sys.argv[1:]
        if "--help" in args:
            usage = '''
    Usage: zyte_api_convertor <payload> --project-name <project_name> --spider-name <spider_name>
    Example: zyte_api_convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project --spider-name sample_spider

    Usage: zyte_api_convertor <payload> --project-name <project_name>
    Example: zyte_api_convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --project-name sample_project

    Usage: zyte_api_convertor <payload> --spider-name <spider_name>
    Example: zyte_api_convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}' --spider-name sample_spider

    Usage: zyte_api_convertor <payload>
    Example: zyte_api_convertor '{"url": "https://httpbin.org/ip", "browserHtml": true, "screenshot": true}'
            '''
            print(usage)
            return

        elif "--project-name" in args and '--spider-name' in args:
            try:
                project_name = args[args.index("--project-name") + 1]
                spider_name = args[args.index("--spider-name") + 1]
                if "-" in project_name:
                    print(
                        "Error: Project names must begin with a letter and contain only\n letters, numbers and underscores")
                    return
                code = payload_to_zyte(spider_name)
                print("Code Generated!")
                print("Writing to file...")
                create_scrapy_project(code, project_name)
                return
            except IndexError:
                print("Please provide a project name and spider name.")
                return

        elif "--project-name" in args:
            try:
                project_name = args[args.index("--project-name") + 1]
                spider_name = "sample_zyte_api"
                if "-" in project_name:
                    print(
                        "Error: Project names must begin with a letter and contain only\n letters, numbers and underscores")
                    return
                code = payload_to_zyte(spider_name)
                print("Code Generated!")
                print("Writing to file...")
                create_scrapy_project(code, project_name)
                return
            except IndexError:
                print("Please provide a project name.")
                return

        elif "--spider-name" in args:
            try:
                spider_name = args[args.index("--spider-name") + 1]
                project_name = "sample_zyte_api_project"
                code = payload_to_zyte(spider_name)
                print("Code Generated!")
                print("Writing to file...")
                create_scrapy_project(code, project_name)
                return
            except IndexError:
                print("Please provide a spider name.")
                return

        elif len(args) < 1:
            print("Please provide a payload, Payload is Must. Use --help for more info")
            return


        else:
            spider_name = "sample_zyte_api"
            code = payload_to_zyte(spider_name)
            print("Code Generated!")
            print("Writing to file...")
            project_name = "sample_zyte_api_project"
            create_scrapy_project(code, project_name)
            return

    except IndexError:
        print("Please provide a payload, Payload is Must. Use --help for more info")
        return


if __name__ == '__main__':
    main()

import scrapy;
import time;
from scrapy.http import FormRequest as FR;
from scrapy.utils.response import open_in_browser as OIB;
from scrapy.selector import Selector;
from scrapy.http import HtmlResponse;
from scrapy.http import Request as Request;


class LMMDT(scrapy.Spider):
    name = "apes_spider";
    start_urls = ["https://lms.lwsd.org/do/account/login"];
    file_urls = [];

    custom_settings = {
        'ITEM_PIPELINES' : {'scrapy.pipelines.files.FilesPipeline': 1},
        'FILES_STORE' : '/files',
        'COOKIES_DEBUG' : True
    }
    def parse(self, response):
        OIB(response);
        return FR.from_response(
            response,
            formdata = {'login': 's-aaprasad', 'password': 'Maxwell2208!'},
            callback = self.timer
            );
    def login(self, response):
        return FR.from_response(
            response,
            formdata = {'login': 's-aaprasad', 'password': 'Maxwell2208!'},
            callback = self.postLogin
            );

    def timer(self, response):
        start = time.time();
        while(time.time() - start < 5):
            self.logger.error("Waiting");
            pass;
        OIB(response);
        return Request(
            "https://lms.lwsd.org/u/s-aaprasad/portal",
            callback = self.postLogin
        )

    def postLogin(self, response):
        if response.request.url == self.start_urls[0]:
            self.logger.error("Login failed");
            return;
        else:
            self.logger.error("Login succeeded");
            self.logger.error(response.request.url);
            return Request("https://lms.lwsd.org/aleslie/stem-apenvironmentalscience-leslie2018-19/cms_page/view", callback = self.apesParse);


    def apesParse(self, response):
        if response.request.url == self.start_urls[0]:
            self.login(response);
        self.logger.error(response.request.url);
        for href in response.css(".nostats"):
            file_urls.append(href);

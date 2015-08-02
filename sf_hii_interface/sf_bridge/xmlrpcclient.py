from firststm import First_STM
from principleadvantage import Principle_Advantage
from healthemedstm import HealtheMed_STM
import urllib
import urllib2
import xmlrpclib
import HTMLParser



class XMLRPCClient(First_STM, Principle_Advantage, HealtheMed_STM):

    def post_xml(self, endpoint, xml_value):
        da = { 'HII_New_Business' : xml_value}
        data = urllib .urlencode(da)
        req = urllib2.Request(endpoint, data )
        req.add_header('Content-Length', len(xml_value))
        urlopen = urllib2.urlopen(req)
        response = urlopen.read()
        return response

    def send_quote(self, endpoint, xml_value):
        server = xmlrpclib.ServerProxy(endpoint)
        result = server.QuoteRequest(xml_value)
        xml_value = result
        htm_parser = HTMLParser.HTMLParser()
        xml_value = htm_parser.unescape(xml_value)
        return xml_value






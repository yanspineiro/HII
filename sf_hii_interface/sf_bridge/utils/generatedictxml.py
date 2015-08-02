from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework.renderers import BaseRenderer
from django.utils import six
from django.utils.xmlutils import SimplerXMLGenerator
from StringIO import StringIO
from django.utils.encoding import smart_text


class XMLRenderer(BaseRenderer):
    """
    Renderer which serializes to XML.
    """
    media_type = 'application/xml'
    format = 'xml'
    charset = 'iso-8859-1'
    item_tag_name = 'list-item'
    list_tags = {
        'Dependents': 'Dependent',
        'addons': 'additional'
    }

    def render(self, data, root_tag='root', accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(root_tag, {})

        self._to_xml(xml, data)

        xml.endElement(root_tag)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            for key, value in six.iteritems(data):
                xml.startElement(key, {})
                for k, v in self.list_tags.iteritems():
                    if key == k:
                        self.item_tag_name = v
                        break
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(smart_text(data))

def test_xml(request,root_tag):
    data = {
        'first_name': 'edilio',
        'last_name': 'gallardo',
        'dependents': [
            {
                'first_name': 'Camila',
                'last_name': 'Gallardo',
                'birth_date': '06/19/2003',
            },
            {
                'first_name': 'Pepe',
                'last_name': 'Gallardo',
                'birth_date': '06/19/2073',
            },
        ],
        'addons': [
            {
                'prod': 'iir',
                'pp': 'jaun',
            }
        ]
    }


    content = XMLRenderer().render(data,root_tag)
    print content

    return HttpResponse(content=content, content_type='application/xml')


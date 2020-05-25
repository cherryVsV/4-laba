import json
import xml.dom.minidom


class json_loader(object):

    @staticmethod
    def parse_loaded_dict(loaded_dict):
        return (loaded_dict['name'],
                loaded_dict['country'],
                '-'.join(map(str, loaded_dict['years'])))

    @staticmethod
    def load(string):
        loaded = json.loads(string)
        if isinstance(loaded, list):
            return [json_loader.parse_loaded_dict(item) for item in loaded]
        else:
            return [json_loader.parse_loaded_dict(loaded)]

    @staticmethod
    def dump(name, country, years):
        return json.dumps({'name': name,
                           'country': country,
                           'years': years.split('-')})


class xml_loader(object):

    @staticmethod
    def load(string):
        parsed = xml.dom.minidom.parseString(string)
        author = parsed.getElementsByTagName('author')[0]
        name = author.getElementsByTagName('name')[0].firstChild.data
        country = author.getElementsByTagName('country')[0].firstChild.data
        years = author.getElementsByTagName('years')[0]
        return (name,
                country,
                '-'.join((years['born'].value, years['died'].value)))

    @staticmethod
    def dump(name, country, years):
        try:
            document = xml.dom.minidom.Document()
            dom_author = document.createElement('author')
            dom_name = document.createElement('name')
            dom_name.appendChild(document.createTextNode(name))
            dom_author.appendChild(dom_name)
            dom_country = document.createElement('country')
            dom_country.data = country
            dom_country.appendChild(document.createTextNode(country))
            dom_author.appendChild(dom_country)
            dom_years = document.createElement('years')
            (dom_years.attributes['born'],
             dom_years.attributes['died']) = years.split('-')
            dom_author.appendChild(dom_years)
            document.appendChild(dom_author)
            return document.toprettyxml()
        except BaseException as e:
            print(e)
            raise
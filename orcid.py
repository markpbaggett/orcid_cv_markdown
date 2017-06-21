from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import xmltodict
import json
import yaml


def header_builder(info):
    given_name = info['record:record']['person:person']['person:name']['personal-details:given-names']
    family_name = info['record:record']['person:person']['person:name']['personal-details:family-name']
    orcid_uri = info['record:record']['common:orcid-identifier']['common:uri']
    biography = info['record:record']['person:person']["person:biography"]["personal-details:content"]
    webpage = info['record:record']['person:person']['researcher-url:researcher-urls']['researcher-url:researcher-url']
    webpage_name = webpage['researcher-url:url-name']
    webpage_uri = webpage['researcher-url:url']
    return "<p style='text-align: center;'>[{0} {1}]({2})\n{3}\n[{4}]({5})</p>"\
        .format(given_name, family_name, orcid_uri, biography, webpage_name, webpage_uri)


def build_cv(x):
    new_cv = open("mark.md", 'w')
    header = header_builder(x)
    new_cv.write('# <p style="text-align: center;">CURRICULUM VITAE</p>')
    new_cv.write('\n\n{0}'.format(header))
    new_cv.write("\n\n##Education\n\n")
    new_cv.write("\n\n##Employment\n\n")
    new_cv.write("\n\n##Creative Activity\n\n")
    new_cv.close


if __name__ == "__main__":
    orcid_details = yaml.load(open('config.yml', 'r'))
    client = BackendApplicationClient(client_id=orcid_details["client_id"])
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://pub.orcid.org/oauth/token', client_id=orcid_details["client_id"],
                              client_secret=orcid_details["client_secret"], scope=orcid_details["scope"])
    client = OAuth2Session(orcid_details["client_id"], token=token)
    r = client.get(orcid_details["orcid_url"])
    orcid_response = json.dumps(xmltodict.parse(r.text))
    orcid_as_json = json.loads(orcid_response)
    build_cv(orcid_as_json)

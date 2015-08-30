import logging
from bs4 import BeautifulSoup

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from googleapiclient.errors import HttpError
import requests

from apiclient.discovery import build

logger = logging.getLogger(__name__)

PREFIX = "https://docs.google.com/document/d/"


class DriveError(Exception):
    pass


def get_doc_info(api_key, file_id):
    service = build('drive', 'v2', developerKey=api_key)
    try:
        file = service.files().get(fileId=file_id).execute()
    except HttpError as e:
        logging.error("Google drive api error: {}".format(e), exc_info=True)
        raise DriveError(e)
    return file


def download(url):
    logger.debug("Getting %s", url)
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def id_from_url(url):
    url = url.strip()
    if not url.startswith(PREFIX):
        raise ValidationError(_("Bad URL"))
    return url[len(PREFIX):].split("/")[0].split("?")[0]


def retrieve_doc_content(doc_id, api_key=None):
    if api_key is None:
        api_key = settings.GDRIVE_API_KEY
    info = get_doc_info(api_key, doc_id)
    return {
        'title': info['title'],
        'text': download(info['exportLinks']['text/plain']),
        'html': download(info['exportLinks']['text/html']),
    }


def extract_body(html):
    """Extracts body tag, dropping everything else, from a google docs html"""
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body
    body.name = 'div'
    return str(body)

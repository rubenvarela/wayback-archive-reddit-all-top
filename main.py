from waybackpy import WaybackMachineSaveAPI
import requests
import re
import random
from dotenv import load_dotenv
import github #PyGithub
import os
from bs4 import BeautifulSoup
import json


def get_ua():
    url = "https://www.useragents.me/"
    r1 = requests.get(url)
    soup = BeautifulSoup(r1.content, 'html.parser')
    elements = soup.select('#most-common-desktop-useragents-json-csv textarea')
    element = elements[0]
    json_text = element.text
    json_data = json.loads(json_text)
    random.shuffle(json_data)
    ua = json_data[0]['ua']

    return ua


def save_gh(data):
    token = os.getenv('ghtoken')
    g = github.Github(token)
    repo = g.get_repo("rubenvarela/wayback-archive-reddit-all-top")

    ts = data.timestamp()
    date_format = '%Y-%m-%d %H.%M.%S'

    body = f"archive_url: {data.archive_url}\n"
    body += f"status_code: {data.status_code}\n"
    body += f"saved_archive: {data.saved_archive}\n"
    body += f"url: {data.url}\n"
    body += f"user_agent: {data.user_agent}\n"
    body += f"cached_save: {data.cached_save}\n"
    body += f"headers: {data.headers}\n"

    path = f"data/{ts.year}/{ts.month}/{ts.day}/{ts.strftime(date_format)}.txt"

    repo.create_file(
        path,
        message=f"New export created {ts.strftime(date_format)} - {ts.strftime(date_format)}.txt",
        content=body,
        branch="main"
    )


def main():
    ua = get_ua()
    url = "https://old.reddit.com/r/all/top/"

    save_api = WaybackMachineSaveAPI(url, ua)
    save_api.save()

    save_gh(save_api)


if __name__ == '__main__':
    load_dotenv()
    main()

import requests


def dl_file(pu_url, pu_path):
    # TODO: Retry the download based on the retries and delay specified in the constants file
    data = requests.get(pu_url)
    # Save file data to local copy
    with open(pu_path, 'wb') as o_file:
        o_file.write(data.content)

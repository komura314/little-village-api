import os
import requests
import xmltodict


class HatenaApi():
    HATENA_API_USER = os.environ.get('HATENA_API_USER')
    HATENA_API_BLOG = os.environ.get('HATENA_API_BLOG')
    HATENA_API_KEY = os.environ.get('HATENA_API_KEY')

    HATENA_API_URL_HEADER = 'https://blog.hatena.ne.jp'
    HATENA_API_URL_FUTTER = 'atom'

    def getAllEntries(self):

        all_entries = []
        url = self.getHatenaApiFirstUrl('entry')

        while url != '':
            hatenaApiData = self.getHatenaApi(url)

            for entry in self.getApiEntries(hatenaApiData):
                all_entries.append(self.formatEntry(entry))
            url = self.getHatenaApiNextUrl(hatenaApiData)

        return all_entries

    def getHatenaApi(self, url):
        auth = self.getHatenaApiAuth()
        hatena_list = requests.get(url, auth=auth)
        dict_data = xmltodict.parse(hatena_list.text, encoding='utf-8')
        return dict_data

    def getApiEntries(self, hatenaApiData):
        return self.getDictValue(hatenaApiData, ['feed', 'entry'])

    def formatEntry(self, entry):
        format_entry = {}
        format_entry['hatena_entry_id'] = self.getHatenaEntryId(entry)
        format_entry['category'] = self.getCategory(entry)
        format_entry['title'] = self.getDictValue(entry, ['title'])
        format_entry['summary'] = self.getDictValue(
            entry, ['summary', '#text'])
        format_entry['content_md'] = self.getDictValue(
            entry, ['content', '#text'])
        format_entry['content_html'] = self.getDictValue(
            entry, ['hatena:formatted-content', '#text'])
        format_entry['draft'] = self.getDictValue(
            entry, ['app:control', 'app:draft'])
        format_entry['updated_at'] = self.getDictValue(
            entry, ['updated'], None)
        format_entry['edited_at'] = self.getDictValue(
            entry, ['app:edited'], None)

        return format_entry

    def getHatenaEntryId(self, entry):
        id_all = self.getDictValue(entry, ['id'])
        id = id_all[id_all.rfind('-') + 1:] if id_all else ''
        return id

    def getCategory(self, entry):
        category_all = self.getDictValue(entry, ['category'])
        if isinstance(category_all, list):
            category = category_all[0]
        else:
            category = category_all
        return self.getDictValue(category, ['@term'])

    def getHatenaApiFirstUrl(self, action):

        url = [
            self.HATENA_API_URL_HEADER,
            self.HATENA_API_USER,
            self.HATENA_API_BLOG,
            self.HATENA_API_URL_FUTTER,
            action
        ]
        return os.path.join(*url)

    def getHatenaApiNextUrl(self, hatenaApiEntries):
        url = ''
        links = self.getDictValue(hatenaApiEntries, ['feed', 'link'])
        if isinstance(links, list):
            for link in links:
                if self.getDictValue(link, ['@rel']) == 'next':
                    url = self.getDictValue(link, ['@href'])
        return url

    def getHatenaApiAuth(self):

        return (self.HATENA_API_USER, self.HATENA_API_KEY)

    def getDictValue(self, dictData, keys, emptyValue=''):
        for key in keys:
            if isinstance(dictData, dict):
                if key in dictData:
                    dictData = dictData[key]
            else:
                return emptyValue
        return dictData

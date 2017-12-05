import requests
import logging
from basecone.lib import Artifact, Document, Transaction


BASE_URL = 'https://api.basecone.com/v1'


class Client:
    def __init__(self, client_id, api_access_key, company_id, limit=100):
        self.client_id = client_id
        self.api_access_key = api_access_key
        self.company_id = company_id
        self.limit = limit

    def do_get(self, uri):
        url = '{0}/{1}'.format(BASE_URL, uri)
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.api_access_key)
        return requests.get(url, auth=auth)

    def artifacts(self, document_id):
        result = self.do_get('documents/{0}/artifacts'.format(document_id))
        ret = list()
        for a in result.json()['artifacts']:
            a = Artifact(a['artifactId'], document_id, a['pageCount'],
                         a['contentType'], a['type'])
            ret.append(a)

        return ret

    def download_artifact(self, artifact):
        page_id = 1
        content_type = 'application/pdf'
        result = self.do_get('documents/{0}/artifacts/{1}?pageId={2}&'
                             'contentType={3}'.format(artifact.docment_id,
                                                      artifact.id, page_id,
                                                      content_type))
        return result.content

    def transaction(self, id):
        result = self.do_get('transactions/{0}'.format(id)).json()
        return Transaction(result['transactionId'], result['type'],
                           result['documentId'], result['transactionNumber'],
                           result['transactionDate'], result['description'],
                           result['totalAmount'], result['currency']['code'])

    def documents(self):
        result = self.do_get('documents?limit={0}'
                             '&companyId={1}'.format(self.limit,
                                                     self.company_id))

        documents = result.json()['documents']
        logging.info('Fetched %d documents', len(documents))

        ret = list()
        for d in documents:
            document = Document(d['documentId'],
                                d['name'], d['company'], d['createdOn'], d['modifiedOn'],
                                d['transactionProposalId'], d['transactionId'])

            if document.transaction_id:
                logging.info('Transaction id for %s is %s', document.id,
                             document.transaction_id)
                document.transaction = self.transaction(document.transaction_id)

            document.artifacts = self.artifacts(document.id)

            ret.append(document)

        return ret

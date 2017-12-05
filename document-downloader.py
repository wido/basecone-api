#!/usr/bin/python3
import os
import logging
import json
from config import *
from basecone import Client

DOWNLOAD_DIR = './downloads'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Starting to talk to Basecone')


def download_transactions(company_id):
    client = Client(CLIENT_ID, API_SECRET_KEY, company_id, LIMIT)
    transactions = list()

    basedir = '{0}/{1}'.format(DOWNLOAD_DIR, company_id)
    if not os.path.isdir(basedir):
        os.mkdir(basedir)

    for doc in client.documents():
        for artifact in doc.artifacts:
            if not doc.transaction:
                logger.warning('Document %s has no transaction. Skipping',
                               doc.id)
                continue

            transaction_number = doc.transaction.transaction_number

            directory = '{0}/{1}'.format(basedir, transaction_number)

            data = {
                'transaction_number': transaction_number,
                'currency': doc.transaction.currency,
                'total_amount': doc.transaction.total_amount,
                'description': doc.transaction.description,
                'date': doc.transaction.transaction_date
            }

            transactions.append(data)

            if not os.path.isdir(directory):
                os.mkdir(directory)

                data = {
                    'currency': doc.transaction.currency,
                    'total_amount': doc.transaction.total_amount,
                    'description': doc.transaction.description,
                    'date': doc.transaction.transaction_date
                }

                jsonfile = '{0}/{1}.json'.format(directory, transaction_number)
                logger.info('Writing to %s', jsonfile)
                with open(jsonfile, 'wt') as fh:
                    fh.write(json.dumps(data, indent=2) + os.linesep)

                body = client.download_artifact(artifact)
                pdffile = '{0}/{1}.pdf'.format(directory, transaction_number)
                logger.info('Writing to %s', pdffile)
                with open(pdffile, 'wb') as fh:
                    fh.write(body)

    database_file = '{0}/transactions.csv'.format(basedir)
    logger.info('Writing to database file %s', database_file)

    with open(database_file, 'wt') as fh:
        fh.write('transaction_number;date;currency;total_amount;description'
                 + os.linesep)

        for t in transactions:
            date = t['date'].split('T')[0]
            line = '{0};{1};{2};{3};{4}'.format(t['transaction_number'],
                                                date,
                                                t['currency'],
                                                t['total_amount'],
                                                t['description'])
            fh.write(line + os.linesep)


for id in COMPANY_IDS:
    download_transactions(id)

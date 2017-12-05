class Transaction:
    def __init__(self, id, type, document_id, transaction_number,
                 transaction_date, description, total_amount, currency):
        self.id = id
        self.type = type
        self.document_id = document_id
        self.transaction_number = transaction_number
        self.transaction_date = transaction_date
        self.description = description
        self.total_amount = total_amount
        self.currency = currency

class Document:
    def __init__(self, id, name, company, created_on, modified_on,
                 transaction_proposal_id=None, transaction_id=None):
        self.id = id
        self.name = name
        self.company = company
        self.created_on = created_on
        self.modified_on = modified_on
        self.transaction_proposal_id = transaction_proposal_id
        self.transaction_id = transaction_id
        self.artifacts = None
        self.transaction = None

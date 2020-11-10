from typing import Iterable


class InvertedIndex:
    def __init__(self, documents: Iterable):
        self.doc_id = {}  # Internal Id
        self.doc_no = {}  # Document No
        self.index = {}  # Posting list for every word
        self.document_count = 0
        self.make_index(documents)

    def make_index(self, documents: Iterable):
        for doc_no, text in documents:
            doc_id = len(self.doc_id)  # Assign internal id
            self.document_count += 1
            self.doc_id[doc_no] = doc_id
            self.doc_no[doc_id] = doc_no
            for word in text.split():
                if not word:
                    continue
                if word not in self.index:
                    self.index[word] = set()
                self.index[word].add(doc_id)
        for word, posting_list in self.index.items():
            self.index[word] = sorted(posting_list)  # Sort posting list for later merging

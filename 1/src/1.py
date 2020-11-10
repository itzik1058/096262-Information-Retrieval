from typing import Iterable, List
from pathlib import Path
import xml.etree.ElementTree as ET


class InvertedIndex:
    def __init__(self, documents: Iterable[ET.Element]):
        self.doc_id = {}
        self.doc_no = {}
        self.index = {}
        self.make_index(documents)

    def make_index(self, documents: Iterable[ET.Element]):
        for document in documents:
            try:
                doc_no = document.find('DOCNO').text
                text = document.find('TEXT').text
                doc_id = len(self.doc_id)
                self.doc_id[doc_no] = doc_id
                self.doc_no[doc_id] = doc_no
                for word in text.split():
                    if word not in self.index:
                        self.index[word] = set()
                    self.index[word].add(doc_id)
            except AttributeError:
                pass
        for word, posting_list in self.index.items():
            self.index[word] = sorted(posting_list)


def boolean_retrieval(inv_index: InvertedIndex, query_expr: List):
    while len(query_expr) > 1:
        operand1 = query_expr.pop(0)
        operand2 = query_expr.pop(0)
        operator = query_expr.pop(0)
        result = []
        if isinstance(operand1, str):
            operand1 = inv_index.index[operand1]
        if isinstance(operand2, str):
            operand2 = inv_index.index[operand2]
        idx1, idx2 = 0, 0
        while idx1 < len(operand1) and idx2 < len(operand2):
            if operand1[idx1] < operand2[idx2]:
                if operator == 'OR' or operator == 'NOT':
                    result.append(operand1[idx1])
                idx1 += 1
            elif operand1[idx1] > operand2[idx2]:
                if operator == 'OR':
                    result.append(operand2[idx2])
                idx2 += 1
            elif operand1[idx1] == operand2[idx2]:
                if operator == 'OR' or operator == 'AND':
                    result.append(operand1[idx1])
                idx1 += 1
                idx2 += 1
        while idx1 < len(operand1):
            if operator == 'OR' or operator == 'NOT':
                result.append(operand1[idx1])
            idx1 += 1
        while idx2 < len(operand2):
            if operator == 'OR':
                result.append(operand2[idx2])
            idx2 += 1
        query_expr.insert(0, result)
    result = query_expr.pop(0)
    if isinstance(result, str):
        result = inv_index.index[result]
    return result


def iterate_documents(path: Path):
    for p in path.iterdir():
        if not p.is_file():
            continue
        with p.open('r', errors='ignore') as f:
            text = f.read()
            print(f)
            text = text.replace('</DOCNO>\n</TEXT>', '</DOCNO>\n<TEXT></TEXT>')  # Fix broken </TEXT>
            root = ET.fromstring(f'<root>{text}</root>')
            for document in root:
                yield document


def main():
    data = Path('../data/')
    inv_index = InvertedIndex(iterate_documents(data / 'AP_Coll_Parsed'))
    with (data / 'BooleanQueries.txt').open('r') as f:
        queries = f.read().splitlines()
        for query in queries:
            print(boolean_retrieval(inv_index, query.split()))


if __name__ == '__main__':
    main()

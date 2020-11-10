from inverted_index import InvertedIndex
from boolean_retrieval import boolean_retrieval
from pathlib import Path
from re import findall


def iterate_documents(path: Path):
    for i, p in enumerate(path.iterdir()):
        if i != 0 and i % 100 == 0:
            print(f'{i} document files fetched')
        if not p.is_file():
            continue
        with p.open('r', errors='ignore') as f:
            documents = f.read().split('</DOC>')
            for document in documents:  # Yield all documents in file
                doc_no = findall('<DOCNO>(.+?)</DOCNO>', document)
                if not doc_no:
                    continue
                doc_no = doc_no[0].strip()
                text = findall('<TEXT>(.*?)</TEXT>', document.replace('\n', ''))
                if not text:
                    continue
                text = ' '.join(text)
                yield doc_no, text


def main():
    data = Path('../data/')
    inv_index = InvertedIndex(iterate_documents(data / 'AP_Coll_Parsed'))
    results = []
    with (data / 'BooleanQueries.txt').open('r') as f:  # Read boolean queries
        queries = f.read().splitlines()
        for query in queries:
            result = boolean_retrieval(inv_index, query.lower().split())
            results.append(' '.join(sorted(result)))
    with (data / 'Part_2.txt').open('w') as r:  # Write query results
        r.write('\n'.join(results))
    # Word document frequencies
    frequency = {word: len(documents) / inv_index.document_count for word, documents in inv_index.index.items()}
    frequent_words = sorted(inv_index.index, key=lambda w: frequency[w], reverse=True)
    with (data / 'Part_3.txt').open('w') as r:
        r.write(' '.join(frequent_words[:10]) + '\n')
        r.write(' '.join(frequent_words[-10:]) + '\n')


if __name__ == '__main__':
    main()

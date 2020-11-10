from inverted_index import InvertedIndex
from typing import List


def boolean_retrieval(inv_index: InvertedIndex, query_expr: List):
    while len(query_expr) > 1:
        operand1 = query_expr.pop(0)  # First operand
        operand2 = query_expr.pop(0)  # Second operand
        operator = query_expr.pop(0)  # Set Operator
        result = []
        if isinstance(operand1, str):
            operand1 = inv_index.index.get(operand1, [])  # Convert word to its posting list
        if isinstance(operand2, str):
            operand2 = inv_index.index.get(operand2, [])  # Convert word to its posting list
        # Merge posting lists w.r.t operator
        idx1, idx2 = 0, 0
        while idx1 < len(operand1) and idx2 < len(operand2):
            if operand1[idx1] < operand2[idx2]:
                if operator in ('or', 'not'):
                    result.append(operand1[idx1])
                idx1 += 1
            elif operand1[idx1] > operand2[idx2]:
                if operator == 'or':
                    result.append(operand2[idx2])
                idx2 += 1
            elif operand1[idx1] == operand2[idx2]:
                if operator in ('or', 'and'):
                    result.append(operand1[idx1])
                idx1 += 1
                idx2 += 1
        # Write leftovers
        result += operand1[idx1:] * (operator in ('or', 'not')) + operand2[idx2:] * (operator == 'or')
        query_expr.insert(0, result)
    result = query_expr.pop(0)
    if isinstance(result, str):
        result = inv_index.index.get(result, [])  # Convert word to its posting list if necessary
    return [inv_index.doc_no[doc_id] for doc_id in result]

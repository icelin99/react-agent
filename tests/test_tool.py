import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.pdf_query_tools import pdf_query, get_embeddings

test_query = "租房合同中，房东可以随意涨房租吗？"

result = pdf_query(test_query)
print(f"---result: {result}")
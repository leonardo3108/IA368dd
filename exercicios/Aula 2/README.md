# Exercício da Aula 2: buscador booleano/BoW e TF-IDF

* Link do [roteiro do curso](https://github.com/leonardo3108/IA368dd#readme)
* [Instruções, regras e dicas](../instrucoes.md)

## Enunciado
1. Usar o BM25 implementado pelo pyserini para buscar queries no TREC-DL 2020
   - Documentação referencia: https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md
2. Implementar um buscador booleano/bag-of-words.
3. Implementar um buscador com TF-IDF
4. Avaliar implementações 1, 2, e 3 no TREC-DL 2020 e calcular o nDCG@10

Nos itens 2 e 3:
- Fazer uma implementação que suporta buscar eficientemente milhões de documentos.
- Não se pode usar bibliotecas como sklearn, que já implementam o BoW e TF-IDF.


## Artefatos gerados
1. [process_docs.py](process_docs.py) - baixa, preprocessa e processa as passagens do MS Marco, gerando arquivos pickle para pesquisa rápida:
   - índice invertido - data/inverted_index.pickle
   - frequência dos termos - data/term_frequencies.pickle
   - tamanho dos documentos - doc_lengths.pickle
2. [process_queries.py](process_queries.py) - baixa, preprocessa e processa as queries com avaliação no TREC 2020 DL passages, gerando arquivos pickle com resultados de pesquisa:
   - pesquisa booleana - data/retrieved_boolean.pickle
   - pesquisa com ranking TF-IDF - data/retrieved_tf_idf.pickle
3. [evaluate_queries.py](evaluate_queries.py) - avaliação das pesquisas booleana e com TF-IDF por meio da métrica nBCG
4. [BM25.ipynb](BM25.ipynb) - pesquisa com BM25 do pyserini, resultados e avaliação
5. [Saved_Chat_GPT_1.md](Saved_Chat_GPT_1.md) - conversas realizadas com o ChatGPT

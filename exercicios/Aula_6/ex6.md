# Exercício - Aula 5/6

## Enunciado

* Treinar um modelo seq2seq (a partir do T5-base) na tarefa de expansão de documentos usando o doc2query
* Usar como treino o dataset "tiny" do MS MARCO na tarefa doc2query
https://storage.googleapis.com/unicamp-dl/ia368dd_2023s1/msmarco/msmarco_triples.train.tiny.tsv
* doc2query: A entrada é a passagem e o target é a query
Note que apenas pares (query, passagem relevante) são usados como treino.
O treino é relativamente rápido (<1 hora).
* Validar a cada X steps usando o sacreBLEU 
* A parte lenta deste exercício é a pré-indexação: para cada documento da coleção, temos que gerar uma ou mais queries, que depois são concatenadas ao documento original, e esse documento "expandido" é indexado.
* Avaliar no TREC-COVID (171K docs), pois é menor que o MS MARCO/TREC-DL 2020 (8.8M passagens). 
  * Indice invertido do Trec-covid no pyserini: beir-v1.0.0-trec-covid-flat
  * Corpus e queries na HF: https://huggingface.co/datasets/BeIR/trec-covid
  * qrels: https://huggingface.co/datasets/BeIR/trec-covid-qrels
  * Usar nDCG@10
  * Comparar com o BM25 com e sem os documentos expandidos pelo doc2query
  
## Solução - Etapas 
1. [Finetuning do modelo](Aula_6_Finetuning.ipynb)
2. [Geração das queries](Aula_6_Generation.ipynb)
3. [Indexação, busca e avaliação](Aula_6_Indexing_Search_Evaluation.ipynb)

  
## Resultados
Métrica: nDCG@10
* documentos originais:  0,5963
* documentos aumentados: 0,6373

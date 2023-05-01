# Enunciado - Aula 3

Reranqueamento usando um modelo estilo-BERT com o treinamento no dataset do MS MARCO e avaliação no TREC-DL 2020
* O treinamento é igual ao de um classificador binário, que será feito por vocês.
* O que muda é a forma de avaliação: reranqueadores precisam ser alimentados com documentos candidatos (ex: trazidos pelo BM25 - exercício aula 1)
* Sugestão: usar este dataset reduzido do MS MARCO como treinamento, com 10k triplas (query, passagem relevante, passagem não-relevante):
  * https://storage.googleapis.com/unicamp-dl/ia368dd_2023s1/msmarco/msmarco_triples.train.tiny.tsv
* Sugestão: usar miniLM (modelo BERT pequeno, 5x mais rapido) para começar o finetuning:
  * https://huggingface.co/nreimers/MiniLM-L6-H384-uncased pois oferece um bom compromisso entre qualidade e velocidade.
* Sugestão: usar este notebook como base
* Análise de sentimentos (dataset IMDB) usando um modelo estilo BERT: https://colab.research.google.com/drive/10etP7Lb915EC-uEuf1IKC8DYkyg_om6-?usp=sharing
* Sugestão de debug: usar este minilm para ver se consegue ndcg ~0.70: https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2
* Sugestão: fazer overfit em um batch: treinar por 200 epocas um unico batch, e ver se consegue loss=0, e acuracia=100%, ou ndcg=1

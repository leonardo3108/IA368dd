# Enunciado - Aula 7/8 - Busca esparsa - SPLADE

Implementar a fase de indexação e buscas de um modelo sparso
- Usar este modelo SPLADE já treinado naver/splade_v2_distil (do distilbert) ou splade-cocondenser-selfdistil (do BERT-base 110M params). Mais informações sobre os modelos estão neste artigo: https://arxiv.org/pdf/2205.04733.pdf
- Não é necessário treinar o modelo
- Avaliar nDCG@10 no TREC-COVID e comparar resultados com o BM25 e buscador denso da semana passada

A dificuldade do exercício está em implementar a função de busca e ranqueamento usada pelo SPLADE. A implementação deve ser codificada e usar implementação do SPLADE apenas para comparação. A implementação do índice invertido é apenas um "dicionário python".

- Fazer a comparação dos seus resultados com a busca "original" do SPLADE.
- Medir latência (s/query)

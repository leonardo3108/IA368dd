# Enunciado - Aula 5

Treinar um modelo de linguagem em dados em portugues
- Avaliar o modelo usando a perplexidade, que é simplesmente a exponencial de todas as losses do dataset de validação
- Iremos treinar o modelo para prever o próximo token dado os anteriores (também conhecido como Causal Language Modeling). Não confundir com o Masked Language Modeling (MLM), que consiste em prever tokens mascarados em uma dada sequência (ex: BERT's MLM)

Dicas:
- Usar como ponto de partida o modelo [OPT-125M](https://huggingface.co/facebook/opt-125m), que já foi treinado em 300B de tokens (maioria em Inglês)
- Usar este dataset reduzido do mc4 portugues, com ~300M de tokens: [mc4-pt-sample-1g.txt](https://unicamp-dl/ia025a_2022s1/aula9/sample-1gb.txt)
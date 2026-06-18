# Jogo de PC do Roleta Russa

Recriação em Python do programa **Roleta Russa**, exibido na RecordTV entre 2002 e 2003. Feito com pygame.

> Baixe a versão mais recente em **[github.com/AlexTorres10/ProgramaRoletaRussa/releases](https://github.com/AlexTorres10/ProgramaRoletaRussa/releases)**

Não há intenção de infringimento de direitos autorais. Todos os direitos reservados à RecordTV e à Sony Television. Este é um jogo criado por um grande fã do programa, sem fins lucrativos.

---

## Como jogar

Assim como o programa original, são 5 jogadores — humanos ou bots — que respondem perguntas de conhecimentos gerais e jogam a roleta, que pode eliminá-los do jogo.

### A Roleta
- **Normal:** o jogador que errou a pergunta joga a roleta; buracos vermelho indicam as zonas de perigo. Humanos param com Espaço ou clicando na alavanca; bots param automaticamente.
- **Carrasco:** o líder joga a roleta para eliminar um dos jogadores em risco.
- **Abertura:** jogo inicial para definir quem será o primeiro desafiante da rodada.

---

## Bots

O jogo conta com **5 níveis de dificuldade** de bot (1 = mais fácil, 5 = mais difícil). Cada jogador pode ser configurado individualmente como humano ou bot de qualquer nível pelo menu de configurações.

---

## Melhorias em relação ao programa original

- Bots jogáveis com 5 níveis de dificuldade
- Valores das premiações corrigidos pela inflação (opção configurável)
- Dinheiro arredondado — ninguém mais ganhará R$ 23.898, e sim R$ 23.900
- Opção de rodada 1 estendida
- Pergunta bônus se todos os 5 jogadores acertarem na mesma rodada
- Questão extra para que todos os jogadores tenham chance de responder
- Editor de perguntas integrado (`editor.py`)

---

## Opções de configuração

| Opção | Descrição |
|---|---|
| Jogadores | Nome e tipo de cada um dos 5 jogadores (humano ou bot nível 1–5) |
| Valores novos | Usa os valores de premiação corrigidos pela inflação |
| Rodada 1 estendida | Ativa a versão estendida da primeira rodada (vai até 7 perguntas, independente de como ela acontecer) |
| Extra — não responde | Permite perguntas extras numa rodada até todos os jogadores responderem ao menos uma (máximo de 7 perguntas) |
| Extra — escapa | Permite pergunta extra se um jogador escapar de uma situação 5×1 sem dinheiro |
| Bônus — todos acertam | Pergunta bônus quando as 5 perguntas são acertadas |

---

## Instalação (para rodar o código-fonte)

```bash
# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Inicie o jogo
python main.py

# Editor de perguntas (app separado)
python editor.py
```

O jogo deve ser executado a partir da raiz do projeto — todos os caminhos de assets (`img/`, `sons/`, `fonts/`, `base/`) são relativos.

---

## Base de perguntas

As perguntas ficam em `base/main.csv` (separado por ponto e vírgula, UTF-8). Use o `editor.py` para adicionar, editar ou remover perguntas sem precisar mexer no CSV diretamente.

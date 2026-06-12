# Semáforo Inteligente - Simulação de Máquina de Estados

Este projeto consiste na simulação de um sistema de controle para um **Semáforo Inteligente**, desenvolvido em Python utilizando a biblioteca gráfica **Tkinter**. O sistema modela o comportamento real de cruzamentos urbanos modernos, integrando conceitos de Engenharia de Software e Sistemas Digitais, como Máquinas de Estados Finitos (FSM), Filas de Prioridade (FIFO com interrupção), Teoria de Conjuntos e mapeamento de saídas binárias para hardware.

## 🚀 Funcionalidades

- **Interface Gráfica Interativa:** Simulação visual em tempo real dos estados das vias (Via A, Via B e Pedestres) utilizando componentes nativos do Tkinter.
- **Fila de Prioridade Dinâmica:** Gerenciamento inteligente de solicitações por ordem de chegada com regras rígidas de interrupção:
  - **Emergência:** Veículos de emergência (ambulâncias, viaturas) interrompem imediatamente o ciclo atual, zerando o temporizador para liberação imediata da via.
  - **Idoso / PCD:** Pedestres prioritários possuem tempo de travessia estendido e aplicam uma regra de otimização que encurta o tempo verde das vias de carros para no máximo 2 segundos, agilizando o atendimento.
- **Mapeamento Binário (10-bits):** Simulação de registradores de hardware, onde cada estado do semáforo gera uma string binária correspondente para o acionamento de LEDs físicos:
  - `Ordem dos bits:` A(Vermelho, Amarelo, Verde), B(Vermelho, Amarelo, Verde), Pedestre(Vermelho, Verde), Emergência, Idoso.
- **Visualização de Teoria de Conjuntos:** Exibição em tempo real dos conjuntos de entidades em espera ($A$, $B$, $P$, $I$, $E$) e do conjunto Universo ($U$) representando a união de todas as demandas do sistema.
- **Logs no Console:** Exibição automática da Tabela de Decisão e do Grafo de Transição de Estados no terminal assim que a aplicação é iniciada.

---

## 🛠️ Pré-requisitos e Tecnologias

Antes de executar o projeto, certifique-se de ter o Python instalado em sua máquina.

- **Python 3.x**
- **Tkinter** (Biblioteca padrão do Python para interfaces gráficas)

Nenhuma biblioteca externa adicional (via `pip`) é estritamente necessária para rodar o script original.

---

## 💻 Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [[https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)](https://github.com/allysonsilvadev/Projeto-A3.py/tree/main)

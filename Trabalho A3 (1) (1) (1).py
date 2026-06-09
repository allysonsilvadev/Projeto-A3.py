# Trabalho A3 - Semáforo Inteligente
# Simulação de máquina de estados usando Tkinter

import tkinter as tk

# Conjuntos para armazenar quem está esperando
carrosA = set()
carrosB = set()
pedestres = set()
idosos = set()
emergencia = set()

# Fila de prioridade
fila = []

estado = "AMARELO PISCANTE"
tempo = 0

# Dicionário com os tempos de cada fase do semáforo
tempos = {
    "VIA A VERDE": 5,
    "VIA B VERDE": 5,
    "AMARELO A": 2,
    "AMARELO B": 2,
    "PEDESTRE ATIVO": 5,
    "PEDESTRE IDOSO": 9,
    "EMERGENCIA": 5,
    "AMARELO PISCANTE": 1
}

# Mapeando os bits das luzes
# Ordem: A(verm, amar, verde), B(verm, amar, verde), P(verm, verde), emergência, idoso
binario = {
    "VIA A VERDE": "0011001000",
    "AMARELO A": "0101001000",
    "VIA B VERDE": "1000011000",
    "AMARELO B": "1000101000",
    "PEDESTRE ATIVO": "1001000100",
    "PEDESTRE IDOSO": "1001000101",
    "EMERGENCIA": "1001001010",
    "AMARELO PISCANTE": "0100101000"
}

# Mapeamento da máquina de estados (quem pode ir pra onde)
grafo = {
    "AMARELO PISCANTE": ["VIA A VERDE", "VIA B VERDE", "PEDESTRE ATIVO", "PEDESTRE IDOSO", "EMERGENCIA"],
    "VIA A VERDE": ["AMARELO A", "EMERGENCIA"],
    "AMARELO A": ["VIA B VERDE", "PEDESTRE ATIVO", "PEDESTRE IDOSO", "EMERGENCIA"],
    "VIA B VERDE": ["AMARELO B", "EMERGENCIA"],
    "AMARELO B": ["VIA A VERDE", "PEDESTRE ATIVO", "PEDESTRE IDOSO", "EMERGENCIA"],
    "PEDESTRE ATIVO": ["VIA A VERDE", "VIA B VERDE", "AMARELO PISCANTE"],
    "PEDESTRE IDOSO": ["VIA A VERDE", "VIA B VERDE", "AMARELO PISCANTE"],
    "EMERGENCIA": ["AMARELO PISCANTE"]
}


def colocar_na_fila(tipo):
    global tempo

    if tipo not in fila:
        fila.append(tipo)

    if tipo == "A":
        carrosA.add("carro A")
    elif tipo == "B":
        carrosB.add("carro B")
    elif tipo == "P":
        pedestres.add("pedestre")
    elif tipo == "I":
        idosos.add("idoso/PCD")
    elif tipo == "E":
        emergencia.add("emergencia")

    # Se for ambulância/polícia, zera o tempo pra forçar a troca no ciclo atual
    if tipo == "E":
        tempo = 0

    # Regra do idoso: corta o tempo do farol verde dos carros pra no máximo 2s
    if tipo == "I":
        if estado == "VIA A VERDE" or estado == "VIA B VERDE":
            if tempo > 2:
                tempo = 2

    atualizar_textos()


# Funções dos botões
def clickA():
    colocar_na_fila("A")

def clickB():
    colocar_na_fila("B")

def clickP():
    colocar_na_fila("P")

def clickIdoso():
    colocar_na_fila("I")

def clickEmergencia():
    colocar_na_fila("E")


def limpar():
    global estado, tempo

    # Zera tudo
    carrosA.clear()
    carrosB.clear()
    pedestres.clear()
    idosos.clear()
    emergencia.clear()
    fila.clear()

    estado = "AMARELO PISCANTE"
    tempo = 0

    atualizar_luzes()
    atualizar_textos()


def escolher_pedido():
    # Se não tem ninguém na fila, não faz nada
    if len(fila) == 0:
        return None

    # Emergência fura a fila de todo mundo
    if "E" in fila:
        return "E"

    # Idosos e PCDs passam na frente dos pedestres e carros comuns
    if "I" in fila:
        return "I"

    # Se não tem prioridade máxima, pega o primeiro da fila (FIFO)
    return fila[0]


def estado_do_pedido(pedido):
    if pedido == "A":
        return "VIA A VERDE"
    elif pedido == "B":
        return "VIA B VERDE"
    elif pedido == "P":
        return "PEDESTRE ATIVO"
    elif pedido == "I":
        return "PEDESTRE IDOSO"
    elif pedido == "E":
        return "EMERGENCIA"


def precisa_amarelo(proximo_estado):
    if proximo_estado == "EMERGENCIA":
        return None

    if estado == "VIA A VERDE" and proximo_estado != "VIA A VERDE":
        return "AMARELO A"

    if estado == "VIA B VERDE" and proximo_estado != "VIA B VERDE":
        return "AMARELO B"

    return None


def tirar_da_fila(tipo):
    if tipo in fila:
        fila.remove(tipo)


def terminar_atendimento():
    # Limpa o conjunto correspondente e tira da fila quando o tempo acaba
    if estado == "VIA A VERDE":
        carrosA.clear()
        tirar_da_fila("A")
    elif estado == "VIA B VERDE":
        carrosB.clear()
        tirar_da_fila("B")
    elif estado == "PEDESTRE ATIVO":
        pedestres.clear()
        tirar_da_fila("P")
    elif estado == "PEDESTRE IDOSO":
        idosos.clear()
        tirar_da_fila("I")
    elif estado == "EMERGENCIA":
        emergencia.clear()
        tirar_da_fila("E")


def sensores():
    # Retorna 1 se tiver alguém esperando, 0 se estiver vazio
    a = 1 if len(carrosA) > 0 else 0
    b = 1 if len(carrosB) > 0 else 0
    p = 1 if len(pedestres) > 0 else 0
    i = 1 if len(idosos) > 0 else 0
    e = 1 if len(emergencia) > 0 else 0

    return a, b, p, i, e


def texto_fila():
    if len(fila) == 0:
        return "vazia"

    nomes = []
    for item in fila:
        if item == "A":
            nomes.append("Via A")
        elif item == "B":
            nomes.append("Via B")
        elif item == "P":
            nomes.append("Pedestre")
        elif item == "I":
            nomes.append("Idoso/PCD")
        elif item == "E":
            nomes.append("Emergência")

    return " -> ".join(nomes)


def atualizar_textos():
    a, b, p, i, e = sensores()

    # Atualiza as labels na interface
    texto_sensores["text"] = f"Sensores: A={a} | B={b} | Ped={p} | Idoso={i} | Emergência={e}"
    texto_estado["text"] = f"Estado: {estado}"
    texto_tempo["text"] = f"Tempo restante: {tempo}s"
    texto_binario["text"] = f"Binário: {binario[estado]}"
    texto_fila_label["text"] = f"Fila: {texto_fila()}"

    texto_conjuntos["text"] = (
        "Conjuntos:\n"
        f"A = {carrosA}\n"
        f"B = {carrosB}\n"
        f"P = {pedestres}\n"
        f"I = {idosos}\n"
        f"E = {emergencia}\n"
        f"U = {carrosA.union(carrosB).union(pedestres).union(idosos).union(emergencia)}"
    )


def atualizar_luzes():
    # Gerencia as cores dos labels simulando os LEDs do semáforo
    if estado == "VIA A VERDE":
        cor_a["bg"] = "green"
        cor_b["bg"] = "red"
        cor_p["bg"] = "red"

    elif estado == "VIA B VERDE":
        cor_a["bg"] = "red"
        cor_b["bg"] = "green"
        cor_p["bg"] = "red"

    elif estado == "AMARELO A":
        cor_a["bg"] = "yellow"
        cor_b["bg"] = "red"
        cor_p["bg"] = "red"

    elif estado == "AMARELO B":
        cor_a["bg"] = "red"
        cor_b["bg"] = "yellow"
        cor_p["bg"] = "red"

    elif estado in ("PEDESTRE ATIVO", "PEDESTRE IDOSO"):
        cor_a["bg"] = "red"
        cor_b["bg"] = "red"
        cor_p["bg"] = "green"

    elif estado == "EMERGENCIA":
        cor_a["bg"] = "red"
        cor_b["bg"] = "red"
        cor_p["bg"] = "red"

    elif estado == "AMARELO PISCANTE":
        # Faz a lógica de piscar invertendo as cores
        if cor_a["bg"] == "yellow":
            cor_a["bg"] = "black"
            cor_b["bg"] = "black"
        else:
            cor_a["bg"] = "yellow"
            cor_b["bg"] = "yellow"

        cor_p["bg"] = "red"


def rodarSemaforo():
    global estado, tempo

    if tempo > 0:
        tempo -= 1

        if tempo == 0:
            terminar_atendimento()

        atualizar_luzes()
        atualizar_textos()
        janela.after(1000, rodarSemaforo) # Roda de novo em 1s
        return

    pedido = escolher_pedido()

    if pedido is None:
        estado = "AMARELO PISCANTE"
        tempo = tempos[estado]

        atualizar_luzes()
        atualizar_textos()
        janela.after(1000, rodarSemaforo)
        return

    proximo_estado = estado_do_pedido(pedido)
    amarelo = precisa_amarelo(proximo_estado)

    # Verifica se precisa passar pelo amarelo antes de trocar
    if amarelo is not None:
        estado = amarelo
    else:
        estado = proximo_estado

    tempo = tempos[estado]

    atualizar_luzes()
    atualizar_textos()

    janela.after(1000, rodarSemaforo)


def mostrar_tabela():
    print("--- TABELA DE DECISÃO ---")
    print("A B P I E | Resultado")
    print("0 0 0 0 0 | Amarelo piscante")
    print("1 0 0 0 0 | Via A verde")
    print("0 1 0 0 0 | Via B verde")
    print("0 0 1 0 0 | Pedestre ativo")
    print("0 0 0 1 0 | Pedestre idoso/PCD")
    print("x x x x 1 | Emergência")
    print("\nPrioridade utilizada:")
    print("Emergência > Idoso/PCD > Ordem de chegada (FIFO)\n")


def mostrar_grafo():
    print("--- GRAFO DOS ESTADOS ---")
    for chave, valor in grafo.items():
        print(f"{chave} -> {valor}")


# --- Configuração da Interface Gráfica (Tkinter) ---
janela = tk.Tk()
janela.geometry("430x720")
janela.title("Semáforo Inteligente")

tk.Label(janela, text="Semáforo Inteligente", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(janela, text="Carro Via A", width=25, command=clickA).pack(pady=4)
tk.Button(janela, text="Carro Via B", width=25, command=clickB).pack(pady=4)
tk.Button(janela, text="Pedestre Comum", width=25, command=clickP).pack(pady=4)
tk.Button(janela, text="Pedestre Idoso/PCD", width=25, command=clickIdoso).pack(pady=4)
tk.Button(janela, text="Emergência", width=25, command=clickEmergencia).pack(pady=4)
tk.Button(janela, text="Limpar", width=25, command=limpar).pack(pady=4)

texto_sensores = tk.Label(janela, text="")
texto_sensores.pack(pady=8)

texto_estado = tk.Label(janela, text="", font=("Arial", 12, "bold"))
texto_estado.pack(pady=5)

texto_tempo = tk.Label(janela, text="")
texto_tempo.pack(pady=5)

texto_binario = tk.Label(janela, text="")
texto_binario.pack(pady=5)

texto_fila_label = tk.Label(janela, text="")
texto_fila_label.pack(pady=5)

tk.Label(janela, text="VIA A").pack()
cor_a = tk.Label(janela, width=15, height=2, bg="gray")
cor_a.pack(pady=3)

tk.Label(janela, text="VIA B").pack()
cor_b = tk.Label(janela, width=15, height=2, bg="gray")
cor_b.pack(pady=3)

tk.Label(janela, text="PEDESTRE").pack()
cor_p = tk.Label(janela, width=15, height=2, bg="gray")
cor_p.pack(pady=3)

texto_conjuntos = tk.Label(janela, text="", justify="left")
texto_conjuntos.pack(pady=12)

# Inicializando prints do console e loop da interface
mostrar_tabela()
mostrar_grafo()

atualizar_luzes()
atualizar_textos()

janela.after(1000, rodarSemaforo)
janela.mainloop()
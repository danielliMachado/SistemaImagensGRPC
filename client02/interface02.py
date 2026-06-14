import tkinter as tk
from tkinter import messagebox
import grpc
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import image_service_pb2
import image_service_pb2_grpc

SERVER_IP = "localhost"

channel = grpc.insecure_channel(
    f"{SERVER_IP}:50051"
)

stub = image_service_pb2_grpc.ImageServiceStub(channel)


def listar_imagens():

    lista.delete(
        0,
        tk.END
    )

    resposta = stub.ListImages(
        image_service_pb2.Empty()
    )

    for imagem in resposta.filenames:

        lista.insert(
            tk.END,
            imagem
        )


def baixar_imagem():

    selecionado = lista.curselection()

    if not selecionado:

        messagebox.showwarning(
            "Aviso",
            "Selecione uma imagem."
        )

        return

    nome_imagem = lista.get(
        selecionado[0]
    )

    os.makedirs(
        "downloads_cliente2",
        exist_ok=True
    )

    resposta = stub.DownloadImage(
        image_service_pb2.ImageRequest(
            filename=nome_imagem
        )
    )

    caminho = os.path.join(
        "downloads_cliente2",
        nome_imagem
    )

    with open(
        caminho,
        "wb"
    ) as arquivo:

        for chunk in resposta:

            arquivo.write(
                chunk.data
            )

    messagebox.showinfo(
        "Cliente 2",
        f"Imagem salva em:\n{caminho}"
    )


janela = tk.Tk()

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

largura_janela = largura_tela // 2
altura_janela = altura_tela - 100

janela.geometry(
    f"{largura_janela}x{altura_janela}+{largura_janela}+0"
)

janela.title(
    "CLIENTE 2 - Download"
)


tk.Label(
    janela,
    text="CLIENTE 2",
    font=("Arial", 18, "bold")
).pack(pady=10)

tk.Button(
    janela,
    text="Listar Imagens",
    width=30,
    command=listar_imagens
).pack(pady=10)

lista = tk.Listbox(
    janela,
    width=70,
    height=12
)

lista.pack(pady=15)

tk.Button(
    janela,
    text="Baixar Imagem",
    width=30,
    command=baixar_imagem
).pack(pady=10)

janela.mainloop()
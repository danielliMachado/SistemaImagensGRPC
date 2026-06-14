import tkinter as tk
from tkinter import filedialog, messagebox
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

stub = image_service_pb2_grpc.ImageServiceStub(
    channel
)

arquivo_selecionado = ""


def selecionar_imagem():

    global arquivo_selecionado

    arquivo_selecionado = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")
        ]
    )

    if arquivo_selecionado:

        lbl_arquivo.config(
            text=os.path.basename(
                arquivo_selecionado
            )
        )


def enviar_imagem():

    if arquivo_selecionado == "":

        messagebox.showwarning(
            "Aviso",
            "Selecione uma imagem."
        )

        return

    nome_arquivo = os.path.basename(
        arquivo_selecionado
    )

    def gerar_chunks():

        with open(
            arquivo_selecionado,
            "rb"
        ) as imagem:

            while True:

                dados = imagem.read(1024)

                if not dados:
                    break

                yield image_service_pb2.ImageChunk(
                    filename=nome_arquivo,
                    data=dados
                )

    try:

        resposta = stub.UploadImage(
            gerar_chunks()
        )

        messagebox.showinfo(
            "Cliente 1",
            resposta.message
        )

        listar_imagens()

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


def listar_imagens():

    try:

        lista.delete(
            0,
            tk.END
        )

        resposta = stub.ListImages(
            image_service_pb2.Empty()
        )

        if not resposta.filenames:

            lista.insert(
                tk.END,
                "Nenhuma imagem encontrada."
            )

            return

        for imagem in resposta.filenames:

            lista.insert(
                tk.END,
                imagem
            )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


def excluir_imagem():

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

    confirmar = messagebox.askyesno(
        "Confirmação",
        f"Deseja excluir '{nome_imagem}'?"
    )

    if not confirmar:
        return

    try:

        resposta = stub.DeleteImage(
            image_service_pb2.ImageRequest(
                filename=nome_imagem
            )
        )

        messagebox.showinfo(
            "Cliente 1",
            resposta.message
        )

        listar_imagens()

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )


# ==========================
# JANELA
# ==========================

janela = tk.Tk()

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

largura_janela = largura_tela // 2
altura_janela = altura_tela - 100

janela.geometry(
    f"{largura_janela}x{altura_janela}+0+0"
)


janela.title(
    "CLIENTE 1 - Upload e Gerenciamento"
)



janela.resizable(
    False,
    False
)

titulo = tk.Label(
    janela,
    text="CLIENTE 1",
    font=("Arial", 18, "bold")
)

titulo.pack(
    pady=10
)

subtitulo = tk.Label(
    janela,
    text="Upload, Listagem e Exclusão de Imagens",
    font=("Arial", 10)
)

subtitulo.pack(
    pady=5
)

btn_selecionar = tk.Button(
    janela,
    text="Selecionar Imagem",
    width=30,
    command=selecionar_imagem
)

btn_selecionar.pack(
    pady=10
)

lbl_arquivo = tk.Label(
    janela,
    text="Nenhuma imagem selecionada"
)

lbl_arquivo.pack()

btn_enviar = tk.Button(
    janela,
    text="Enviar Imagem",
    width=30,
    command=enviar_imagem
)

btn_enviar.pack(
    pady=10
)

btn_listar = tk.Button(
    janela,
    text="Listar Imagens",
    width=30,
    command=listar_imagens
)

btn_listar.pack(
    pady=10
)


lista = tk.Listbox(
    janela,
    width=70,
    height=12
)

lista.pack(
    pady=15
)

btn_excluir = tk.Button(
    janela,
    text="Excluir Imagem",
    width=30,
    command=excluir_imagem
)

btn_excluir.pack(
    pady=10
)

listar_imagens()

janela.mainloop()
import grpc
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import image_service_pb2
import image_service_pb2_grpc

SERVER_IP = "192.168.3.9"

channel = grpc.insecure_channel(
    f"{SERVER_IP}:50051"
)

stub = image_service_pb2_grpc.ImageServiceStub(channel)


def upload_image(caminho):

    nome_arquivo = os.path.basename(caminho)

    def gerar_chunks():

        with open(caminho, "rb") as imagem:

            while True:

                dados = imagem.read(1024)

                if not dados:
                    break

                yield image_service_pb2.ImageChunk(
                    filename=nome_arquivo,
                    data=dados
                )

    resposta = stub.UploadImage(
        gerar_chunks()
    )

    print("\n" + resposta.message)


def listar_imagens():

    resposta = stub.ListImages(
        image_service_pb2.Empty()
    )

    print("\nImagens disponíveis:\n")

    if not resposta.filenames:

        print("Nenhuma imagem encontrada.")
        return

    for imagem in resposta.filenames:
        print("-", imagem)


def baixar_imagem(nome_imagem):

    os.makedirs(
        "downloads",
        exist_ok=True
    )

    resposta = stub.DownloadImage(
        image_service_pb2.ImageRequest(
            filename=nome_imagem
        )
    )

    caminho = os.path.join(
        "downloads",
        nome_imagem
    )

    with open(caminho, "wb") as arquivo:

        for chunk in resposta:
            arquivo.write(chunk.data)

    print(
        f"\nImagem salva em: {caminho}"
    )


if __name__ == "__main__":

    print("\n===== SISTEMA DE IMAGENS gRPC =====\n")

    print("1 - Enviar imagem")
    print("2 - Listar imagens")
    print("3 - Baixar imagem")

    opcao = input("\nEscolha: ")

    if opcao == "1":

        caminho = input(
            "\nDigite o caminho da imagem: "
        )

        upload_image(caminho)

    elif opcao == "2":

        listar_imagens()

    elif opcao == "3":

        nome = input(
            "\nDigite o nome da imagem: "
        )

        baixar_imagem(nome)

    else:

        print("\nOpção inválida!")
import grpc
from concurrent import futures
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import image_service_pb2
import image_service_pb2_grpc

IMAGE_DIR = "images"

os.makedirs(IMAGE_DIR, exist_ok=True)


class ImageService(image_service_pb2_grpc.ImageServiceServicer):

    def UploadImage(self, request_iterator, context):

        filename = None

        for chunk in request_iterator:

            filename = chunk.filename
            filepath = os.path.join(IMAGE_DIR, filename)

            with open(filepath, "ab") as f:
                f.write(chunk.data)

        return image_service_pb2.UploadResponse(
            success=True,
            message="Imagem recebida com sucesso!"
        )

    def ListImages(self, request, context):

        arquivos = os.listdir(IMAGE_DIR)

        return image_service_pb2.ImageList(
            filenames=arquivos
        )

    def DownloadImage(self, request, context):

        filepath = os.path.join(
            IMAGE_DIR,
            request.filename
        )

        if not os.path.exists(filepath):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Imagem não encontrada")
            return

        with open(filepath, "rb") as f:

            while True:

                data = f.read(1024)

                if not data:
                    break

                yield image_service_pb2.ImageChunk(
                    filename=request.filename,
                    data=data
                )


def serve():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    image_service_pb2_grpc.add_ImageServiceServicer_to_server(
        ImageService(),
        server
    )

    # Aceita conexões de outros computadores
    server.add_insecure_port("0.0.0.0:50051")

    server.start()

    print("Servidor rodando na porta 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
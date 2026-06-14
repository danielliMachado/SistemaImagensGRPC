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
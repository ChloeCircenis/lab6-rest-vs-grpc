import grpc
from concurrent import futures

import lab6_pb2
import lab6_pb2_grpc
from PIL import Image
import io
import base64


class Lab6Service(lab6_pb2_grpc.Lab6Servicer):

    def DotProduct(self, request, context):
        a = request.a
        b = request.b

        if len(a) != len(b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(x * y for x, y in zip(a, b))
        return lab6_pb2.dotProductReply(dotproduct=result)
        
    def Add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            return lab6_pb2.imageReply(
                width=img.width,
                height=img.height
            )
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid image"
            )

    def JsonImage(self, request, context):
        try:
            image_bytes = base64.b64decode(
                request.img, validate=True
            )
            img = Image.open(io.BytesIO(image_bytes))

            return lab6_pb2.imageReply(
                width=img.width,
                height=img.height
            )
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid Base64 image"
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    lab6_pb2_grpc.add_Lab6Servicer_to_server(
        Lab6Service(), server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("gRPC server running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
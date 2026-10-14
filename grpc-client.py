import grpc
import random
import time
import argparse
import base64
import lab6_pb2
import lab6_pb2_grpc

parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument(
    'cmd',
    choices=['add', 'dotProduct', 'rawImage', 'jsonImage']
)
parser.add_argument('reps', type=int)
parser.add_argument('-d', '--debug', action='store_true')

args = parser.parse_args()

# Connect to the gRPC server
channel = grpc.insecure_channel(f'{args.host}:50051')
stub = lab6_pb2_grpc.Lab6Stub(channel)

# Prepare inputs before timing
if args.cmd == 'dotProduct':
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

elif args.cmd in ('rawImage', 'jsonImage'):
    with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
        img = f.read()

    if args.cmd == 'jsonImage':
        encoded = base64.b64encode(img).decode('ascii')

def doDotProduct(debug=False):
    # a = [random.random() for _ in range(100)]
    # b = [random.random() for _ in range(100)]

    request = lab6_pb2.dotProductMsg(a=a, b=b)
    response = stub.DotProduct(request)

    if debug:
        expected = sum(x * y for x, y in zip(a, b))
        print("Server result:", response.dotproduct)
        print("Expected result:", expected)

def doAdd(debug=False):
    request = lab6_pb2.addMsg(a=5, b=10)
    response = stub.Add(request)

    if debug:
        print("Sum:", response.sum)


def doRawImage(debug=False):
    # with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
    #     img = f.read()

    request = lab6_pb2.rawImageMsg(img=img)
    response = stub.RawImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)


def doJsonImage(debug=False):
    # with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
    #     img = f.read()

    # encoded = base64.b64encode(img).decode('ascii')

    request = lab6_pb2.jsonImageMsg(img=encoded)
    response = stub.JsonImage(request)

    if debug:
        print("Width:", response.width)
        print("Height:", response.height)
# Measure performance

operations = {
    'add': doAdd,
    'dotProduct': doDotProduct,
    'rawImage': doRawImage,
    'jsonImage': doJsonImage
}

start = time.perf_counter()

for _ in range(args.reps):
    operations[args.cmd](debug=args.debug)

delta = ((time.perf_counter() - start) / args.reps) * 1000

print(f"Took {delta:.3f} ms per operation")

channel.close()
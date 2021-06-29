import grpc
import image_pb2_grpc
import image_pb2
import imageRecog
from concurrent import futures
import logging

class ImagePreprocessingServicer(image_pb2_grpc.ImagePreprocessingServicer):
    def facerecog(self,request,context):
        response = image_pb2.UserInfo()
        response.status = imageRecog.FaceRecog(request.b64image,request.width,request.height)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_ImagePreprocessingServicer_to_server(ImagePreprocessingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Grpc server started successfully......")
    server.wait_for_termination()
    
if __name__ == '__main__':
    logging.basicConfig()
    serve()

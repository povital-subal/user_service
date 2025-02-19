import grpc
from concurrent import futures
from .proto import user_pb2, user_pb2_grpc
from .models import User

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        try:
            user = User.objects.get(id=request.user_id)
            return user_pb2.UserResponse(
                user_id=user.id,
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )
        except User.DoesNotExist:
            context.set_details("User not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return user_pb2.UserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("User Service gRPC server running on port 50051...")
    server.wait_for_termination()

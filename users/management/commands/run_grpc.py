from django.core.management.base import BaseCommand
from users.grpc_server import serve

class Command(BaseCommand):
    help = 'Start the gRPC server for User Service'

    def handle(self, *args, **kwargs):
        serve()

from django.contrib.auth.models import User
from rest_framework import generics, status, permissions, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sessions.models import Session
from sessions.permissions import IsObjectOwnerOrReadOnly
from sessions.serializers import SessionSerializer


class SessionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    filterset_fields = ("city",)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.query_params.get('city'):
            return Response({"detail": "In order to get the sessions, a city must be given in the params."})
        return self.list(self, request, *args, **kwargs)


class SessionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsObjectOwnerOrReadOnly]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()


class SessionJoinOrLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        session = get_object_or_404(Session, pk=pk)
        if request.user not in session.users.all():
            session.users.add(request.user)
            return Response(status=status.HTTP_202_ACCEPTED)

        elif request.user in session.users.all():
            return Response(
                data={"detail": "User is already in the session."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif session.player_limit <= len(session.users.all()):
            return Response(
                data={"detail": "Player limit already satisfied."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        session = get_object_or_404(Session, pk=pk)

        if request.user == session.owner:
            return Response(
                {
                    "detail": "An owner can not leave its own session but only delete it."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.user in session.users.all():
            session.users.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        elif request.user not in session.users.all():
            return Response(
                data={"detail": "You must be in the session to be able to leave it."},
                status=status.HTTP_400_BAD_REQUEST,
            )

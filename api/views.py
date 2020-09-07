from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from hashlib import md5

from .models import (
    Member,
    Team,
    Ticket,
    TicketComment,
    TicketStatus
)
from .serializers import (
    TicketSerializer,
    MemberSerializer,
    TeamSerializer,
    TicketCommentSerializer,
)
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class MemberViewSet(viewsets.ModelViewSet):
    """
    CRUD stuff inherited from ModelViewSet
    """

    queryset = Member.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    serializer_class = MemberSerializer

    # i think it should be reasonable that when members are created, the authenticated user
    # is the one that the member record references
    def create(self, request, *args, **kwargs):
        team_id = request.data.get("team_id")

        try:
            team = Team.objects.get(id=team_id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user=self.request.user, team=team)

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # requiring that all updates are partial instead of full
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["put"])
    def approve(self, request):
        """ approve the join request """
        return Response({"msg": "sucess"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def leave(self, request):
        """ leave this team """
        return Response({"msg": "sucess"}, status=status.HTTP_200_OK)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly | IsAdminOrReadOnly
    ]

    serializer_class = TeamSerializer

    # requiring that all updates are partial instead of full
    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def search(self, request, search_term=None):
        """ retrieve teams based on a user search term. ideally i would want to use something like
            cosine similarity
        """
        pass


class TicketViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        # IsOwnerOrReadOnly | IsAdminOrReadOnly, ignoring these until we get owner field squared away
    ]

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=False, methods=["get"])
    def list_team(self, request, pk=None):
        queryset = Ticket.objects.filter(team__id=pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TicketCommentViewSet(viewsets.ModelViewSet):
    """
    Basic crud should be pre-generated, so we only need to do the more complicated calls
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly | IsAdminOrReadOnly,
    ]

    queryset = TicketComment.objects.all()
    serializer_class = TicketCommentSerializer

    @action(detail=False)
    def recent_comments(self, request, team_id=None):
        """ This call returns the first page of comments associated with the given team_id """
        pass


class TicketStatusViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly | IsAdminOrReadOnly
    ]

    queryset = TicketStatus.objects.all()

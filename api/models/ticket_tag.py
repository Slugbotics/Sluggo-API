# this here defines the ticket_tags
from django.db import models
import uuid
from .team import Team
from .ticket import Ticket
from api.models.interfaces import HasUuid, TeamRelated
from hashlib import md5


class TagManager(models.Manager):
    def create(self, **obj_data):
        title = obj_data.get("title")
        team = obj_data.get("team")

        if not title or not team:
            raise ValueError("missing title or team")

        title_id = "{}".format(title)
        team_id = "{}".format(team.id)
        obj_data["team_title_hash"] = md5(title_id.encode()).hexdigest() + md5(team_id.encode()).hexdigest()
        return super().create(**obj_data)


class Tag(HasUuid, TeamRelated):
    team_title_hash = models.CharField(max_length=256, unique=True, editable=False)
    title = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    activated = models.DateTimeField(null=True, blank=True)
    deactivated = models.DateTimeField(null=True, blank=True)
    objects = TagManager()

    class Meta:
        ordering = ["id"]
        app_label = "api"

    def __str__(self):
        return f"Tag: {self.title}"


class TicketTagManager(models.Manager):
    def create(self, **obj_data):
        tag = obj_data.get("tag")
        ticket = obj_data.get("ticket")

        if not tag or not ticket:
            raise ValueError("missing tag or team")

        team_id = "{}".format(tag.id)
        ticket_id = "{}".format(ticket.id)
        obj_data["id"] = md5(team_id.encode()).hexdigest() + md5(ticket_id.encode()).hexdigest()
        return super().create(**obj_data)


class TicketTag(HasUuid, TeamRelated):
    id = models.CharField(max_length=256, unique=True, editable=False, primary_key=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    activated = models.DateTimeField(null=True, blank=True)
    deactivated = models.DateTimeField(null=True, blank=True)
    objects = TicketTagManager()

    class Meta:
        ordering = ["created"]
        app_label = "api"

    def __str__(self):
        return f"TicketTag: {self.created}"

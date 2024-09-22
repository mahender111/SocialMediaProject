from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, 
        choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], 
        default='pending'
    )

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f'{self.sender} -> {self.receiver} ({self.status})'


class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user1} & {self.user2} (Since: {self.created_at})'


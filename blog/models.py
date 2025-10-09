from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post (models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='posts/', blank=True)
	description = models.TextField()
	likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.author.username}: {self.description[:20]}..."

	def total_likes(self):
		return self.likes.count()

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.author.username}: {self.text[:20]}..."



class Coinshakhzot(models.Model):
	coin = models.IntegerField(default=0)

	def __str__(self):
		return f"Монет: {self.coin}"


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	bio = models.TextField(blank=True, null=True)
	city = models.CharField(max_length=100, blank=True, null=True)
	birth_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.user.username



class Follow(models.Model):
	follower = models.ForeignKey(
		User,
		related_name='following',
		on_delete=models.CASCADE
	)

	followed = models.ForeignKey(
		User,
		related_name='followers', 
		on_delete=models.CASCADE
	)

	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('follower', 'followed')

	def __str__(self):
		return f"{self.follower.username} follows {self.followed.username}"
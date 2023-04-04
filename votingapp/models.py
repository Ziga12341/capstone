from django.contrib.auth.models import AbstractUser
from django.db import models


class Suggestions(models.Model):
    name = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    # user that created the suggestion
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="suggestions")
    likes = models.ManyToManyField("User", null=True, related_name="likes")
    open_by = models.ManyToManyField("User", blank=True, related_name="opened_suggestions")
    list = models.ForeignKey("Categorised_list", on_delete=models.CASCADE, related_name="suggestions")

    def __str__(self):
        return f"{self.name}"


# optional: add suggestions that users already seen (suggestions that are not new suggestions for him)
# optional: add option user to add profile picture
# optional: add option user to add profile description
class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"


class Categorised_list(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="lists")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, related_name="lists")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} {self.group}"


class Group(models.Model):
    group_name = models.CharField(max_length=64)
    group_description = models.TextField()
    group_image = models.URLField(blank=True, null=True) # optional
    created_at = models.DateTimeField(auto_now_add=True)
    # each group can have many categories, but each category can have only one group - one-to-many relationship
    categories = models.ForeignKey("Category", blank=True, related_name="groups", on_delete=models.CASCADE)
    owner = models.ForeignKey("User", on_delete=models.CASCADE, null=True, related_name="owner")
    members = models.ManyToManyField("User", related_name="group_members", null=False)

    def __str__(self):
        return f"{self.group_name}"


class Category(models.Model):
    category_name = models.CharField(max_length=64)
    # one suggestion can have only one category - each suggestion in one category
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category_name}"


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comments")
    suggestion = models.ForeignKey("Suggestions", on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.content}"

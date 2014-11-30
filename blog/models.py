from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=250, blank=True)

    def __unicode__(self):
        return(self.title)

    @models.permalink
    def get_absolute_url(self):
        return(("blog:category-posts", (), {"slug": self.slug}))

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class PostManager(models.Manager):
    def live(self):
        return(self.model.objects.filter(published=True))


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False,
                                      unique=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False,
                                      unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, default='')
    content = models.TextField()
    published = models.BooleanField(default=True)
    author = models.ForeignKey(User, related_name="posts")
    objects = PostManager()
    category = models.ForeignKey(Category, related_name="posts")

    def __unicode__(self):
        return(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "title"]

    @models.permalink
    def get_absolute_url(self):
        return(("blog:detail", (), {"slug": self.slug}))

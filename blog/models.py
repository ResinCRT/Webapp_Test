from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from tinymce.models import HTMLField

# Create your models here.
class Post(models.Model):
    title = models.CharField('TITLE', max_length=50)
    slug = models.SlugField('SLUG', allow_unicode=True, max_length=50, unique=True, help_text="one word for title alias.")
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text="simple description text.")
    content = HTMLField('CONTENT')

    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    #modify_dt = models.DateTimeField('MODIFY DATE', auto_now=True)
    modify_dt = models.DateTimeField('MODIFY DATE')
    read_cnt = models.IntegerField('READ COUNT', default = 0)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER', blank=True, null=True)
    tags = TaggableManager(blank=True)


    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog_posts'

        # -이면 내림차순
        ordering = ('-modify_dt',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.slug,))

    def get_previous(self):
        return self.get_previous_by_modify_dt()

    def get_next(self):
        return self.get_next_by_modify_dt()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class PostAttachFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="files",
                             verbose_name='Post', blank=True, null=True)
    upload_file = models.FileField(upload_to="%Y/%M/%d", null=True, blank= True, verbose_name='파일')

    filename = models.CharField(max_length=64, null=True, verbose_name='첨부파일명')

    content_type = models.CharField(max_length=128, null=True,
                                    verbose_name='MIME TYPE')
    size = models.IntegerField('파일 크기')

    def __str__(self):
        return self.filename

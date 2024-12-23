# context_processors.py
from .models import Region, Post

def unique_posts_by_region(request):
    posts = Post.objects.all().order_by('-created_at')
    regions = Region.objects.all().order_by('name')
    unique_posts_by_region = {}

    for region in regions:
        seen_titles = set()
        unique_posts = []
        for post in Post.objects.filter(region=region):
            if post.title not in seen_titles:
                unique_posts.append(post)
                seen_titles.add(post.title)
        unique_posts_by_region[region] = unique_posts

    return {'posts': posts, 'regions': regions, 'unique_posts_by_region': unique_posts_by_region}

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def robots_txt(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        'Disallow: /admin/',
        '',
        f'Sitemap: {request.build_absolute_uri("/sitemap.xml")}',
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')


def sitemap_xml(request):
    base = request.build_absolute_uri('/').rstrip('/')
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base}/</loc>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
'''
    return HttpResponse(xml, content_type='application/xml')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('', include('landing.urls')),
]

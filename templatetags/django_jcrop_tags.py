import json

from django import template
from django.template import defaultfilters as filters

register = template.Library()


def render_jcrop_widget(template, crop_settings):
    updated_crop_settings = dict(crop_settings)
    updated_crop_settings['jcrop'] = json.dumps(
        updated_crop_settings.get('jcrop', '')
    ).replace('"', "'")

    return (
        filters.safe(template.format(**updated_crop_settings))
        if updated_crop_settings.get("url", "") else
        ""
    )


@register.filter
def django_jcrop_widget(crop_settings):
    crop_widget_html = """
<img
    class="djangoJcrop {klass}"
    alt="{url}"
    src="{url}"
    data-output-id="{output_key}"
    data-jcrop="{jcrop}"
></img>
<input id="{output_key}" name="{output_key}" value="" type="hidden">
</input>
"""
    return render_jcrop_widget(crop_widget_html, crop_settings)


@register.simple_tag
def init_django_jcrop():
    init_django_jcrop_html = """
<script>
$(document).ready(function() {{
    $(".djangoJcrop").djangoJcrop();
}});
</script>
"""
    return filters.safe(init_django_jcrop_html)

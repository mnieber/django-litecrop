===============
django_litecrop
===============

The django_litecrop module offers non-magical Jcrop based image cropping for Django. It is light-weight in the sense that it does not use Django model fields or Django widgets. It requires that you write your html form code manually (in my opinion, this is the best choice anyway), and makes it easy to drop a Jcrop widget into your form.

Step 0: Add django_litecrop to INSTALLED_APPS
------------------------------------------

.. code:: bash

    pip install django_litecrop

.. code:: python

    INSTALLED_APPS = [
        ...
        django_litecrop
        ...
    ]

Step 1: Add crop_settings to your template context
--------------------------------------------------
- Instead of :code:`crop_settings`, you can choose a different name.
- Note that any values you put into the jcrop field (such as :code:`aspectRatio`) are passed *as is* to Jcrop.

.. code:: python

    context = {
        'crop_settings': {
            'url': 'http://www.vegan101.info/wp1/wp-content/uploads/baby_pig.jpg',
            'klass': 'my_cropped_image_class',
            'output_key': 'cute_pig_123',
            'jcrop': dict(
                aspectRatio=360.0 / 200.0,
                setSelect=[0, 0, 10000, 10000],
            ),
        },
    }
    return render(request, 'example.html', context)

Step 2: Convert crop_settings into an **<img>** element
-------------------------------------------------------
- In your template, use the :code:`django_litecrop_widget` filter to convert :code:`crop_settings` into an :code:`<img>` element that has the :code:`djangoLitecrop` class and various other attributes related to cropping.
- You should include jquery, jcrop and django_litecrop in the :code:`head` section. To activate image cropping, call :code:`$(".djangoLitecrop").djangoLitecrop()` in the :code:`$(document).ready()` handler. In the example below, the :code:`init_django_litecrop` template tag is used as a shortcut to do exactly that.
- The example below adds a css rule for the :code:`my_cropped_image_class` that we supplied in our :code:`crop_settings`.
- It's easy to write your own variation on the :code:`django_litecrop_widget` template tag (just copy-paste-edit).

.. code:: html

    {% load django_litecrop_tags %}
    {% load staticfiles %}

    <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js" type="text/javascript"></script>
    <script src="http://jcrop-cdn.tapmodo.com/v0.9.12/js/jquery.Jcrop.min.js"></script>
    <link rel="stylesheet" href="http://jcrop-cdn.tapmodo.com/v0.9.12/css/jquery.Jcrop.min.css" type="text/css">
    <script src="{% static 'django_litecrop/jquery.django_litecrop.js' %}" type="text/javascript"></script>
    <style media="screen" type="text/css"> .my_cropped_image_class { height: 200px; !important }
    </head>

    <body>
    <form enctype="multipart/form-data" method="post">
    {% csrf_token %}

    <div>{{ crop_settings|django_litecrop_widget }}</div>

    <button id="upload-submit" name="submit" value="upload">Upload</button>
    </form>
    </body>

    {% init_django_litecrop %}

Step 3: Extract the dimensions of the cropped image from the POST data
----------------------------------------------------------------------
- The key ('cute_pig_123') we supplied in :code:`crop_settings` is used to identify the cropping parameters in the POST data.
- Because of the :code:`my_cropped_image_class` css rule, the :code:`display_height` will be different from the :code:`natural_height` in our example.

.. code:: python

    from django.http import JsonResponse

    class ExampleView(View):

        def post(self, request):
            """
            Return something like the following:

            {
                "h": 156.11111111111111,
                "x2": 348,
                "natural_height": 515,
                "w": 281,
                "natural_width": 1440,
                "y": 9,
                "x": 67,
                "display_height": 200,
                "y2": 165.11111111111111,
                "display_width": 559
            }
            """
            return JsonResponse(
                json.loads(request.POST['cute_pig_123'])
            )

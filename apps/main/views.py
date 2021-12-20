from django.shortcuts import render

from apps.main.integrations.unify import UnifyControllerIntegration


def landing(request):
    from apps.main.models import Controller
    controller = Controller.objects.all().last()

    credentials = controller.credentials

    sites = []
    hs = []
    if request.POST:
        site = request.POST.get('site')
        print('site ---- ')
        print(site, flush=True)
        credentials['site'] = site
        controller = UnifyControllerIntegration(**credentials)
        hs = controller.get_hotspotop()
        sites = controller.get_sites()
        # controller.create_hotspotop('probato wifi', '123', 'made with py')
    else:
        controller = UnifyControllerIntegration(**credentials)
        sites = controller.get_sites()

    return render(request, 'landing.html', context={
        'sites': sites,
        'hs': hs
    })


def landing_redirect(request):
    print(request.GET, flush=True)
    return render(request, 'portal.html')


from django.shortcuts import render_to_response, get_object_or_404


def main_page(request):
    # shared_bookmarks = SharedBookmark.objects.order_by('-date')[:10]
    # variables = RequestContext(request, {
    #         'shared_bookmarks': shared_bookmarks
    # })
    return render_to_response('taCore/main.html')



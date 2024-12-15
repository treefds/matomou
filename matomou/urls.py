from django.urls import path

from . import views

app_name = "matomou"
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about_me, name="about"),
    path("create", views.create_entry, name="create"), 
    path("makelist", views.create_video_list, name="create_video_list"),
    path("video/<int:vdid>", views.video_detail, name="video_detail"), 
    path("list/<int:listid>", views.video_list, name="video_list"), 
    path("list/<int:listid>/edit/<int:vdid>", views.edit_list_entry, name="edit_list_entry"),
    path("list/<int:listid>/editlist", views.edit_video_list, name="edit_video_list"),
    path("api/makelist", views.call_create_video_list, name="call_create_video_list"),
    path("api/create", views.call_create_entry, name="call_create"), 
    path("api/list/<int:listid>/add", views.call_add_to_list, name="call_add_to_list"),
    path("api/list/<int:listid>/editlist", views.call_edit_video_list, name="call_edit_video_list"),
    path("api/list/<int:listid>/remove/<int:vdid>", views.call_remove_from_list, name="call_remove_from_list"),
    path("api/list/<int:listid>/edit/<int:vdid>", views.call_edit_list_entry, name="call_edit_list_entry"),


    path("api/bvproxy", views.api_bvid_proxy, name="api_bvproxy")
]
from django.urls import path
from . import views
from django.conf.urls import handler404

handler404 = views.error404
#app_name = 'filme'


urlpatterns = [
    path('', views.film_index, name='film_index'),
    path('film/programm/', views.filmevent_programm_list, name='filmevent_programm_list'),
    path('film/vorschlag/neu/', views.film_neu, name='film_neu'),
    path('film/vorschlag/sichten', views.film_draft_sichten_list, name='film_draft_sichten_list'),
    path('film/vorschlag/vorauswahl', views.film_draft_programmplanung_list, name='film_draft_programmplanung_list'),
    path('film/archiv', views.film_archiv, name='film_archiv'),
    path('film/chronik', views.filmevent_archiv, name='filmevent_archiv'),
    path('a', views.filmevent_openarchiv, name='filmevent_openarchiv'),

    
    path('film/vorschlag/<int:pk>/bewerten', views.film_draft_bewertung, name='film_draft_bewertung'),
    path('film/vorschlag/<int:pk>/delete/', views.film_remove, name='film_remove'),
    path('film/vorschlag/<int:pk>/status/<key>/', views.film_status, name='film_status'),

    path('film/spielplanung', views.film_spielplanung_list, name='film_spielplanung_list'),
    path('film/spielplanung/<int:kat>', views.film_spielplanung_list, name='film_spielplanung_list'),
    path('film/veranstaltung/neu/', views.event_new, name='event_new'),
    path('film/spielplan', views.film_spielplan_list, name='film_spielplan_list'),
    path('film/<int:pk>/', views.film_detail, name='film_detail'),
    path('film/<int:pk>/bearbeiten/', views.film_detail_edit, name='film_detail_edit'),
    path('film/event/<int:pk>/confirm/', views.confirm_eventfilm, name='confirm_eventfilm'),
    path('film/event/<int:pk>/detail/', views.filmevent_detail, name='filmevent_detail'),

    path('newsletter/newsletter_for_today/', views.newsletter_render_today, name='newsletter_render_today'),
    path('newsletter/newsletter_hinweis/', views.newsletter_render_hinweis, name='newsletter_render_hinweis'),
    path('newsletter/sondernewsletter/liste', views.sondernewsletter_list, name='sondernewsletter_list'),
    path('newsletter/sondernewsletter/neu', views.sondernewsletter_neu, name='sondernewsletter_neu'),
    path('newsletter/sondernewsletter/del/<int:pk>', views.sondernewsletter_delete, name='sondernewsletter_delete'),

    path('newsletter/sondernewsletter/edit/<int:pk>', views.sondernewsletter_edit, name='sondernewsletter_edit'),
    path('newsletter/sondernewsletter/render/<int:pk>', views.sondernewsletter_render, name='sondernewsletter_render'),




    path('newsletter/sende/<typ>/<key>', views.newsletter_send, name='newsletter_send'),
    path('newsletter/sende/sondernews/<int:pk>/<email>', views.sondernews_send, name='sondernews_send'),


    path('filmevent/newsletter/feedback/<flag>', views.newsletter_abo_feedback, name='newsletter_abo_feedback'),
    path('newsletter/opt_in/<email>/<salz>', views.newsletters_opt_in, name='newsletters_opt_in'),
    # newsletter/abmelden/ wird in newsletter_render hartcodet verwendet!
    path('newsletter/abmelden/<email>/<salz>', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),

    path('import/drupal', views.import_drupal, name='import_drupal'),

    
    path('film/event/<int:pk>/bearbeiten/', views.filmevent_detail_edit, name='filmevent_detail_edit'),
    path('film/event/<int:pk>/dienste/bearbeiten/', views.filmevent_dienste, name='filmevent_dienste'),

    path('film/impressum/', views.film_impressum, name='film_impressum'),
    path('film/datenschutzhinweis/', views.film_datenschutzhinweis, name='film_datenschutzhinweis'),
    path('film/ueber_uns/', views.film_ueber_uns, name='film_ueber_uns'),
    path('film/anfahrt/', views.film_anfahrt, name='film_anfahrt'),



    
    


 

   

 


    # path('film/<int:pk>/comment/', views.add_comment_to_film, name='add_comment_to_film'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),






]
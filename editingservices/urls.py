from django.urls import path

from .import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('article', views.ArticleView.as_view(), name='article'),
    path('article-sort-catagory/<cat>', views.ArticleView.as_view(), name='article_sort'),
    path('article-sort-by-char/<charsort>', views.ArticleView.as_view(), name='article_sort_char'),
    path('article-procesing-stage/', views.ArticleprocesingstageView.as_view(), name='article_procesing_stage'),
    path('article-mid-stage/', views.ArticlesentauthorView.as_view(), name='article_sent_author'),
    path('article-final-stage/', views.ArticlefinalstageView.as_view(), name='final_stage'),

    path('partner', views.PartnerView.as_view(), name='partner'),
    path('editor', views.EditorView.as_view(), name='editor'),

    path('root-admin/', views.root_admin, name='root_admin'),
    path('logout-site/', views.logout_view, name='logout_view'),
    path('create-article/', views.create_article, name='create_article'),
    path('article/<slug:slug>', views.article_detail, name='article_detail'),
    path('edit-article/<slug:slug>', views.article_edit_full, name='article_edit_full'),
    path('edit-article-title-or-catatgory/<slug:slug>', views.article_edit, name='article_edit'),
    path('delete-article/<slug:slug>', views.article_delete, name='article_delete'),
    path('edit-subject-word/<slug:slug>', views.subject_word_edit, name='subject_word_edit'),
    path('edit-stage/<slug:slug>', views.stage_add, name='stage_add'),
    path('edit-delivery-and-payment-date/<slug:slug>', views.payment_delivery_add, name='payment_delivery_add'),

    path('add-author/<slug:slug>', views.author_add, name='author_add'),
    path('edit-author/<slug:slug>/<int:pk>', views.author_edit, name='author_edit'),
    path('delete-author/<slug:slug>/<int:pk>', views.author_delete, name='author_delete'),
    
    path('add-target-journal/<slug:slug>', views.target_journal_add, name='target_journal_add'),
    path('edit-target-journal/<slug:slug>/<int:pk>', views.target_journal_edit, name='target_journal_edit'),
    path('delete-target-journal/<slug:slug>/<int:pk>', views.target_journal_delete, name='target_journal_delete'),

    path('add-service/<slug:slug>', views.service_add, name='service_add'),
    path('edit-service/<slug:slug>/<int:pk>', views.service_edit, name='service_edit'),
    path('delete-service/<slug:slug>/<int:pk>', views.service_delete, name='service_delete'),

    path('add-partner/<slug:slug>', views.partner_add, name='partner_add'),
    path('edit-partner/<slug:slug>/<int:pk>', views.partner_article_edit, name='partner_article_edit'),
    path('delete-partner/<slug:slug>/<int:pk>', views.partner_article_delete, name='partner_article_delete'),

    path('add-article-editor/<slug:slug>', views.editor_add, name='editor_add'),
    path('edit-article-editor/<slug:slug>/<int:pk>', views.editor_edit, name='editor_edit'),
    path('delete-article-editor/<slug:slug>/<int:pk>', views.editor_delete, name='editor_delete'),

    
    


    path('create-partner/', views.create_partner, name='create_partner'),
    path('edit-partner/<int:id>', views.edit_partner, name='edit_partner'),
    path('delete-partner/<int:id>', views.delete_partner, name='delete_partner'),
    path('partner-list/', views.partner_list, name='partner_list'),
    path('create-editor/', views.create_editor, name='create_editor'),
    path('edit-editor/<int:id>', views.edit_editor, name='edit_editor'),
    path('delete-editor/<int:id>', views.delete_editor, name='delete_editor'),
    path('editor-list/', views.editor_list, name='editor_list'),
   
    path('article-pdf/<slug:slug>', views.GeneratePDF.as_view(), name='article_pdf'),
    path('pdf-edit/<slug:slug>', views.article_pdf_editing, name='article_pdf_editing'),
    
    
]
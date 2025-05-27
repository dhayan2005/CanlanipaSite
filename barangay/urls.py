from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserComplaintList, ComplaintDetail, UpdateComplaintStatusView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('complaint/', views.complaint_view, name='complaint'),
    path('complaint/review/', views.complaint_review, name='complaint_review'),
    path('complaint/edit/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('api/my-complaints/', UserComplaintList.as_view(), name='api-my-complaints'),
    path('api/complaint/<int:pk>/update-status/', UpdateComplaintStatusView.as_view(), name='update-complaint-status'),
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
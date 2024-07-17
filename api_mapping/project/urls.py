from django.urls import path
from . import views
from .views import project_page
from .views import add_mapping
from .views import  add_mapping,select_api
from django.contrib.auth import views as auth_views
from .views import select_version
from .views import CreateProjectView
from .views import RemoveMappingView,AddMappingAPI,UpdateNodeAPI,SelectApiView,SelectVersionView,changeFlownum,changeProjectdetails
urlpatterns = [
    path('', views.home, name='home'),
    path('project/', views.project, name='project'),
    path('mapping/', views.mapping, name='mapping'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', project_page, name='project_page'),
    path('add_mapping/<int:project_id>/', add_mapping, name='add_mapping'),
    # path('project/<int:project_id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/select_api/<str:api>/', select_api, name='select_api'),
   
    path('project/<int:project_id>/select_version/<str:ver>/',select_version,name='select_version'),
    path('get_subtypes/<int:type_id>/', views.get_subtypes, name='get_subtypes'),
    path('get_subadd/<str:type_id>/', views.get_subadd, name='get_subadd'),
    path('api/create_project/', CreateProjectView.as_view(), name='create_project'),

    path('api/get_source_types/', views.get_source_types, name='get_source_types'),
    path('api/get_destination_types/', views.get_destination_types, name='get_destination_types'),
   
    
    path('admins/', views.admin_page, name='admin_page'),
    
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('remove_mapping/<int:project_id>/', views.remove_mapping, name='remove_mapping'),
    # path('get_subtypes/', views.get_subtypes, name='get_subtypes'),
    path('project/<int:project_id>/update_node/', views.update_node, name='update_node'),

    path('api/get_subtypes/<int:type_id>/', views.get_subtypes, name='get_subtypes'),
    path('api/get_subtypes_1/<str:id>/', views.get_subtypes_1, name='get_subtypes_1'),
    path('api/get_projects/', views.get_projects, name='get_projects'),
    path('api/project_data/<int:project_id>/', views.project_data, name='project_data'),
    path('api/remove_mapping/<int:project_id>/', RemoveMappingView.as_view(), name='remove_mapping_api'),
    path('api/add_mapping/<int:project_id>/', AddMappingAPI.as_view(), name='add_mapping_api'),
    path('api/update_node/<int:project_id>/', UpdateNodeAPI.as_view(), name='update_node_api'),
    path('api/select_api/<int:project_id>/<str:api>/', SelectApiView.as_view(), name='select_api_api'),
    path('api/select_version/<int:project_id>/<str:ver>/', SelectVersionView.as_view(), name='select_version_api'),
    path('api/add_mapping_excel/<int:project_id>/', views.add_mapping_excel, name='add_mapping_excel'),
    path('api/flow_num_change/<int:project_id>/', changeFlownum.as_view(), name='flow_num_change'),
    path('api/change_details/<int:project_id>/',changeProjectdetails.as_view(),name='change_details'),
    
    
]
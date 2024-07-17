# project_manager/views.py

from django.shortcuts import render
from .models import Project_team
from django.contrib import messages
def home(request):
    return render(request, 'home.html')

def project(request):
    projects = Project_team.objects.all()
    return render(request, 'project.html', {'projects': projects})

def mapping(request):
    projects = Project_team.objects.all()
    return render(request, 'mapping.html', {'projects': projects})
from django.shortcuts import render, redirect
from .forms import ProjectForm



def admin_page(request):
    projects = Project_team.objects.all()
    return render(request, 'admins.html', {'projects': projects})

def delete_project(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    project.delete()
    return redirect('admin_page')



def ver_naming(version_name):
    version_name=version_name.split('_')
    no=int(version_name[1])+1
    return "v_"+str(no)
# views.py

from django.shortcuts import render, get_object_or_404
from .models import Project_team



import pandas as pd  # Import pandas for handling Excel files
from io import TextIOWrapper  # Import TextIOWrapper for reading Excel file from request

from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project_team
from django.utils.datastructures import MultiValueDictKeyError



from django.shortcuts import render, get_object_or_404, redirect
from .models import Project_team, Type_color,Master






def update_node(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    types = Type_color.objects.all()
    subtypes = Subtype.objects.all()

    if request.method == 'POST':
        node_name = request.POST['node_name']
        new_node_name = request.POST['new_node_name']
        type_id = request.POST['type_up']
        subtype_id = request.POST['subtype_up']
        subtype_name=subtype_id
        
        subtype_id=Subtype.objects.get(subtype=subtype_id,type_id=Type_color.objects.get(type=type_id).id)
        print(subtype_id,type(subtype_id))
        subtype_id=subtype_id.id
        # type_obj = get_object_or_404(Type_color, pk=type_id)
        subtype_obj = get_object_or_404(Subtype, pk=subtype_id)

        # Update node name in the project's mapping
        updated_mapping = project.mapping.replace(node_name, f'{new_node_name}::{subtype_obj.subtype}')
        project.mapping = updated_mapping
        project.save()

        #version naming
        from datetime import datetime
        current_time=datetime.now()
        format_date=current_time.strftime("%Y-%m-%d %H:%M:%S")
        vn=version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
        vn=ver_naming(vn)


        version.objects.create(
            project_team=project,
            version_name=vn,
            version_timestamp=format_date,
            mapping=project.mapping
        )
        #####

        node_name=node_name.split('::')
        node_name=node_name[0]

        Master.objects.filter(source=node_name, project_team=project).update(
            source=new_node_name,
            source_type=type_id,
            source_subtype=subtype_obj.subtype
        )
        Master.objects.filter(destination=node_name, project_team=project).update(
            destination=new_node_name,
            destination_type=type_id,
            destination_subtype=subtype_obj.subtype
        )
        # Redirect or render response
        return redirect('project_page', project_id=project_id)

    return render(request, 'update_node.html', {
        'project': project,
        'types': types,
        'subtypes': subtypes,
    })
from .models import version



def add_mapping(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    if request.method == 'POST':
        api = request.POST.get('api')
        mapping = request.POST.get('mapping')
        source_type = request.POST.get('source_type')
        source_subtype = request.POST.get('source_subtype')#
        destination_type = request.POST.get('destination_type')
        destination_subtype = request.POST.get('destination_subtype')
        two_way = request.POST.get('two_way', False)
        flow_num=request.POST.get('flow_num')
        if two_way=='on':
            two_way='Yes'
        # print(type(two_way),two_way)
        if api and mapping and source_type and destination_type:
            try:
                source_color = Type_color.objects.get(type=source_type).color
                destination_color = Type_color.objects.get(type=destination_type).color
            except Type_color.DoesNotExist as e:
                error_message = f"Type_color matching query does not exist: {str(e)}"
                source_types = Type_color.objects.values_list('type', flat=True)
                destination_types = Type_color.objects.values_list('type', flat=True)
                return render(request, 'project_page_template.html', {'project': project, 'error_message': error_message, 'source_types': source_types, 'destination_types': destination_types})
            print(source_subtype,type(source_subtype))
            if source_subtype=='NA':
                API=api
                print("excuted, if")
            else:
                API=api+"::"+source_subtype
                print("excuted, elsef")
            if destination_subtype=='NA':
                MAP=mapping
            else:
                MAP=mapping+"::"+destination_subtype
            
            if flow_num=='None':
                if two_way:
                    mapping_data = f"\n    {API}<-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    mapping_data = f"\n    {API}-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
            else:
                if two_way:
                    mapping_data = f"\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    mapping_data = f"\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
            project.mapping += mapping_data
            project.save()

            #version naming
            from datetime import datetime
            current_time=datetime.now()
            format_date=current_time.strftime("%Y-%m-%d %H:%M:%S")
            vn=version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
            vn=ver_naming(vn)


            version.objects.create(
                project_team=project,
                version_name=vn,
                version_timestamp=format_date,
                mapping=project.mapping
            )
            #####
            #save to master table
            Master.objects.create(
                source=api,
                source_type=source_type,
                source_subtype=source_subtype,
                destination=mapping,
                destination_type=destination_type,
                destination_subtype=destination_subtype,
                project_team=project,
                flow_num=flow_num,
                two_way=two_way,
            )
            return redirect('project_page', project_id=project_id)
    
    source_types = Type_color.objects.values_list('type', flat=True)
    destination_types = Type_color.objects.values_list('type', flat=True)
    return render(request, 'project_page_template.html', {'project': project, 'source_types': source_types, 'destination_types': destination_types})




from django.shortcuts import render, get_object_or_404, redirect
from .models import Project_team
import pandas as pd
from io import TextIOWrapper
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project_team
from django.shortcuts import render, get_object_or_404
from .models import Project_team,Type_color
def create_map(project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    data=Master.objects.filter(project_team_id=project_id)
    
    filtered_mappings="graph TD;\n"
    node_styles=''
    
    for i in (data):
        if i.source_subtype=='NA':
            API=i.source
        else:
            API=i.source+'::'+i.source_subtype
        if i.destination_subtype=='NA':
            MAP=i.destination
        else:
            MAP=i.destination+'::'+i.destination_subtype
        if i.flow_num=='None':
            if i.two_way=='Yes':

                filtered_mappings += f"    {API}<-->{MAP};\n"
            else:
                filtered_mappings += f"    {API}-->{MAP};\n"
        else:
            if i.two_way=='Yes':
                #GSLB_PORT_306266::GSLB_MU<-->|1|Kubernetes_cluster::K8S
                filtered_mappings += f"    {API}<-->|{i.flow_num}|{MAP};\n"
            else:
                filtered_mappings += f"    {API}-->|{i.flow_num}|{MAP};\n"
        source_color=Type_color.objects.get(type=i.source_type).color
        destination_color= Type_color.objects.get(type=i.destination_type).color
        node_styles += f"    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n"
        node_styles += f"    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

            

 
    filtered_mappings += "\n%% Node styles\n" + node_styles
    return filtered_mappings

def project_page(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    data=Master.objects.filter(project_team_id=project_id)
    apis = set()
    filtered_mappings="graph TD;\n"
    node_styles=''
    
    for i in (data):
        if i.source_subtype=='NA':
            API=i.source
        else:
            API=i.source+'::'+i.source_subtype
        if i.destination_subtype=='NA':
            MAP=i.destination
        else:
            MAP=i.destination+'::'+i.destination_subtype
            
        if i.two_way=='Yes':
            #GSLB_PORT_306266::GSLB_MU<-->|1|Kubernetes_cluster::K8S
            filtered_mappings += f"    {API}<-->|{i.flow_num}|{MAP};\n"
        else:
            filtered_mappings += f"    {API}-->|{i.flow_num}|{MAP};\n"
        source_color=Type_color.objects.get(type=i.source_type).color
        destination_color= Type_color.objects.get(type=i.destination_type).color
        node_styles += f"    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n"
        node_styles += f"    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

            

 
    filtered_mappings += "\n%% Node styles\n" + node_styles
    # print(filtered_mappings)
    for i in (data):
        apis.add(i.source)
        apis.add(i.destination)
 
    source_types = Type_color.objects.values_list('type', flat=True)
    destination_types = Type_color.objects.values_list('type', flat=True)
    types = Type_color.objects.all()
    send_mapping=filtered_mappings
    print(send_mapping)


    from .models import version
    vl=version.objects.filter(project_team=project).values_list('version_name',flat=True).distinct()
    vl=list(vl)

    return render(request, 'project_page_template.html', {
        'project': project, # {{ project.mapping|safe }}
        'apis': sorted(apis),
        'source_types': source_types,
        'destination_types': destination_types,
        'type_list': types,
        'send_mapping':send_mapping,
        'versions':vl,

    })
  


def select_version(request,project_id,ver):
    project = get_object_or_404(Project_team, pk=project_id)
    from .models import version
    version_mapping = version.objects.filter(project_team=project).get(version_name=ver).mapping
    version_time=version.objects.filter(project_team=project).get(version_name=ver).version_timestamp



    data=Master.objects.filter(project_team_id=project_id)
    apis = set()
    filtered_mappings="graph TD;\n"
    node_styles=''
    
    for i in (data):
        if i.source_subtype=='NA':
            API=i.source
        else:
            API=i.source+'::'+i.source_subtype
        if i.destination_subtype=='NA':
            MAP=i.destination
        else:
            MAP=i.destination+'::'+i.destination_subtype
            
        if i.two_way=='Yes':
            #GSLB_PORT_306266::GSLB_MU<-->|1|Kubernetes_cluster::K8S
            filtered_mappings += f"    {API}<-->|{i.flow_num}|{MAP};\n"
        else:
            filtered_mappings += f"    {API}-->|{i.flow_num}|{MAP};\n"
        source_color=Type_color.objects.get(type=i.source_type).color
        destination_color= Type_color.objects.get(type=i.destination_type).color
        node_styles += f"    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n"
        node_styles += f"    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

            

 
    filtered_mappings += "\n%% Node styles\n" + node_styles
    # print(filtered_mappings)
    for i in (data):
        apis.add(i.source)
        apis.add(i.destination)
 
    source_types = Type_color.objects.values_list('type', flat=True)
    destination_types = Type_color.objects.values_list('type', flat=True)
    types = Type_color.objects.all()
    send_mapping=filtered_mappings
    print(send_mapping)


    from .models import version
    vl=version.objects.filter(project_team=project).values_list('version_name',flat=True).distinct()
    vl=list(vl)

    return render(request, 'project_page_template.html', {
        'project': project,
        'apis': sorted(apis),
        # 'selected_api': api,
        'filtered_mappings': filtered_mappings.strip(),
        'send_mapping':send_mapping,
        'version_mapping':version_mapping,
        'version_time':version_time,
        'ver':ver,
        'versions':vl,
    })

from django.shortcuts import render, get_object_or_404
from .models import Project_team, Type_color,Master,Subtype

def select_api(request,project_id,api):
    project = get_object_or_404(Project_team, pk=project_id)
    data=Master.objects.filter(project_team_id=project_id)
    filtered_mappings = ""
    apis=set()
    node_styles = ""

    for i in (data):
        if api in i.source or api in i.destination:
            if i.two_way=='Yes':
                #GSLB_PORT_306266::GSLB_MU<-->|1|Kubernetes_cluster::K8S
                filtered_mappings += f"    {i.source}::{i.source_subtype}<-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
            else:
                filtered_mappings += f"    {i.source}::{i.source_subtype}-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
            source_color=Type_color.objects.get(type=i.source_type).color
            destination_color= Type_color.objects.get(type=i.destination_type).color
            node_styles += f"    style {i.source}::{i.source_subtype} fill:{source_color},stroke:#333,stroke-width:2px;\n"
            node_styles += f"    style {i.destination}::{i.destination_subtype} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

            apis.add(i.source)
            apis.add(i.destination)

 
    filtered_mappings += "\n%% Node styles\n" + node_styles

    data=Master.objects.filter(project_team_id=project_id)
    
    filtered_mappings_1="graph TD;\n"
    node_styles=''
    for i in (data):
        
        if i.two_way=='Yes':
            #GSLB_PORT_306266::GSLB_MU<-->|1|Kubernetes_cluster::K8S
            filtered_mappings_1 += f"    {i.source}::{i.source_subtype}<-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
        else:
            filtered_mappings_1 += f"    {i.source}::{i.source_subtype}-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
        source_color=Type_color.objects.get(type=i.source_type).color
        destination_color= Type_color.objects.get(type=i.destination_type).color
        node_styles += f"    style {i.source}::{i.source_subtype} fill:{source_color},stroke:#333,stroke-width:2px;\n"
        node_styles += f"    style {i.destination}::{i.destination_subtype} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

            

 
    filtered_mappings_1 += "\n%% Node styles\n" + node_styles
    send_mapping=filtered_mappings_1
    print(filtered_mappings)
    print("APIS:  ",apis)
    vl=version.objects.filter(project_team=project).values_list('version_name',flat=True).distinct()
    vl=list(vl)
    return render(request, 'project_page_template.html', {
        'project': project,
        'apis': sorted(apis),
        'selected_api': api,
        'filtered_mappings': filtered_mappings.strip(),
        'send_mapping':send_mapping,
        'versions':vl,
    })

            

from django.shortcuts import render, redirect
from .forms import ProjectForm
from .models import Project_team, Type_color,Master
import pandas as pd

from django.http import JsonResponse
from .models import Subtype

def get_subtypes(request, type_id):
    subtypes = Subtype.objects.filter(type_id=type_id).values('id', 'subtype')
    return JsonResponse({'subtypes': list(subtypes)})

def get_subadd(request,type_id):
    type_instance = Type_color.objects.get(type=type_id)
    subtypes = Subtype.objects.filter(type=type_instance).values('id', 'subtype')
    return JsonResponse({'subtypes': list(subtypes)})

from .models import version
def create_project(request):
    types = Type_color.objects.all()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            mapping_type = form.cleaned_data['mapping_type']
            
            if mapping_type == 'single_input':
                try:
                    api = form.cleaned_data['api']
                    mapping = form.cleaned_data['mapping']
                    source_type = form.cleaned_data['source_type']
                    source_subtype = form.cleaned_data['source_subtype']
                    destination_type = form.cleaned_data['destination_type']
                    destination_subtype = form.cleaned_data['destination_subtype']
                    two_way = request.POST.get('two_way', False)
                    flow_num=form.cleaned_data['flow_num']
                    print(flow_num)
                    print("Source Type:", source_type.type, "Destination Type:", destination_type.type)  # Debugging
                    # print("type:",type(source_type.type))
                    print(source_subtype.subtype,destination_subtype.subtype)
                
                    source_color = Type_color.objects.get(type=source_type.type).color
                    destination_color = Type_color.objects.get(type=destination_type.type).color
                except Exception as e:
                    error_message = f"Type_color matching query does not exist: {str(e)}"
                    messages.error(request, f"Project not created. Please enter valid details.\n {str(e)}")
                    return render(request, 'Create_Project.html', {'form': form, 'error_message': error_message})
                
                API=api+"::"+source_subtype.subtype
                MAP=mapping+"::"+destination_subtype.subtype
                if flow_num=='None':
                    if two_way:
                        mapping_data = f"graph TD;\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                        # print(mapping_data)
                    else:
                        mapping_data = f"graph TD;\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    if two_way:
                        mapping_data = f"graph TD;\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                        # print(mapping_data)
                    else:
                        mapping_data = f"graph TD;\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                # if two_way:
                #     mapping_data += f"\n    {MAP}-->{API};"

                project=Project_team.objects.create(
                    project_name=form.cleaned_data['project_name'],
                    project_manager=form.cleaned_data['project_manager'],
                    mapping=mapping_data
                )
                from datetime import datetime
                current_time=datetime.now()
                format_date=current_time.strftime("%Y-%m-%d %H:%M:%S")
                version.objects.create(
                    project_team=project,
                    version_name='v_1',
                    version_timestamp=format_date,
                    mapping=mapping_data
                )
                if two_way=='on':
                    two_way='Yes'
                # Save to Master table
                Master.objects.create(
                    source=api,
                    source_type=source_type.type,
                    source_subtype=source_subtype.subtype,
                    destination=mapping,
                    destination_type=destination_type.type,
                    destination_subtype=destination_subtype.subtype,
                    flow_num=flow_num,
                    two_way=two_way,
                    project_team=project
                )
            elif mapping_type == 'excel_file':
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file, engine='openpyxl')
                data=[]
                mapping_data = "graph TD;\n"
                for index, row in df.iterrows():
                    try:
                        Source=row['Source']
                        Destination=row['Destination']
                        Source_type=row['Source_type']
                        Destination_type=row['Destination_type']
                        Source_subtype=row['Source_subtype']
                        Destination_subtype=row['Destination_subtype']
                        two_way=row['two_way']
                        flow_num=row['Flow_num']

                        print(Source,Source_type,Source_subtype,Destination,Destination_type,Destination_subtype,flow_num)
                        data.append({'two_way':two_way,'source':Source,'source_type':Source_type,'source_subtype':Source_subtype,'destination':Destination,'destination_type':Destination_type,'destination_subtype':Destination_subtype,'flow_num':flow_num,})
                        source_color = Type_color.objects.get(type=row['Source_type']).color
                        destination_color = Type_color.objects.get(type=row['Destination_type']).color
                    except Type_color.DoesNotExist as e:
                        error_message = f"Type_color matching query does not exist: {str(e)}"
                        messages.error(request, "Project not created. Please enter valid details.")
                        return render(request, 'Create_Project.html', {'form': form, 'error_message': error_message})

                    
                    API=row['Source']+"::"+row['Source_subtype']
                    MAP=row['Destination']+"::"+row['Destination_subtype']
                     
                    
                    # mapping_data += f"    {row['Source']}-->{row['Destination']};\n\n    %% Node styles\n    style {row['Source']} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {row['Destination']} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
                    if two_way=="Yes":
                        mapping_data += f"    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
                    else:
                        mapping_data += f"    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

                project=Project_team.objects.create(
                    project_name=form.cleaned_data['project_name'],
                    project_manager=form.cleaned_data['project_manager'],
                    mapping=mapping_data
                )  
                from datetime import datetime
                current_time=datetime.now()
                format_date=current_time.strftime("%Y-%m-%d %H:%M:%S")
                version.objects.create(
                    project_team=project,
                    version_name='v_1',
                    version_timestamp=format_date,
                    mapping=mapping_data
                )
                for item in data:
                    item['project_team']=project
                    Master.objects.create(**item)
                
                
                
            return redirect('project')
        else:
            messages.error(request, "Project not created. Please enter valid details.")
            print(form.errors)  # Print form errors for debugging  # Print form errors for debugging
    else:
        form = ProjectForm()
        types = Type_color.objects.all()
        
    return render(request, 'Create_Project.html', {'form': form,'type_list': types,})#'type_list': types,





def remove_mapping(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    if request.method == 'POST':
        source = request.POST.get('source')
        to_be_deleted=source
       
        Master.objects.filter(
            destination=to_be_deleted,
            # source_subtype=source_subtype,
            # destination=destination,
            # destination_subtype=destination_subtype,
            project_team=project
        ).delete()
        Master.objects.filter(
            source=to_be_deleted,
            # source_subtype=source_subtype,
            # destination=destination,
            # destination_subtype=destination_subtype,
            project_team=project
        ).delete()
        vm=create_map(project_id)
        #version naming
        from datetime import datetime
        current_time=datetime.now()
        format_date=current_time.strftime("%Y-%m-%d %H:%M:%S")
        vn=version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
        vn=ver_naming(vn)


        version.objects.create(
            project_team=project,
            version_name=vn,
            version_timestamp=format_date,
            mapping=vm
        )
            #####

        return redirect('project_page', project_id=project_id)
    
    source_types = Type_color.objects.values_list('type', flat=True)
    destination_types = Type_color.objects.values_list('type', flat=True)
    return render(request, 'project_page_template.html', {'project': project, 'source_types': source_types, 'destination_types': destination_types})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Project_team, Master, Type_color, Subtype
# from .forms import UpdateNodeForm








#############
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Type_color, Project_team, Master
from .serializers import ProjectSerializer
from .forms import ProjectForm

class CreateProjectView(APIView):   

    def post(self, request, format=None):
        form = ProjectForm(request.data, request.FILES)
        if form.is_valid():
            mapping_type = form.cleaned_data['mapping_type']
            
            if mapping_type == 'single_input':
                try:
                    api = form.cleaned_data['api']
                    api=api.replace(" ","_")
                    mapping = form.cleaned_data['mapping']
                    mapping=mapping.replace(" ","_")
                    source_type = form.cleaned_data['source_type']
                    source_subtype = form.cleaned_data['source_subtype']
                    destination_type = form.cleaned_data['destination_type']
                    destination_subtype = form.cleaned_data['destination_subtype']
                    two_way = request.data.get('two_way', False)
                    flow_num = form.cleaned_data['flow_num']

                    source_color = Type_color.objects.get(type=source_type.type).color
                    destination_color = Type_color.objects.get(type=destination_type.type).color
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

                API = f"{api}::{source_subtype.subtype}"
                MAP = f"{mapping}::{destination_subtype.subtype}"
                print(flow_num,"flow num")
                if flow_num=='None':
                    if two_way:
                        mapping_data = f"graph TD;\n    {API}<-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                    else:
                        mapping_data = f"graph TD;\n    {API}-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    if two_way:
                        mapping_data = f"graph TD;\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                    else:
                        mapping_data = f"graph TD;\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"

                project = Project_team.objects.create(
                    project_name=form.cleaned_data['project_name'],
                    project_manager=form.cleaned_data['project_manager'],
                    mapping=mapping_data
                )

                from datetime import datetime
                current_time = datetime.now()
                format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

                version.objects.create(
                    project_team=project,
                    version_name='v_1',
                    version_timestamp=format_date,
                    mapping=mapping_data
                )

                Master.objects.create(
                    source=api,
                    source_type=source_type.type,
                    source_subtype=source_subtype.subtype,
                    destination=mapping,
                    destination_type=destination_type.type,
                    destination_subtype=destination_subtype.subtype,
                    flow_num=flow_num,
                    two_way=two_way,#'Yes' if two_way == 'on' else 'No',
                    project_team=project
                )
            elif mapping_type == 'excel_file':
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file, engine='openpyxl')
                data = []
                mapping_data = "graph TD;\n"
                for index, row in df.iterrows():
                    try:
                        source_color = Type_color.objects.get(type=row['Source_type']).color
                        destination_color = Type_color.objects.get(type=row['Destination_type']).color
                    except Type_color.DoesNotExist as e:
                        return Response({'error': f"Type_color matching query does not exist: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
                    api=row['Source'].replace(" ","_")
                    map=row['Destination'].replace(" ","_")
                    API = f"{api}::{row['Source_subtype']}"
                    MAP = f"{map}::{row['Destination_subtype']}"
                    flow_num = str(row['Flow_num'])
                    if flow_num=='nan':
                        flow_num='None'
                    if flow_num=='None':
                        if row['two_way'] == "Yes":
                            mapping_data += f"    {API}<-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
                        else:
                            mapping_data += f"    {API}-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
                    else:

                        if row['two_way'] == "Yes":
                            mapping_data += f"    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
                        else:
                            mapping_data += f"    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

                    data.append({
                        'two_way': row['two_way'],
                        'source': api,
                        'source_type': row['Source_type'],
                        'source_subtype': row['Source_subtype'],
                        'destination': map,
                        'destination_type': row['Destination_type'],
                        'destination_subtype': row['Destination_subtype'],
                        'flow_num': flow_num,
                    })

                project = Project_team.objects.create(
                    project_name=form.cleaned_data['project_name'],
                    project_manager=form.cleaned_data['project_manager'],
                    mapping=mapping_data
                )

                from datetime import datetime
                current_time = datetime.now()
                format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")

                version.objects.create(
                    project_team=project,
                    version_name='v_1',
                    version_timestamp=format_date,
                    mapping=mapping_data
                )

                for item in data:
                    item['project_team'] = project
                    Master.objects.create(**item)

            return Response({'message': 'Project created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        projects = Project_team.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

# In urls.py, add the endpoint for the API view



from django.http import JsonResponse
from .models import Type_color,Subtype

def get_source_types(request):
    source_types = list(Type_color.objects.values('id', 'type'))
    return JsonResponse({'source_types': source_types})

def get_destination_types(request):
    destination_types = list(Type_color.objects.values('id', 'type'))
    return JsonResponse({'destination_types': destination_types})
def get_subtypes(request, type_id):
    subtypes = list(Subtype.objects.filter(type_id=type_id).values('id', 'subtype'))
    return JsonResponse({'subtypes': subtypes})
def get_subtypes_1(request,id):
    id_no=Type_color.objects.filter(type=id).values('id')
    print(id)
    print(id_no[0]['id'])
    subtypes = list(Subtype.objects.filter(type_id=id_no[0]['id']).values('id', 'subtype'))
    return JsonResponse({'subtypes': subtypes})

from django.http import JsonResponse
from .models import Project_team

def get_projects(request):
    projects = Project_team.objects.all().values('id', 'project_name', 'project_manager')
    return JsonResponse(list(projects), safe=False)










from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProjectSerializer, MasterSerializer, TypeColorSerializer, VersionSerializer

@api_view(['GET'])
def project_data(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)
    data = Master.objects.filter(project_team_id=project_id)
    
    apis = set()
    filtered_mappings = "graph TD;\n"
    node_styles = ''
    
    for i in data:
        if i.source_subtype == 'NA':
            API = i.source
        else:
            API = i.source + '::' + i.source_subtype
        if i.destination_subtype == 'NA':
            MAP = i.destination
        else:
            MAP = i.destination + '::' + i.destination_subtype
        print(i.two_way)
        if i.flow_num=='None':
            if i.two_way=='Yes' or i.two_way=='True':
                filtered_mappings += f"    {API}<-->{MAP};\n"
            else:
                filtered_mappings += f"    {API}-->{MAP};\n";
        else:
            if i.two_way=='Yes' or i.two_way=='True':
                filtered_mappings += f"    {API}<-->|{i.flow_num}|{MAP};\n"
            else:
                filtered_mappings += f"    {API}-->|{i.flow_num}|{MAP};\n"
        
        source_color = Type_color.objects.get(type=i.source_type).color
        destination_color = Type_color.objects.get(type=i.destination_type).color
        node_styles += f"    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n"
        node_styles += f"    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"
    
    filtered_mappings += "\n%% Node styles\n" + node_styles
    
    for i in data:
        apis.add(i.source)
        apis.add(i.destination)
    
    source_types = Type_color.objects.values_list('type', flat=True)
    destination_types = Type_color.objects.values_list('type', flat=True)
    types = Type_color.objects.all()
    send_mapping = filtered_mappings

    vl = version.objects.filter(project_team=project).values_list('version_name', flat=True).distinct()
    vl = list(vl)
    
    response_data = {
        'project': ProjectSerializer(project).data,
        'apis': sorted(apis),
        'source_types': list(source_types),
        'destination_types': list(destination_types),
        'type_list': TypeColorSerializer(types, many=True).data,
        'send_mapping': send_mapping,
        'versions': vl,
    }
    
    return Response(response_data)



from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from .models import Project_team, Master, Type_color, version
from .serializers import RemoveMappingSerializer
# from .utils import create_map, ver_naming  # Import your utility functions

class RemoveMappingView(APIView):
    def post(self, request, project_id):
        project = get_object_or_404(Project_team, pk=project_id)
        serializer = RemoveMappingSerializer(data=request.data)
        
        if serializer.is_valid():
            source = serializer.validated_data['source']
            to_be_deleted = source
            
            Master.objects.filter(
                destination=to_be_deleted,
                project_team=project
            ).delete()
            Master.objects.filter(
                source=to_be_deleted,
                project_team=project
            ).delete()
            
            vm = create_map(project_id)
            
            current_time = datetime.now()
            format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
            vn = version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
            vn = ver_naming(vn)

            version.objects.create(
                project_team=project,
                version_name=vn,
                version_timestamp=format_date,
                mapping=vm
            )

            return Response({"message": "Mapping removed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#add mapping
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project_team, Type_color, version, Master
# from .utils import create_map, ver_naming
from datetime import datetime

class AddMappingAPI(APIView):
    global two_way
    def post(self, request, project_id):
        project = get_object_or_404(Project_team, pk=project_id)
        api = request.data.get('api')
        api=api.replace(" ","_")
        mapping = request.data.get('mapping')
        mapping=mapping.replace(" ","_")
        source_type = request.data.get('source_type')
        source_subtype = request.data.get('source_subtype')
        destination_type = request.data.get('destination_type')
        destination_subtype = request.data.get('destination_subtype')
        two_way = request.data.get('two_way', False)
        flow_num = request.data.get('flow_num')
        flow_num=flow_num.replace(" ","_")
        print(two_way,type(two_way))
        # print(str(two_way))
        if two_way == 'True':
            two_way = 'Yes'
        elif two_way =='False':
            two_way = 'No'

        if api and mapping and source_type and destination_type:
            try:
                source_color = Type_color.objects.get(type=source_type).color
                destination_color = Type_color.objects.get(type=destination_type).color
            except Type_color.DoesNotExist as e:
                return Response({'error': f"Type_color matching query does not exist: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            if source_subtype == 'NA':
                API = api
            else:
                API = api + "::" + source_subtype

            if destination_subtype == 'NA':
                MAP = mapping
            else:
                MAP = mapping + "::" + destination_subtype
            print(two_way,type(two_way))
            if flow_num=='None':
                if two_way:
                    mapping_data = f"\n    {API}<-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    mapping_data = f"\n    {API}-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
            else:
                if two_way:
                    mapping_data = f"\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                else:
                    mapping_data = f"\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
            print(mapping_data)
            project.mapping += mapping_data
            project.save()

            current_time = datetime.now()
            format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
            vn = version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
            vn = ver_naming(vn)

            version.objects.create(
                project_team=project,
                version_name=vn,
                version_timestamp=format_date,
                mapping=project.mapping
            )

            Master.objects.create(
                source=api,
                source_type=source_type,
                source_subtype=source_subtype,
                destination=mapping,
                destination_type=destination_type,
                destination_subtype=destination_subtype,
                project_team=project,
                flow_num=flow_num,
                two_way=two_way,
            )
            return Response({'success': 'Mapping added successfully'}, status=status.HTTP_201_CREATED)

        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project_team, Type_color, Subtype, version, Master
# from .utils import ver_naming
from datetime import datetime

class changeProjectdetails(APIView):
    def post(self,request,project_id):
        project=get_object_or_404(Project_team,pk=project_id)
        project_new_name=request.data.get('project_new_name')
        project_new_manager=request.data.get('project_new_manager')
        print(project_new_manager,project_new_name)
        project.project_name=project_new_name
        project.project_manager=project_new_manager
        project.save()

        return Response({'success': 'Node updated successfully'}, status=status.HTTP_200_OK)
        
class changeFlownum(APIView):
    def post(self,request,project_id):
        project = get_object_or_404(Project_team, pk=project_id)
        flow_num=request.data.get('flow_num')
        flow_num_new=request.data.get('flow_num_new')
        flow_num_new=flow_num_new.replace(" ","_")
        print(flow_num,flow_num_new)
        updated_mapping = project.mapping.replace(flow_num, flow_num_new)
        project.mapping = updated_mapping
        project.save()

        current_time = datetime.now()
        format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
        vn = version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
        vn = ver_naming(vn)

        version.objects.create(
            project_team=project,
            version_name=vn,
            version_timestamp=format_date,
            mapping=project.mapping
        )

        Master.objects.filter(flow_num=flow_num, project_team=project).update(flow_num=flow_num_new)
       
        return Response({'success': 'Node updated successfully'}, status=status.HTTP_200_OK)








class UpdateNodeAPI(APIView):
    def post(self, request, project_id):
        project = get_object_or_404(Project_team, pk=project_id)
        node_name = request.data.get('node_name')
        new_node_name = request.data.get('new_node_name')
        new_node_name=new_node_name.replace(" ","_")
        type_id = request.data.get('type_up')
        subtype_name = request.data.get('subtype_up')

        if node_name and new_node_name and type_id and subtype_name:
            try:
                type_obj = Type_color.objects.get(type=type_id)
                subtype_obj = Subtype.objects.get(subtype=subtype_name, type_id=type_obj.id)
            except (Type_color.DoesNotExist, Subtype.DoesNotExist) as e:
                return Response({'error': f"Type_color or Subtype matching query does not exist: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            updated_mapping = project.mapping.replace(node_name, f'{new_node_name}::{subtype_obj.subtype}')
            project.mapping = updated_mapping
            project.save()

            current_time = datetime.now()
            format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
            vn = version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
            vn = ver_naming(vn)

            version.objects.create(
                project_team=project,
                version_name=vn,
                version_timestamp=format_date,
                mapping=project.mapping
            )

            node_name = node_name.split('::')[0]

            Master.objects.filter(source=node_name, project_team=project).update(
                source=new_node_name,
                source_type=type_id,
                source_subtype=subtype_obj.subtype
            )
            Master.objects.filter(destination=node_name, project_team=project).update(
                destination=new_node_name,
                destination_type=type_id,
                destination_subtype=subtype_obj.subtype
            )

            return Response({'success': 'Node updated successfully'}, status=status.HTTP_200_OK)

        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project_team, Master, Type_color, version

class SelectApiView(APIView):
    def get(self, request, project_id, api):
        project = get_object_or_404(Project_team, pk=project_id)
        data = Master.objects.filter(project_team_id=project_id)
        filtered_mappings = ""
        apis = set()
        node_styles = ""

        for i in data:
            if api in i.source or api in i.destination:
                if i.flow_num=='None':
                    if i.two_way == 'Yes':
                        filtered_mappings += f"    {i.source}::{i.source_subtype}<-->{i.destination}::{i.destination_subtype};\n"
                    else:
                        filtered_mappings += f"    {i.source}::{i.source_subtype}-->{i.destination}::{i.destination_subtype};\n"
                else:
                    if i.two_way == 'Yes':
                        filtered_mappings += f"    {i.source}::{i.source_subtype}<-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
                    else:
                        filtered_mappings += f"    {i.source}::{i.source_subtype}-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
                source_color = Type_color.objects.get(type=i.source_type).color
                destination_color = Type_color.objects.get(type=i.destination_type).color
                node_styles += f"    style {i.source}::{i.source_subtype} fill:{source_color},stroke:#333,stroke-width:2px;\n"
                node_styles += f"    style {i.destination}::{i.destination_subtype} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

                apis.add(i.source)
                apis.add(i.destination)

        filtered_mappings += "\n%% Node styles\n" + node_styles

        data = Master.objects.filter(project_team_id=project_id)
        filtered_mappings_1 = "graph TD;\n"
        node_styles = ''
        for i in data:
            if i.flow_num=='None':
                if i.two_way == 'Yes':
                    filtered_mappings_1 += f"    {i.source}::{i.source_subtype}<-->{i.destination}::{i.destination_subtype};\n"
                else:
                    filtered_mappings_1 += f"    {i.source}::{i.source_subtype}-->{i.destination}::{i.destination_subtype};\n"
            else:
                if i.two_way == 'Yes':
                    filtered_mappings_1 += f"    {i.source}::{i.source_subtype}<-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
                else:
                    filtered_mappings_1 += f"    {i.source}::{i.source_subtype}-->|{i.flow_num}|{i.destination}::{i.destination_subtype};\n"
            source_color = Type_color.objects.get(type=i.source_type).color
            destination_color = Type_color.objects.get(type=i.destination_type).color
            node_styles += f"    style {i.source}::{i.source_subtype} fill:{source_color},stroke:#333,stroke-width:2px;\n"
            node_styles += f"    style {i.destination}::{i.destination_subtype} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

        filtered_mappings_1 += "\n%% Node styles\n" + node_styles
        send_mapping = filtered_mappings_1
        vl = version.objects.filter(project_team=project).values_list('version_name', flat=True).distinct()
        vl = list(vl)

        return Response({
            'project': {
                'id': project.id,
                'project_name': project.project_name,
                'project_manager': project.project_manager
            },
            'apis': sorted(apis),
            'selected_api': api,
            'filtered_mappings': filtered_mappings.strip(),
            'send_mapping': send_mapping,
            'versions': vl
        }, status=status.HTTP_200_OK)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Project_team, Master, Type_color, version

class SelectVersionView(APIView):
    def get(self, request, project_id, ver):
        project = get_object_or_404(Project_team, pk=project_id)
        version_obj = version.objects.filter(project_team=project).get(version_name=ver)
        version_mapping = version_obj.mapping
        version_time = version_obj.version_timestamp

        data = Master.objects.filter(project_team_id=project_id)
        apis = set()
        filtered_mappings = "graph TD;\n"
        node_styles = ''

        for i in data:
            if i.source_subtype == 'NA':
                API = i.source
            else:
                API = i.source + '::' + i.source_subtype
            if i.destination_subtype == 'NA':
                MAP = i.destination
            else:
                MAP = i.destination + '::' + i.destination_subtype

            if i.two_way == 'Yes':
                filtered_mappings += f"    {API}<-->|{i.flow_num}|{MAP};\n"
            else:
                filtered_mappings += f"    {API}-->|{i.flow_num}|{MAP};\n"
            source_color = Type_color.objects.get(type=i.source_type).color
            destination_color = Type_color.objects.get(type=i.destination_type).color
            node_styles += f"    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n"
            node_styles += f"    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;\n"

        filtered_mappings += "\n%% Node styles\n" + node_styles

        for i in data:
            apis.add(i.source)
            apis.add(i.destination)

        vl = version.objects.filter(project_team=project).values_list('version_name', flat=True).distinct()
        vl = list(vl)

        return Response({
            'project': {
                'id': project.id,
                'project_name': project.project_name,
                'project_manager': project.project_manager
            },
            'apis': sorted(apis),
            'filtered_mappings': filtered_mappings.strip(),
            'send_mapping': filtered_mappings.strip(),
            'version_mapping': version_mapping,
            'version_time': version_time,
            'ver': ver,
            'versions': vl
        }, status=status.HTTP_200_OK)





import pandas as pd
from io import BytesIO
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Project_team, Type_color, Master, version
@api_view(['POST'])
def add_mapping_excel(request, project_id):
    project = get_object_or_404(Project_team, pk=project_id)

    if request.method == 'POST' and request.FILES['file']:
        if 'file' not in request.FILES:
            print("File not in request")
        
        excel_file = request.FILES['file']
        print(excel_file,type(excel_file),"Hello")
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Assuming the Excel file has columns: 'API', 'Mapping', 'Source Type', 'Source Subtype', 'Destination Type', 'Destination Subtype', 'Flow Number', 'Two Way'
        for _, row in df.iterrows():
            api = row['Source']
            api=api.replace(" ","_")
            mapping = row['Destination']
            mapping=mapping.replace(" ","_")
            source_type = row['Source_type']
            source_subtype = row['Source_subtype'] if not pd.isna(row['Source_subtype']) else 'NA'
            destination_type = row['Destination_type']
            destination_subtype = row['Destination_subtype'] if not pd.isna(row['Destination_subtype']) else 'NA'
            # flow_num=int(row['Flow_num'])
            flow_num = str(row['Flow_num'])
            if flow_num=='nan':
                flow_num='None'
            print(flow_num,type(flow_num))
            two_way = row['two_way'] 
            flow_num=flow_num.replace(" ","_")
           

            if api and mapping and source_type and destination_type:
                try:
                    source_color = Type_color.objects.get(type=source_type).color
                    destination_color = Type_color.objects.get(type=destination_type).color
                except Type_color.DoesNotExist:
                    continue

                if source_subtype == 'NA':
                    API = api
                else:
                    API = f"{api}::{source_subtype}"

                if destination_subtype == 'NA':
                    MAP = mapping
                else:
                    MAP = f"{mapping}::{destination_subtype}"
                if flow_num=='None':
                    if two_way:
                        mapping_data = f"\n    {API}<-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                    else:
                        mapping_data = f"\n    {API}-->{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                    
                else:
                    if two_way:
                        mapping_data = f"\n    {API}<-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"
                    else:
                        mapping_data = f"\n    {API}-->|{flow_num}|{MAP};\n\n    %% Node styles\n    style {API} fill:{source_color},stroke:#333,stroke-width:2px;\n    style {MAP} fill:{destination_color},stroke:#333,stroke-width:2px;"

                project.mapping += mapping_data

                # Save to Master table
                Master.objects.create(
                    source=api,
                    source_type=source_type,
                    source_subtype=source_subtype,
                    destination=mapping,
                    destination_type=destination_type,
                    destination_subtype=destination_subtype,
                    project_team=project,
                    flow_num=flow_num,
                    two_way=two_way
                )

        project.save()

        # version naming
        from datetime import datetime
        current_time = datetime.now()
        format_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
        vn = version.objects.filter(project_team=project).order_by('version_timestamp').last().version_name
        vn = ver_naming(vn)

        version.objects.create(
            project_team=project,
            version_name=vn,
            version_timestamp=format_date,
            mapping=project.mapping
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request or file not found'}, status=400)

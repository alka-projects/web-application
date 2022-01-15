from django.shortcuts import render
from web_app.forms import studentform
from web_app.models import student
from django.shortcuts import redirect,get_object_or_404
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    student_list = student.objects.all().order_by('-id') 
    return render(request,'web_app/home.html', {'student_list':student_list})

@login_required
def edit(request,id):
    student_list = get_object_or_404(student, id=id)
    if(request.method == "POST"):
        name = request.POST.get("name")
        email = request.POST.get("email")
        form = studentform(request.POST, instance = student_list)

        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'web_app/edit.html',{'name':student_list.name, "email": student_list.email})

@login_required
def new(request):
    form = studentform()
    if request.method == 'POST':
        form = studentform(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request,'web_app/new.html', {'form':form})

@login_required
def delete_record(request,id):
    student_list = student.objects.all().filter(id=id).delete()
    return redirect('/')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="web_app/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

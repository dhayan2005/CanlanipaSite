from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, ComplaintForm
from django.contrib.auth.models import User
from .models import ResidentProfile, Complaint, Profile
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from .serializers import ComplaintSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response 
from rest_framework import permissions  
from rest_framework.views import APIView  
from rest_framework import status  

from django.shortcuts import render

def home(request):
    return render(request, 'barangay/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Username already exists. Please choose another one.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=form.cleaned_data['password']
                )
                ResidentProfile.objects.create(
                    user=user,
                    fullname=form.cleaned_data['fullname'],
                    age=form.cleaned_data['age'],
                    purok=form.cleaned_data['purok'],
                    email=form.cleaned_data['email']
                )

                login(request, user)
                return redirect('complaint') 
    else:
        form = SignUpForm()
    return render(request, 'barangay/signup.html', {'form': form})

from .models import ResidentProfile

@login_required
def complaint_submission(request):
    user_profile = ResidentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.resident = request.user  # Assuming your Complaint model links to the user
            complaint.save()
            return redirect('complaint_success')
    else:
        form = ComplaintForm(initial={
            'email': user_profile.email,
            'contact_number': user_profile.contact_number,
        })

    return render(request, 'complaint.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('complaint')
    else:
        form = LoginForm()
    return render(request, 'barangay/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def complaint_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.resident = request.user  # if you want to link to the user
            complaint.save()
            # redirect or render success
    else:
        form = ComplaintForm(initial={
            'email': request.user.email,
            'contact_number': request.user.residentprofile.contact_number if hasattr(request.user, 'residentprofile') else ''
        })
    # get complaints to display
    complaints = Complaint.objects.filter(resident=request.user)
    return render(request, 'barangay/complaint.html', {'form': form, 'complaints': complaints})



def complaint_review(request):
    if not request.user.is_authenticated:
        return redirect('login')
    complaints = Complaint.objects.filter(resident=request.user)
    return render(request, 'barangay/complaint_review.html', {'complaints': complaints})

def edit_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id, resident=request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Complaint updated successfully!')
            return redirect('complaint_review')
    else:
        form = ComplaintForm(instance=complaint)
    return render(request, 'barangay/edit_complaint.html', {'form': form})

def delete_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id, resident=request.user)
    if request.method == 'POST':
        complaint.delete()
        messages.success(request, 'Complaint deleted successfully!')
        return redirect('complaint_review')
    return render(request, 'barangay/delete_complaint_confirm.html', {'complaint': complaint})

def about(request):
    officials = [
        {"name": "Hon. Joel A. Cambalon", "position": "Punong Barangay"},
        {"name": "Hon. Jerry C. Manlimos", "position": "Chair Committee on Peace & Order and Public Safety/Rule and Privileges"},
        {"name": "Hon. Leonardo A. Ejandra", "position": "Chair Committe on Agriculture/Cooperative"},
        {"name": "Hon. Melvin L. Conde", "position": "Chair Committee on Public Works Transportation/Communication"},
        {"name": "Hon. Kym R. Ellena", "position": "Chair Committee on Budget and Appropriation/Ways & Means"},
        {"name": "Romeo R. Juarez, Sr.", "position": "Barangay Secretary"},
        {"name": "Hon. Mark Quincy V. Menor", "position": "Chair Committe on Environmental Protection and Human Rights"},
        {"name": "Hon. Cristita C. Juanite", "position": "Chair Committee on Women and Family/Health & Social Services"},
        {"name": "Hon. Eve Gary L. Florendo", "position": "Chair Committee on Education & Culture/Tourism/Trade & Industry"},
        {"name": "Hon. Gerald M. Bayang", "position": "Chair Committee on Sports and Youth Development"},
        {"name": "Arche F. Ca-as", "position": "Barangay Treasurer"},
    ]
    return render(request, 'barangay/about.html', {"officials": officials})


class UserComplaintList(generics.ListAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Complaint.objects.filter(resident=self.request.user)


class ComplaintDetail(generics.RetrieveAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]

class UpdateComplaintStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]  # Only admin/police can update

    def patch(self, request, pk):
        complaint = get_object_or_404(Complaint, pk=pk)
        new_status = request.data.get('status')

        if new_status not in ['PENDING', 'IN_ACTION', 'RESOLVED']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        complaint.status = new_status
        complaint.save()
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data, status=status.HTTP_200_OK)
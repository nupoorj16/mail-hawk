import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm  # type: ignore
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .gmail_service import get_flow, get_gmail_service  # type: ignore
from .models import ScrapedEmail  # type: ignore
from .utils import get_flow, get_gmail_service  # type: ignore
from django.contrib import messages
from .crewai_pipeline import get_email_category  # type: ignore
from django.db.models import Count

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Get all emails for the logged-in user
    user_emails = ScrapedEmail.objects.filter(user=request.user)

    # Count emails by category
    category_summary = (
        user_emails
        .values('category')
        .annotate(count=Count('category'))
        .order_by('-count')
    )

    # Get 10 most recent emails
    recent_emails = user_emails.order_by('-timestamp')[:10]

    return render(request, 'users/dashboard.html', {
        'category_summary': category_summary,
        'recent_emails': recent_emails
    })


def connect_gmail(request):
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)


@login_required(login_url='/login/')
def oauth2_callback(request):
    flow = get_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    service = get_gmail_service(credentials)

    results = service.users().messages().list(userId='me', maxResults=20).execute()
    messages = results.get('messages', [])

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = msg_data['payload']['headers']
        subject = sender = None
        snippet = msg_data.get('snippet', '')
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            if header['name'] == 'From':
                sender = header['value']

        category = get_email_category(subject or "", snippet or "")

        ScrapedEmail.objects.create(
            user=request.user,
            sender=sender or "Unknown",
            subject=subject or "(No Subject)",
            snippet=snippet,
            category=category
        )

    request.session['gmail_connected'] = True
    return redirect('dashboard')

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from datetime import datetime

from .forms import DateForm, NewPitchForm, NewUserForm
from .models import Pitch, Profile, Booking


@login_required(login_url="/login/")
def homepage(request):
    if request.method == "POST":
        form_date = DateForm(request.POST)
        if form_date.is_valid():
            date = form_date.cleaned_data.get("date_field")
            pitches = Pitch.objects.all()
            context = {'date': date, 'form': pitches}
            return render(request, "view_bookings.html", context)
        else:
            print(form_date.errors)
    form_date = DateForm()
    return render(
        request=request, template_name="home.html", context={"form": form_date}
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect("homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.address = form.cleaned_data.get("address")
            user.phone_numbner = form.cleaned_data.get("phone_number")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            user.save()
            messages.success(request, "Registration successful.")
            return redirect("/login")
        else:
            print(form.errors)
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request, template_name="register.html", context={"register_form": form}
    )


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = Profile.object.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "email_template.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "PitchBook",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject=subject,
                            message=email,
                            from_email=None,
                            recipient_list=[user.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(e)
                        return HttpResponse("Invalid header found")

                    messages.success(
                        request,
                        "A message with reset password instructions has been sent to your inbox.",
                    )
                    return redirect("login")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"password_reset_form": password_reset_form},
    )


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")


@login_required(login_url="/login/")
def manage_pitch_table(request):
    pitches = Pitch.objects.all()
    return render(request, "manage_pitch.html", context={"form": pitches})


@login_required(login_url="/login/")
def view_pitch_table(request):
    pitches = Pitch.objects.all()
    return render(request, "view_bookings.html", context={"form": pitches})


@login_required(login_url="/login/")
def add_pitch_request(request):
    if request.method == "POST":
        form = NewPitchForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            print(request)
            pitch = form.save()
            pitch.refresh_from_db()
            pitch.name = form.cleaned_data.get("name")
            pitch.size = form.cleaned_data.get("size")
            pitch.price = form.cleaned_data.get("price")
            pitch.save()
            return redirect("manage_pitch")
        else:
            print(form.errors)
    form = NewPitchForm()
    return render(request, "add_pitch.html", {"form": form})


@login_required(login_url="/login/")
def edit_pitch_request(request, uidb64):
    pitch = Pitch.objects.get(id=uidb64)
    form = NewPitchForm(instance=pitch)
    if request.method == "POST":
        form = NewPitchForm(request.POST, instance=pitch)
        if form.is_valid():
            pitch = form.save()
            pitch.refresh_from_db()
            pitch.name = form.cleaned_data.get("name")
            pitch.size = form.cleaned_data.get("size")
            pitch.price = form.cleaned_data.get("price")
            pitch.save()
            return redirect("manage_pitch")

    context = {
        "pitch": pitch,
        "form": form,
    }
    return render(request, "edit_pitch.html", context)


@login_required(login_url="/login/")
def delete_pitch_request(request, uidb64):
    pitch = Pitch.objects.get(id=uidb64)

    if request.method == "POST":
        pitch.delete()
        return redirect("manage_pitch")

    context = {"pitch": pitch}
    return render(request, "delete_pitch.html", context)

@login_required(login_url="/login/")
def book_pitch(request, date, uidb64):
    pitch_id = uidb64
    time_list = get_available_time(date, pitch_id)
    context = {'time_list': time_list}
    if request.method == "POST":
        timeslot_ = None 
        for timeslot in Booking.TIMESLOT_LIST:
            if timeslot[1].startswith(request.POST['timeslot']):
                timeslot_ = timeslot[0]
        try:
            pitch = Pitch.objects.get(id = uidb64)
            user = Profile.objects.get(id=request.user.id)
            booking_entry = Booking.objects.create(pitch_id=pitch,
                                                user_id=user,
                                                pitch_name = pitch.name,
                                                pitch_price=pitch.price,
                                                pitch_size=pitch.size,
                                                date = date,
                                                time = request.POST['timeslot'],
                                                timeslot = timeslot_)

            booking_entry.save()
        except Exception as e:
            print(e)
        return redirect('homepage')

    return render(request, "bookings.html", context)


@login_required(login_url="/login/")
def my_booking(request):
    bookings = Booking.objects.filter(user_id_id=request.user.id)
    print(bookings)
    return render(request, "my_bookings.html", context={"form": bookings})


@login_required(login_url="/login/")
def delete_booking_request(request, uidb64):
    booking = Booking.objects.get(id=uidb64)
    booking.delete()
    
    return redirect("my_booking")


def get_available_time(date: datetime.date, pitch_id):
    existing_bookings = list(Booking.objects.filter(date=date, pitch_id=pitch_id).values_list('timeslot'))
    print(existing_bookings)
    timeslot_list = Booking.TIMESLOT_LIST

    time_list = []
    is_booked = None

    for timeslot in timeslot_list:
        if any([timeslot[0] == i[0] for i in existing_bookings]):
            is_booked = True 
        else:
            is_booked = False 
        time_list.append({"time": timeslot[1].split(' - ')[0], "is_booked": is_booked})

    return time_list
    


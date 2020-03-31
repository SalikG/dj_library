from datetime import datetime, date, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, BookLoan, Magazine, MagazineLoan
from login_app.models import UserProfile
from django.urls import reverse
from django.utils import timezone


def is_staff(user):
    user_profile = UserProfile.objects.get(user=user)
    return user_profile.role.role == "staff"


@login_required
def index(request):
    checkouts = {'books': BookLoan.objects.filter(user=request.user, is_handed_in=False),
                 'magazines': MagazineLoan.objects.filter(user=request.user, is_handed_in=False)}
    all_books = Book.objects.all()
    all_magazines = Magazine.objects.all()

    context = {
        'books': all_books,
        'magazines': all_magazines,
        'checkouts': checkouts,
    }
    return render(request, 'library_app/index.html', context)


@login_required
def search(request):
    if request.method == 'POST':
        search_value = request.POST['title_search_value']
        search_book_result = Book.objects.filter(title__contains=search_value)
        search_magazine_result = Magazine.objects.filter(title__contains=search_value)
        checkouts = {'books': BookLoan.objects.filter(user=request.user),
                     'magazines': MagazineLoan.objects.filter(user=request.user)}
        context = {
            'books': search_book_result,
            'magazines': search_magazine_result,
            'checkouts': checkouts,
        }
        return render(request, 'library_app/index.html', context)

    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def checkout_book(request):
    if request.method == 'POST':
        checked_out_books = BookLoan.objects.filter(user=request.user, is_handed_in=False)
        outstanding_book_loans = [book_loan for book_loan in checked_out_books if book_loan.due_date < timezone.now()]

        if outstanding_book_loans.__len__() > 0:
            checkouts = {'books': BookLoan.objects.filter(user=request.user, is_handed_in=False),
                         'magazines': MagazineLoan.objects.filter(user=request.user, is_handed_in=False)}
            all_books = Book.objects.all()
            all_magazines = Magazine.objects.all()

            context = {
                'book_error': 'You have an outstanding loan!',
                'books': all_books,
                'magazines': all_magazines,
                'checkouts': checkouts,
            }
            return render(request, 'library_app/index.html', context)
        if checked_out_books.count() >= 10:
            checkouts = {'books': BookLoan.objects.filter(user=request.user, is_handed_in=False),
                         'magazines': MagazineLoan.objects.filter(user=request.user, is_handed_in=False)}
            all_books = Book.objects.all()
            all_magazines = Magazine.objects.all()

            context = {
                'book_error': 'Max checkouts reached!',
                'books': all_books,
                'magazines': all_magazines,
                'checkouts': checkouts,
            }
            return render(request, 'library_app/index.html', context)
        else:
            book_id = request.POST['book_id']
            selected_book = Book.objects.get(pk=book_id)
            due_date = (date.today() + timedelta(days=30)).isoformat()
            book_loan = BookLoan(book=selected_book, user=request.user, due_date=due_date)
            book_loan.save()

    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def checkin_book(request):
    if request.method == 'POST':
        book_loan_id = request.POST['book_loan_id']
        selected_book_loan = BookLoan.objects.get(pk=book_loan_id)
        selected_book_loan.is_handed_in = True
        selected_book_loan.hand_in_date = datetime.now()
        selected_book_loan.save()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def checkout_magazine(request):
    if request.method == 'POST':
        checked_out_magazines = MagazineLoan.objects.filter(user=request.user, is_handed_in=False)
        outstanding_magazine_loans = [magazine_loan for magazine_loan in checked_out_magazines if magazine_loan.due_date < timezone.now()]

        if outstanding_magazine_loans.__len__() > 0:
            checkouts = {'books': BookLoan.objects.filter(user=request.user, is_handed_in=False),
                         'magazines': MagazineLoan.objects.filter(user=request.user, is_handed_in=False)}
            all_books = Book.objects.all()
            all_magazines = Magazine.objects.all()

            context = {
                'magazine_error': 'You have an outstanding loan!',
                'books': all_books,
                'magazines': all_magazines,
                'checkouts': checkouts,
            }
            return render(request, 'library_app/index.html', context)
        if checked_out_magazines.count() >= 3:
            checkouts = {'books': BookLoan.objects.filter(user=request.user, is_handed_in=False),
                         'magazines': MagazineLoan.objects.filter(user=request.user, is_handed_in=False)}
            all_books = Book.objects.all()
            all_magazines = Magazine.objects.all()

            context = {
                'magazine_error': 'Max checkouts reached!',
                'books': all_books,
                'magazines': all_magazines,
                'checkouts': checkouts,
            }
            return render(request, 'library_app/index.html', context)
        else:
            magazine_id = request.POST['magazine_id']
            selected_magazine = Magazine.objects.get(pk=magazine_id)
            due_date = (date.today() + timedelta(days=7)).isoformat()
            magazine_loan = MagazineLoan(magazine=selected_magazine, user=request.user, due_date=due_date)
            magazine_loan.save()

    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
def checkin_magazine(request):
    if request.method == 'POST':
        magazine_loan_id = request.POST['magazine_loan_id']
        selected_magazine_loan = MagazineLoan.objects.get(pk=magazine_loan_id)
        selected_magazine_loan.is_handed_in = True
        selected_magazine_loan.hand_in_date = datetime.now()
        selected_magazine_loan.save()
    return HttpResponseRedirect(reverse('library_app:index'))


@login_required
@user_passes_test(is_staff)
def outstanding_loans(request):
    checked_out_magazines = MagazineLoan.objects.filter(user=request.user, is_handed_in=False)
    outstanding_magazine_loans = [magazine_loan for magazine_loan in checked_out_magazines if
                                  magazine_loan.due_date < timezone.now()]
    checked_out_books = BookLoan.objects.filter(user=request.user, is_handed_in=False)
    outstanding_book_loans = [book_loan for book_loan in checked_out_books if book_loan.due_date < timezone.now()]

    outstanding_loans = {"books": outstanding_book_loans,
                         "magazines": outstanding_magazine_loans}
    context = {"outstanding_loans": outstanding_loans}
    return render(request, 'library_app/outstanding_loans.html', context)

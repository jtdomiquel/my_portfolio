from django.shortcuts import render

def login_view(request):
    if request.method == 'POST':
        
        username = request.POST.get('username')  
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:

                login(request, user)
                user_type = user.user_type
                if user.user_type == "Admin" or user.user_type == "Marketing Head" or user.user_type == "Monitoring Staff":
                    return redirect('admin_dashboard')
                elif user_type =="Marketing":
                    return redirect('marketing_dashboard')
                elif user_type =="Cashier":
                    return redirect('cashier_dashboard')
                elif user_type =="Accounting" or user.user_type == "Procurement Staff" or user.user_type == "Billing Staff":
                    return redirect('accounting_dashboard')
                elif user_type =="Depositor":
                    return redirect('depositor_dashboard')
                elif user_type =="Developer":
                    return redirect('developer_dashboard')
                elif user_type =="Document Controller" or user.user_type == "Permit In-charge" or user.user_type == "Turn-Over Section":
                    return redirect('documentation_dashboard')
                elif user_type =="Manager":
                    return redirect('manager_dashboard')
                elif user_type =="Project Engineer":
                    return redirect('project_engineer_dashboard')
                else:
                    messages.error(request, 'Other User')

            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Both username and password are required.')
    
    return render(request, 'login.html')

def home_page(request):
    return render(request, 'home_page.html')

def about_me(request):
    return render(request, 'about_me.html')

def portfolio(request):
    return render(request, 'portfolio.html')


    

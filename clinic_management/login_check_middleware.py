from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleware(MiddlewareMixin):
    def process_view(self,request,view_func, view_args, view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "clinic_management.admin_views":
                    pass
                elif modulename == "clinic_management.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "clinic_management.patient_views":
                    pass
                elif modulename == "clinic_management.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("patient_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
from braces import views
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _


class ProtectedViewMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.pre_dispatch(request, *args, **kwargs)
        return super(ProtectedViewMixin, self).dispatch(request, *args,
                                                        **kwargs)

    def pre_dispatch(self, request, *args, **kwargs):
        pass


class PermissionMixin(views.LoginRequiredMixin,
                      views.PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        """
        Check to see if the user in the request has the required
        permission.
        """
        has_permission = self.check_permissions(request)

        if not has_permission:  # If the user lacks the permission
            if request.user.is_authenticated():
                raise PermissionDenied  # Return a 403
            return self.no_permissions_fail(request)

        return super(PermissionMixin, self).dispatch(
            request, *args, **kwargs)


class UIMixin(ProtectedViewMixin):
    page_title = None

    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if hasattr(self, 'object'):
            return self.object

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['page_title'] = self.get_page_title()
        # d['server_instance'] = getattr(settings, 'INSTANCE_NAME', None)
        return d


class PaginationMixin(object):
    allow_empty = True
    paginate_by = None
    paginate_orphans = 0
    paginator_class = Paginator
    page_kwarg = 'page'

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(
            page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(
                    "Page is not 'last', nor can it be converted to an int."))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })

    def get_paginate_by(self):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0,
                      allow_empty_first_page=True, **kwargs):
        """
        Return an instance of the paginator for this view.
        """
        return self.paginator_class(
            queryset, per_page, orphans=orphans,
            allow_empty_first_page=allow_empty_first_page, **kwargs)

    def get_paginate_orphans(self):
        """
        Returns the maximum number of orphans extend the last page by when
        paginating.
        """
        return self.paginate_orphans

    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty

    def paginate(self, queryset):
        page_size = self.get_paginate_by()
        if not page_size:
            return {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset
            }

        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, page_size)
        return {
            'paginator': paginator,
            'page_obj': page,
            'is_paginated': is_paginated,
            'object_list': queryset
        }

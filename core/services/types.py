from rest_framework import generics, views, viewsets, mixins
from . import log


class LoggedAPIView(views.APIView):
    """
    Since responses must go through dispatch method defined in views.APIView,
    the simplest way to do API logging is to hook the dispatch method with
    a logging decorator.
    """
    @log.debug()
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# The following definitions are not needed but
# they are presented below to illustrate how
# one can define custom View/ViewSet classes 
# to enable API logging for specific endpoints

# class LoggedGenericAPIView(generics.GenericAPIView, LoggedAPIView):
#     ...

# class LoggedViewSet(viewsets.ViewSetMixin, LoggedAPIView):
#     ...

# class LoggedGenericViewSet(viewsets.ViewSetMixin, LoggedGenericAPIView):
#     ...

# class LoggedReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet, LoggedGenericViewSet):
#     ...
    
# class LoggedModelViewSet(viewsets.ModelViewSet, LoggedGenericViewSet):
#     ...

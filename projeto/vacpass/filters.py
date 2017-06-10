import django_filters


class VacinaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome')


class SolicitacaoFilter(django_filters.FilterSet):
    vacina__nome = django_filters.CharFilter(lookup_expr='icontains', label='nome da vacina')
    solicitante__django_user__first_name = django_filters.CharFilter(lookup_expr='icontains', label='nome da usuario')

    def __init__(self, data=None, queryset=None, prefix=None, strict=None, request=None, id_formulario=0):
        super().__init__(data, queryset, prefix, strict, request)
        for x in self.base_filters:
            self.filters[x + str(id_formulario)] = self.filters.pop(x)


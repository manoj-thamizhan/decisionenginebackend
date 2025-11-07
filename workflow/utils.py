from django.shortcuts import get_object_or_404

def get_distinct_values_from_target_for_source(
    source_model,
    target_model,
    pk,
    source_fields=None,
    target_fields=None
):
    """
    Given a source model instance, filters target model by matching fields
    and returns distinct non-null, non-blank values from the target queryset.
    """
    source_obj = get_object_or_404(source_model, pk=pk)

    # Default: common fields between source and target
    if source_fields is None:
        source_field_names = {f.name for f in source_model._meta.fields if f.name != source_model._meta.pk.name}
        target_field_names = {f.name for f in target_model._meta.fields if f.name != target_model._meta.pk.name}
        source_fields = list(source_field_names & target_field_names)

    # Build filter kwargs based on source instance values
    filter_kwargs = {}
    for f in source_fields:
        value = getattr(source_obj, f)
        if value not in [None, ""]:  # skip null or blank values
            filter_kwargs[f] = value

    # Filter target queryset
    qs = target_model.objects.filter(**filter_kwargs)

    # Default: get all target fields except PK
    if target_fields is None:
        target_fields = [f.name for f in target_model._meta.fields if f.name != target_model._meta.pk.name]

    result = {}

    for field in target_fields:
        distinct_vals = (
            qs.order_by()
              .values_list(field, flat=True)
              .distinct()
              .exclude(**{f"{field}__isnull": True})  # skip None
              .exclude(**{f"{field}": ""})             # skip blank
        )
        result[field] = list(distinct_vals)

    return result

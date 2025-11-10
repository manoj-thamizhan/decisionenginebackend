from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from workflow.utils import get_distinct_values_from_target_for_source  # optional, if you have django-filter
from .models import Flow, PLMWindchillMockdata, UdiFiaWorkflow,  ChangesInvolved,Rule
from .serializers import (
    FlowSerializer,
    UdiFiaWorkflowSerializer,
    ChangesInvolvedSerializer,
    RuleSerializer
)
from django.db import transaction
from rest_framework.views import APIView


class UdiFiaWorkflowViewSet(viewsets.ModelViewSet):
    queryset = UdiFiaWorkflow.objects.all().order_by('-created_at')
    serializer_class = UdiFiaWorkflowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['created_at', 'updated_at', 'title']
    MODELB_FILTERABLE_FIELDS = [
            'id',
            'health_authority',
            'udi_regulation',
            'category',
            'data_property',
            'data_attribute_ha_field_name',
            'gude_field_name',
            'jnj_udi_data_element',
            'gude_field_number',
            'budi_attribute_eudamed_only',
            'gs1_gtin_trigger_100782299_appendix_b',
            'health_authority_gtin_trigger',
            'jjmt_use_directive',
            'mandatory_field_in_database',
            'field_type',
            'add_flag',
            'edit_flag',
            'delete_flag',
            'change_condition_or_scenarios',
            'additional_change_request_requirements',
            'dri_comments',
            'gtin_outcome_action',
            'data_source_outcome_action',
        ]

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """
        Handle PATCH: clean non-null/non-blank keys from request.data,
        use them to filter ModelB, update ModelA, and return:
          - updated ModelA
          - filtered ModelB list
          - the ModelB field that has the least number of distinct values
        """
        instance = self.get_object()

        cleaned = {}
        for k, v in request.data.items():
            if k is None:
                continue
            if v is None:
                continue
            if isinstance(v, str) and v.strip() == "":
                continue
            cleaned[k] = v

        filter_kwargs = {}
        for k, v in cleaned.items():
            if k in self.MODELB_FILTERABLE_FIELDS:
                filter_kwargs[k] = v
            else:
                filter_kwargs[f"{k}__icontains"] = v

        try:
            modelb_qs = Rule.objects.filter(**filter_kwargs)
        except Exception:
            modelb_qs = Rule.objects.none()

        least_field_info = None 

        candidate_fields = [
            'health_authority',
            'udi_regulation',
            'category',
            'data_property',
            'data_attribute_ha_field_name',
            'gude_field_name',
            'jnj_udi_data_element',
            'gude_field_number',
            'budi_attribute_eudamed_only',
            'gs1_gtin_trigger_100782299_appendix_b',
            'health_authority_gtin_trigger',
            'jjmt_use_directive',
            'mandatory_field_in_database',
            'field_type',
            'add_flag',
            'edit_flag',
            'delete_flag',
            'change_condition_or_scenarios',
            'additional_change_request_requirements',
            'dri_comments',
        ]

        if modelb_qs.exists():
            best_count = None
            best_field = None
            best_sample = []

            for f in candidate_fields:
                fname = f

                try:
                    q = modelb_qs
                    q = q.exclude(**{f"{fname}__isnull": True})

                    internal = getattr(f, "get_internal_type", None)
                    if callable(internal):
                        t = f.get_internal_type()
                        if t in ("CharField", "TextField"):
                            q = q.exclude(**{fname: ""})

                    distinct_count = q.values(fname).distinct().count()

                    

                    if (best_count is None or distinct_count < best_count) and distinct_count > 1:
                        best_count = distinct_count
                        best_field = fname

                except Exception:
                    continue

            if best_field is not None:
                least_field_info = {
                    "field": best_field,
                    "distinct_count": best_count,
                    "sample_values": best_sample,
                }

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        modelb_serializer = RuleSerializer(modelb_qs, many=True)

        # 7) return combined response
        return Response({
            "updated": serializer.data,
            "filtered_modelb": modelb_serializer.data,
            'is_finalized':len(modelb_serializer.data) == 1,
            'action_item' : modelb_serializer.data[0]['gtin_outcome_action'] if len(modelb_serializer.data) == 1 else None,
            'data_source_outcome' : modelb_serializer.data[0]['data_source_outcome_action'] if len(modelb_serializer.data) == 1 else None,
            "least_distinct_field_in_modelb": least_field_info
        }, status=status.HTTP_200_OK)


# class ChangeCategoriesViewSet(viewsets.ModelViewSet):
#     queryset = ChangeCategories.objects.all().order_by('name')
#     serializer_class = ChangeCategoriesSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['name']
#     ordering_fields = ['name']


class ChangesInvolvedViewSet(viewsets.ModelViewSet):
    queryset = ChangesInvolved.objects.all().order_by('-id')
    serializer_class = ChangesInvolvedSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['workflow', 'change_category']
    search_fields = ['change_description']
    ordering_fields = ['id']


# lightweight_tfidf_qna.py
from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def chunk_text(text: str, max_length: int = 500) -> list[str]:
    """
    Split a long text into chunks of up to `max_length` characters each.
    Ensures that words are not cut off in the middle.
    """
    words = text.split()
    chunks = []
    current_chunk = ""

    for word in words:
        # Add word if it fits within the limit
        if len(current_chunk) + len(word) + 1 <= max_length:
            current_chunk += (" " if current_chunk else "") + word
        else:
            chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def choose_best_option_tfidf(
    question: str,
    options: List[str],
    corpus: List[str],
    top_k: int = 5,
    aggregation: str = "max",  # 'max', 'mean', 'sum'
) -> Dict[str, Any]:
    """
    Choose best option using TF-IDF retrieval against corpus.
    Returns same structured dict as the original sbert/faiss approach.
    """
    if not options:
        raise ValueError("options must be a non-empty list")

    # Build combined queries like before
    combined_queries = [f"{question} ||| {opt}" for opt in options]

    # Fit TF-IDF on corpus + queries so queries are in same vector space
    documents = list(corpus) + combined_queries
    vectorizer = TfidfVectorizer().fit(documents)
    corpus_vecs = vectorizer.transform(corpus)        # shape (n_corpus, dim)
    query_vecs = vectorizer.transform(combined_queries)  # shape (n_queries, dim)

    sim = cosine_similarity(query_vecs, corpus_vecs)  # (n_queries, n_corpus)

    details: Dict[str, Dict[str, Any]] = {}
    for i, opt in enumerate(options):
        row = sim[i]  # similarities to all corpus docs
        top_idxs = list(np.argsort(row)[::-1][:top_k])
        hits: List[Tuple[int, str, float]] = [(int(idx), corpus[idx], float(row[idx])) for idx in top_idxs]
        scores = [h[2] for h in hits]
        if not scores:
            agg = 0.0
        else:
            if aggregation == "max":
                agg = float(max(scores))
            elif aggregation == "mean":
                agg = float(sum(scores) / len(scores))
            elif aggregation == "sum":
                agg = float(sum(scores))
            else:
                raise ValueError("aggregation must be one of 'max','mean','sum'")
        details[opt] = {"agg_score": agg, "hits": hits}

    best_option = max(details.items(), key=lambda it: it[1]["agg_score"])[0]
    best_score = details[best_option]["agg_score"]

    return {"best_option": best_option, "best_score": best_score, "details": details}

def choose_best_from_django_model(
    field_question_map: dict,
    model,
    text_field: str,
    top_k: int = 3,
    aggregation: str = "max",
):
    """
    Minimal helper: for each entry in field_question_map (field -> question):
      - use distinct non-empty values of `field` as options
      - use all non-null values of `text_field` as corpus
      - call choose_best_option_tfidf and return results per field
    """
    # Lazy-import Django ORM only when used
    from django.db.models import F

    # Build corpus once
    corpus_qs = model.objects.exclude(**{f"{text_field}__isnull": True}).values_list(text_field, flat=True)
    corpus = [str(s) for s in corpus_qs if s is not None and str(s).strip() != ""]

    if not corpus:
        raise ValueError(f"No text found in model field '{text_field}' to build corpus.")

    results = {}
    for field, question in field_question_map.items():
        opts_qs = model.objects.values_list(field, flat=True).distinct()
        options = [str(x) for x in opts_qs if x is not None and str(x).strip() != ""]

        if not options:
            results[field] = {"error": f"No distinct non-empty values found for field '{field}'."}
            continue

        results[field] = choose_best_option_tfidf(
            question=question,
            options=options,
            corpus=corpus,
            top_k=top_k,
            aggregation=aggregation,
        )

    return results



class WorkflowLookupByIdentifier(APIView):
    """
    GET /.../?change_number=XYZ
    or
    GET /.../?udi_fia_number=ABC   (also accepts udr_fia_number)
    Returns one or more matching UdiFiaWorkflow serialized objects.
    """

    def get(self, request, *args, **kwargs):
        change_number = request.query_params.get("change_number")
        udi_number = request.query_params.get("udi_fia_number") 

        if not change_number and not udi_number:
            return Response(
                {"detail": "Provide 'change_number' or 'udi_fia_number' (or 'udr_fia_number') as query parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if change_number:
            data = PLMWindchillMockdata.objects.get(change_number=change_number)
        if udi_number:
            data = PLMWindchillMockdata.objects.get(udi_fia_number=udi_number)

        context = data.data
        qnf = {
        # "region": "Which region does this product belong to?",
        "country": "In which country is this product marketed or sold?",
        "gtin_change": "Has there been any change in the GTIN for this product?",
        "created_at": "When was this record created?",
        "updated_at": "When was this record last updated?",
        "product_type": "What type of product is this?",
        "product_category_unit": "What is the product’s category unit?",
        "product_category_level": "What is the product’s category level?",
        "gtin_evaluation": "What is the GTIN evaluation result for this product?",
        "has_udi_health_impact": "Does this product have any UDI-related health impact?",
        "has_impact_in_new_gtin": "Does this change have an impact on the new GTIN assignment?"
        }
        chunks = chunk_text(context)
        results = {}
        for field, question in qnf.items():
            opts_qs = Rule.objects.values_list(field, flat=True).distinct()
            options = [str(x) for x in opts_qs if x is not None and str(x).strip() != ""]

            if not options:
                results[field] = {"error": f"No distinct non-empty values found for field '{field}'."}
                continue
            ans = choose_best_option_tfidf(
                question=question,
                options=options,
                corpus=chunks,
            )
            results[field] = ans["best_option"] if ans['best_score'] > 0.2 else None


        return Response(results, status=status.HTTP_200_OK)



class FlowViewSet(viewsets.ModelViewSet):
    """
    Provides list, retrieve, create, update, partial_update, destroy
    """
    queryset = Flow.objects.all()
    serializer_class = FlowSerializer



class DistinctOptionsAPIView(APIView):
    def get(self, request, pk):
        try:
            data = get_distinct_values_from_target_for_source(
                source_model=UdiFiaWorkflow,
                target_model=Rule,
                pk=pk,
            )
            return Response(data)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
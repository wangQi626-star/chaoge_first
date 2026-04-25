"""
Template views for API endpoints.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ResumeTemplate
from .serializers import ResumeTemplateSerializer, ResumeTemplateListSerializer


class ResumeTemplateViewSet(viewsets.ModelViewSet):
    """简历模板CRUD API"""
    queryset = ResumeTemplate.objects.filter(is_active=True).order_by('id')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return ResumeTemplateListSerializer
        return ResumeTemplateSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ResumeTemplateSerializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def use_template(self, request, pk=None):
        """使用模板，增加使用计数"""
        template = self.get_object()
        template.usage_count += 1
        template.save()
        return Response({'message': '模板使用成功', 'usage_count': template.usage_count})

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """热门模板推荐"""
        templates = ResumeTemplate.objects.filter(is_active=True).order_by('-usage_count')[:10]
        serializer = ResumeTemplateListSerializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """模板统计数据"""
        from django.db.models import Count, Sum

        total = ResumeTemplate.objects.filter(is_active=True).count()
        total_usage = ResumeTemplate.objects.filter(is_active=True).aggregate(Sum('usage_count'))['usage_count__sum'] or 0

        by_category = list(ResumeTemplate.objects.filter(is_active=True).values('category').annotate(count=Count('id')))
        top_templates = list(ResumeTemplate.objects.filter(is_active=True).order_by('-usage_count')[:5].values('id', 'name', 'usage_count'))

        return Response({
            'total': total,
            'total_usage': total_usage,
            'by_category': by_category,
            'top_templates': top_templates
        })

    def perform_create(self, serializer):
        """创建自定义模板"""
        serializer.save(creator=self.request.user, is_custom=True)

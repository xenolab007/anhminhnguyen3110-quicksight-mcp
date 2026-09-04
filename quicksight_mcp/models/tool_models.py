"""Request and Response models for all QuickSight MCP tools"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from enum import Enum


# ============================================================================
# Common Response Models
# ============================================================================

@dataclass
class PaginationInfo:
    """Pagination information for list responses"""
    limit: int
    offset: int
    total: int
    has_more: bool
    next_offset: Optional[int] = None


@dataclass
class ErrorInfo:
    """Error information"""
    message: str
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# ============================================================================
# Analysis Tool Models
# ============================================================================

@dataclass
class ListAnalysesRequest:
    """Request to list analyses"""
    offset: int = 0


@dataclass
class ListAnalysesResponse:
    """Response from list analyses"""
    analyses: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeAnalysisRequest:
    """Request to describe an analysis"""
    analysis_id: str


@dataclass
class DescribeAnalysisResponse:
    """Response from describe analysis"""
    analysis: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeAnalysisDefinitionRequest:
    """Request to describe analysis definition"""
    analysis_id: str
    sheet_index: Optional[int] = None  # If set, return only this sheet (0-based); omit for summary mode


@dataclass
class DescribeAnalysisDefinitionResponse:
    """Response from describe analysis definition"""
    analysis_id: str
    definition: Dict[str, Any]
    errors: List[Dict[str, Any]]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None
    total_sheets: Optional[int] = None
    sheet_summaries: Optional[List[Dict[str, Any]]] = None


@dataclass
class CreateAnalysisRequest:
    """Request to create an analysis"""
    analysis_id: str
    name: str
    definition: Optional[Dict[str, Any]] = None
    source_entity: Optional[Dict[str, Any]] = None
    permissions: Optional[List[Dict[str, str]]] = None
    theme_arn: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


@dataclass
class CreateAnalysisResponse:
    """Response from create analysis"""
    arn: str
    analysis_id: str
    creation_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateAnalysisRequest:
    """Request to update an analysis"""
    analysis_id: str
    name: str
    definition: Optional[Dict[str, Any]] = None
    source_entity: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None


@dataclass
class UpdateAnalysisResponse:
    """Response from update analysis"""
    arn: str
    analysis_id: str
    update_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateAnalysisPermissionsRequest:
    """Request to update analysis permissions"""
    analysis_id: str
    grant_permissions: Optional[List[Dict[str, Any]]] = None
    revoke_permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class UpdateAnalysisPermissionsResponse:
    """Response from update analysis permissions"""
    analysis_arn: str
    analysis_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Dashboard Tool Models
# ============================================================================

@dataclass
class ListDashboardsRequest:
    """Request to list dashboards"""
    offset: int = 0


@dataclass
class ListDashboardsResponse:
    """Response from list dashboards"""
    dashboards: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeDashboardRequest:
    """Request to describe a dashboard"""
    dashboard_id: str


@dataclass
class DescribeDashboardResponse:
    """Response from describe dashboard"""
    dashboard: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeDashboardDefinitionRequest:
    """Request to describe dashboard definition"""
    dashboard_id: str


@dataclass
class DescribeDashboardDefinitionResponse:
    """Response from describe dashboard definition"""
    dashboard_id: str
    definition: Dict[str, Any]
    errors: List[Dict[str, Any]]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class ListDashboardVersionsRequest:
    """Request to list dashboard versions"""
    dashboard_id: str
    offset: int = 0


@dataclass
class ListDashboardVersionsResponse:
    """Response from list dashboard versions"""
    dashboard_id: str
    versions: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateDashboardRequest:
    """Request to create a dashboard"""
    dashboard_id: str
    name: str
    source_entity: Dict[str, Any]
    permissions: Optional[List[Dict[str, Any]]] = None
    version_description: Optional[str] = None
    dashboard_publish_options: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


@dataclass
class CreateDashboardResponse:
    """Response from create dashboard"""
    arn: str
    dashboard_id: str
    version_arn: str
    creation_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDashboardRequest:
    """Request to update a dashboard"""
    dashboard_id: str
    name: str
    source_entity: Dict[str, Any]
    version_description: Optional[str] = None
    dashboard_publish_options: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None


@dataclass
class UpdateDashboardResponse:
    """Response from update dashboard"""
    arn: str
    dashboard_id: str
    version_arn: str
    update_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDashboardPublishedVersionRequest:
    """Request to publish a dashboard version"""
    dashboard_id: str
    version_number: int


@dataclass
class UpdateDashboardPublishedVersionResponse:
    """Response from publish dashboard version"""
    dashboard_id: str
    dashboard_arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDashboardPermissionsRequest:
    """Request to update dashboard permissions"""
    dashboard_id: str
    grant_permissions: Optional[List[Dict[str, Any]]] = None
    revoke_permissions: Optional[List[Dict[str, Any]]] = None
    grant_link_permissions: Optional[List[Dict[str, Any]]] = None
    revoke_link_permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class UpdateDashboardPermissionsResponse:
    """Response from update dashboard permissions"""
    dashboard_arn: str
    dashboard_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Dataset Tool Models
# ============================================================================

@dataclass
class ListDatasetsRequest:
    """Request to list datasets"""
    offset: int = 0


@dataclass
class ListDatasetsResponse:
    """Response from list datasets"""
    datasets: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeDatasetRequest:
    """Request to describe a dataset"""
    dataset_id: str


@dataclass
class DescribeDatasetResponse:
    """Response from describe dataset"""
    dataset: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateDatasetRequest:
    """Request to create a dataset"""
    dataset_id: str
    name: str
    physical_table_map: Dict[str, Any]
    import_mode: str
    logical_table_map: Optional[Dict[str, Any]] = None
    column_groups: Optional[List[Dict[str, Any]]] = None
    field_folders: Optional[Dict[str, Any]] = None
    row_level_permission_data_set: Optional[Dict[str, Any]] = None
    column_level_permission_rules: Optional[List[Dict[str, Any]]] = None
    permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class CreateDatasetResponse:
    """Response from create dataset"""
    arn: str
    dataset_id: str
    ingestion_arn: Optional[str]
    ingestion_id: Optional[str]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDatasetRequest:
    """Request to update a dataset"""
    dataset_id: str
    name: str
    physical_table_map: Dict[str, Any]
    import_mode: str
    logical_table_map: Optional[Dict[str, Any]] = None
    column_groups: Optional[List[Dict[str, Any]]] = None
    field_folders: Optional[Dict[str, Any]] = None
    row_level_permission_data_set: Optional[Dict[str, Any]] = None
    column_level_permission_rules: Optional[List[Dict[str, Any]]] = None


@dataclass
class UpdateDatasetResponse:
    """Response from update dataset"""
    arn: str
    dataset_id: str
    ingestion_arn: Optional[str]
    ingestion_id: Optional[str]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDatasetPermissionsRequest:
    """Request to update dataset permissions"""
    dataset_id: str
    grant_permissions: Optional[List[Dict[str, Any]]] = None
    revoke_permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class UpdateDatasetPermissionsResponse:
    """Response from update dataset permissions"""
    dataset_arn: str
    dataset_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Datasource Tool Models
# ============================================================================

@dataclass
class ListDatasourcesRequest:
    """Request to list datasources"""
    offset: int = 0


@dataclass
class ListDatasourcesResponse:
    """Response from list datasources"""
    datasources: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeDatasourceRequest:
    """Request to describe a datasource"""
    datasource_id: str


@dataclass
class DescribeDatasourceResponse:
    """Response from describe datasource"""
    datasource: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateDatasourceRequest:
    """Request to create a datasource"""
    datasource_id: str
    name: str
    type: str
    data_source_parameters: Dict[str, Any]
    credentials: Optional[Dict[str, Any]] = None
    vpc_connection_properties: Optional[Dict[str, Any]] = None
    ssl_properties: Optional[Dict[str, Any]] = None
    permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class CreateDatasourceResponse:
    """Response from create datasource"""
    arn: str
    datasource_id: str
    creation_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDatasourceRequest:
    """Request to update a datasource"""
    datasource_id: str
    name: str
    data_source_parameters: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    vpc_connection_properties: Optional[Dict[str, Any]] = None
    ssl_properties: Optional[Dict[str, Any]] = None


@dataclass
class UpdateDatasourceResponse:
    """Response from update datasource"""
    arn: str
    datasource_id: str
    update_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateDatasourcePermissionsRequest:
    """Request to update datasource permissions"""
    datasource_id: str
    grant_permissions: Optional[List[Dict[str, Any]]] = None
    revoke_permissions: Optional[List[Dict[str, Any]]] = None


@dataclass
class UpdateDatasourcePermissionsResponse:
    """Response from update datasource permissions"""
    datasource_arn: str
    datasource_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Template Tool Models
# ============================================================================

@dataclass
class ListTemplatesRequest:
    """Request to list templates"""
    offset: int = 0


@dataclass
class ListTemplatesResponse:
    """Response from list templates"""
    templates: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeTemplateRequest:
    """Request to describe a template"""
    template_id: str
    version_number: Optional[int] = None
    alias_name: Optional[str] = None


@dataclass
class DescribeTemplateResponse:
    """Response from describe template"""
    template: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeTemplateDefinitionRequest:
    """Request to describe template definition"""
    template_id: str
    version_number: Optional[int] = None
    alias_name: Optional[str] = None


@dataclass
class DescribeTemplateDefinitionResponse:
    """Response from describe template definition"""
    template_id: str
    definition: Dict[str, Any]
    errors: List[Dict[str, Any]]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateTemplateRequest:
    """Request to create a template"""
    template_id: str
    name: str
    source_entity: Dict[str, Any]
    permissions: Optional[List[Dict[str, Any]]] = None
    version_description: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


@dataclass
class CreateTemplateResponse:
    """Response from create template"""
    arn: str
    template_id: str
    version_arn: str
    creation_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateTemplateRequest:
    """Request to update a template"""
    template_id: str
    source_entity: Dict[str, Any]
    name: Optional[str] = None
    version_description: Optional[str] = None


@dataclass
class UpdateTemplateResponse:
    """Response from update template"""
    arn: str
    template_id: str
    version_arn: str
    update_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Theme Tool Models
# ============================================================================

@dataclass
class ListThemesRequest:
    """Request to list themes"""
    offset: int = 0


@dataclass
class ListThemesResponse:
    """Response from list themes"""
    themes: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeThemeRequest:
    """Request to describe a theme"""
    theme_id: str
    version_number: Optional[int] = None
    alias_name: Optional[str] = None


@dataclass
class DescribeThemeResponse:
    """Response from describe theme"""
    theme: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateThemeRequest:
    """Request to create a theme"""
    theme_id: str
    name: str
    base_theme_id: str
    configuration: Dict[str, Any]
    permissions: Optional[List[Dict[str, Any]]] = None
    version_description: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None


@dataclass
class CreateThemeResponse:
    """Response from create theme"""
    arn: str
    theme_id: str
    version_arn: str
    creation_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateThemeRequest:
    """Request to update a theme"""
    theme_id: str
    base_theme_id: str
    configuration: Dict[str, Any]
    name: Optional[str] = None
    version_description: Optional[str] = None


@dataclass
class UpdateThemeResponse:
    """Response from update theme"""
    arn: str
    theme_id: str
    version_arn: str
    update_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Ingestion Tool Models
# ============================================================================

@dataclass
class CreateIngestionRequest:
    """Request to create an ingestion"""
    dataset_id: str
    ingestion_id: str
    ingestion_type: str = "FULL_REFRESH"


@dataclass
class CreateIngestionResponse:
    """Response from create ingestion"""
    arn: str
    ingestion_id: str
    ingestion_status: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DescribeIngestionRequest:
    """Request to describe an ingestion"""
    dataset_id: str
    ingestion_id: str


@dataclass
class DescribeIngestionResponse:
    """Response from describe ingestion"""
    arn: str
    ingestion_id: str
    ingestion_status: str
    ingestion_type: str
    created_time: str
    ingestion_time_in_seconds: Optional[int]
    ingestion_size_in_bytes: Optional[int]
    row_info: Dict[str, Any]
    error_info: Dict[str, Any]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CancelIngestionRequest:
    """Request to cancel an ingestion"""
    dataset_id: str
    ingestion_id: str


@dataclass
class CancelIngestionResponse:
    """Response from cancel ingestion"""
    arn: str
    ingestion_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class ListRefreshSchedulesRequest:
    """Request to list refresh schedules"""
    dataset_id: str


@dataclass
class ListRefreshSchedulesResponse:
    """Response from list refresh schedules"""
    dataset_id: str
    refresh_schedules: List[Dict[str, Any]]
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class CreateRefreshScheduleRequest:
    """Request to create a refresh schedule"""
    dataset_id: str
    schedule_id: str
    schedule_frequency: Dict[str, Any]
    refresh_type: str = "FULL_REFRESH"


@dataclass
class CreateRefreshScheduleResponse:
    """Response from create refresh schedule"""
    arn: str
    schedule_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class UpdateRefreshScheduleRequest:
    """Request to update a refresh schedule"""
    dataset_id: str
    schedule_id: str
    schedule_frequency: Dict[str, Any]
    refresh_type: str = "FULL_REFRESH"


@dataclass
class UpdateRefreshScheduleResponse:
    """Response from update refresh schedule"""
    arn: str
    schedule_id: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Embed Tool Models
# ============================================================================

@dataclass
class GenerateEmbedUrlForAnonymousUserRequest:
    """Request to generate embed URL for anonymous user"""
    namespace: str
    authorized_resource_arns: List[str]
    experience_configuration: Dict[str, Any]
    session_lifetime_in_minutes: int = 600
    allowed_domains: Optional[List[str]] = None
    session_tags: Optional[List[Dict[str, str]]] = None


@dataclass
class GenerateEmbedUrlForAnonymousUserResponse:
    """Response from generate embed URL for anonymous user"""
    embed_url: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class GenerateEmbedUrlForRegisteredUserRequest:
    """Request to generate embed URL for registered user"""
    user_arn: str
    experience_configuration: Dict[str, Any]
    session_lifetime_in_minutes: int = 600
    allowed_domains: Optional[List[str]] = None


@dataclass
class GenerateEmbedUrlForRegisteredUserResponse:
    """Response from generate embed URL for registered user"""
    embed_url: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Search Tool Models
# ============================================================================

@dataclass
class SearchDashboardsRequest:
    """Request to search dashboards"""
    filters: List[Dict[str, Any]]
    offset: int = 0


@dataclass
class SearchDashboardsResponse:
    """Response from search dashboards"""
    dashboards: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class SearchAnalysesRequest:
    """Request to search analyses"""
    filters: List[Dict[str, Any]]
    offset: int = 0


@dataclass
class SearchAnalysesResponse:
    """Response from search analyses"""
    analyses: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class SearchDatasetsRequest:
    """Request to search datasets"""
    filters: List[Dict[str, Any]]
    offset: int = 0


@dataclass
class SearchDatasetsResponse:
    """Response from search datasets"""
    datasets: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class SearchDatasourcesRequest:
    """Request to search datasources"""
    filters: List[Dict[str, Any]]
    offset: int = 0


@dataclass
class SearchDatasourcesResponse:
    """Response from search datasources"""
    datasources: List[Dict[str, Any]]
    pagination: PaginationInfo
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


# ============================================================================
# Delete Tool Models
# ============================================================================

@dataclass
class DeleteAnalysisRequest:
    """Request to delete an analysis"""
    analysis_id: str
    recovery_window_in_days: Optional[int] = 30
    force_delete_without_recovery: bool = False


@dataclass
class DeleteAnalysisResponse:
    """Response from delete analysis"""
    analysis_id: str
    arn: str
    deletion_time: Optional[str] = None
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class RestoreAnalysisRequest:
    """Request to restore an analysis that is pending deletion"""
    analysis_id: str


@dataclass
class RestoreAnalysisResponse:
    """Response from restore analysis"""
    analysis_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteDashboardRequest:
    """Request to delete a dashboard"""
    dashboard_id: str
    version_number: Optional[int] = None


@dataclass
class DeleteDashboardResponse:
    """Response from delete dashboard"""
    dashboard_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteDatasetRequest:
    """Request to delete a dataset"""
    dataset_id: str


@dataclass
class DeleteDatasetResponse:
    """Response from delete dataset"""
    dataset_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteDatasourceRequest:
    """Request to delete a datasource"""
    datasource_id: str


@dataclass
class DeleteDatasourceResponse:
    """Response from delete datasource"""
    datasource_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteTemplateRequest:
    """Request to delete a template"""
    template_id: str
    version_number: Optional[int] = None


@dataclass
class DeleteTemplateResponse:
    """Response from delete template"""
    template_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteThemeRequest:
    """Request to delete a theme"""
    theme_id: str
    version_number: Optional[int] = None


@dataclass
class DeleteThemeResponse:
    """Response from delete theme"""
    theme_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None


@dataclass
class DeleteRefreshScheduleRequest:
    """Request to delete a dataset refresh schedule"""
    dataset_id: str
    schedule_id: str


@dataclass
class DeleteRefreshScheduleResponse:
    """Response from delete refresh schedule"""
    dataset_id: str
    schedule_id: str
    arn: str
    status: str = "SUCCESS"
    error: Optional[ErrorInfo] = None

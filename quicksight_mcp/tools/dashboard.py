"""Dashboard management tools for creating and publishing QuickSight dashboards"""

import logging
from quicksight_mcp.services.dashboard import DashboardService
from quicksight_mcp.models.tool_models import (
    ListDashboardsRequest, ListDashboardsResponse,
    DescribeDashboardRequest, DescribeDashboardResponse,
    DescribeDashboardDefinitionRequest, DescribeDashboardDefinitionResponse,
    ListDashboardVersionsRequest, ListDashboardVersionsResponse,
    CreateDashboardRequest, CreateDashboardResponse,
    UpdateDashboardRequest, UpdateDashboardResponse,
    UpdateDashboardPublishedVersionRequest, UpdateDashboardPublishedVersionResponse,
    UpdateDashboardPermissionsRequest, UpdateDashboardPermissionsResponse,
    PaginationInfo, ErrorInfo,
    DeleteDashboardRequest, DeleteDashboardResponse,
)

logger = logging.getLogger(__name__)


def register_dashboard_tools(mcp):
    """Register all dashboard management tools with the MCP server"""
    
    @mcp.tool(
        name="list_dashboards",
        description="List dashboards in the QuickSight account with pagination (limit 10)"
    )
    async def list_dashboards(request: ListDashboardsRequest) -> ListDashboardsResponse:
        """List dashboards with pagination"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            all_dashboards = service.list_dashboards()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated_dashboards = all_dashboards[start_idx:end_idx]
            
            has_more = end_idx < len(all_dashboards)
            next_offset = end_idx if has_more else None
            
            pagination = PaginationInfo(
                limit=limit,
                offset=request.offset,
                total=len(all_dashboards),
                has_more=has_more,
                next_offset=next_offset
            )
            
            return ListDashboardsResponse(
                dashboards=paginated_dashboards,
                pagination=pagination,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error listing dashboards: {str(e)}")
            return ListDashboardsResponse(
                dashboards=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_dashboard",
        description="Get detailed information about a specific dashboard"
    )
    async def describe_dashboard(request: DescribeDashboardRequest) -> DescribeDashboardResponse:
        """Get dashboard details"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            dashboard = service.describe_dashboard(request.dashboard_id)
            
            return DescribeDashboardResponse(
                dashboard=dashboard,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing dashboard: {str(e)}")
            return DescribeDashboardResponse(
                dashboard={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_dashboard_definition",
        description="Get the definition (structure) of a dashboard"
    )
    async def describe_dashboard_definition(request: DescribeDashboardDefinitionRequest) -> DescribeDashboardDefinitionResponse:
        """Get dashboard definition with full structure"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.describe_dashboard_definition(dashboard_id=request.dashboard_id)
            
            logger.info(f"Retrieved dashboard definition for {request.dashboard_id}")
            
            return DescribeDashboardDefinitionResponse(
                dashboard_id=response.get('DashboardId', request.dashboard_id),
                definition=response.get('Definition', {}),
                errors=response.get('Errors', []),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing dashboard definition: {str(e)}")
            return DescribeDashboardDefinitionResponse(
                dashboard_id=request.dashboard_id,
                definition={},
                errors=[],
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="list_dashboard_versions",
        description="List all versions of a specific dashboard"
    )
    async def list_dashboard_versions(request: ListDashboardVersionsRequest) -> ListDashboardVersionsResponse:
        """List all versions of a dashboard"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            versions = service.list_dashboard_versions(dashboard_id=request.dashboard_id)
            
            logger.info(f"Found {len(versions)} versions for dashboard {request.dashboard_id}")
            
            return ListDashboardVersionsResponse(
                dashboard_id=request.dashboard_id,
                versions=versions,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error listing dashboard versions: {str(e)}")
            return ListDashboardVersionsResponse(
                dashboard_id=request.dashboard_id,
                versions=[],
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_dashboard",
        description="Create a new QuickSight dashboard"
    )
    async def create_dashboard(request: CreateDashboardRequest) -> CreateDashboardResponse:
        """Create a new dashboard in QuickSight"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.create_dashboard(
                dashboard_id=request.dashboard_id,
                name=request.name,
                source_entity=request.source_entity,
                permissions=request.permissions,
                version_description=request.version_description,
                dashboard_publish_options=request.dashboard_publish_options,
                theme_arn=request.theme_arn,
                tags=request.tags
            )
            
            logger.info(f"Created dashboard: {request.dashboard_id}")
            
            return CreateDashboardResponse(
                arn=response['Arn'],
                dashboard_id=response['DashboardId'],
                version_arn=response.get('VersionArn', ''),
                creation_status=response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating dashboard {request.dashboard_id}: {str(e)}")
            return CreateDashboardResponse(
                arn="",
                dashboard_id=request.dashboard_id,
                version_arn="",
                creation_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_dashboard",
        description="Update an existing QuickSight dashboard"
    )
    async def update_dashboard(request: UpdateDashboardRequest) -> UpdateDashboardResponse:
        """Update an existing dashboard"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_dashboard(
                dashboard_id=request.dashboard_id,
                name=request.name,
                source_entity=request.source_entity,
                version_description=request.version_description,
                dashboard_publish_options=request.dashboard_publish_options,
                theme_arn=request.theme_arn
            )
            
            logger.info(f"Updated dashboard: {request.dashboard_id}")
            
            return UpdateDashboardResponse(
                arn=response['Arn'],
                dashboard_id=response['DashboardId'],
                version_arn=response.get('VersionArn', ''),
                update_status=response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating dashboard {request.dashboard_id}: {str(e)}")
            return UpdateDashboardResponse(
                arn="",
                dashboard_id=request.dashboard_id,
                version_arn="",
                update_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_dashboard_published_version",
        description="Publish a specific version of a dashboard"
    )
    async def update_dashboard_published_version(request: UpdateDashboardPublishedVersionRequest) -> UpdateDashboardPublishedVersionResponse:
        """Publish a specific dashboard version"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_dashboard_published_version(
                dashboard_id=request.dashboard_id,
                version_number=request.version_number
            )
            
            logger.info(f"Published dashboard {request.dashboard_id} version {request.version_number}")
            
            return UpdateDashboardPublishedVersionResponse(
                dashboard_id=response['DashboardId'],
                dashboard_arn=response['DashboardArn'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error publishing dashboard {request.dashboard_id}: {str(e)}")
            return UpdateDashboardPublishedVersionResponse(
                dashboard_id=request.dashboard_id,
                dashboard_arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_dashboard_permissions",
        description="Update permissions for a QuickSight dashboard"
    )
    async def update_dashboard_permissions(request: UpdateDashboardPermissionsRequest) -> UpdateDashboardPermissionsResponse:
        """Update permissions for a dashboard"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_permissions(
                dashboard_id=request.dashboard_id,
                grant_permissions=request.grant_permissions,
                revoke_permissions=request.revoke_permissions,
                grant_link_permissions=request.grant_link_permissions,
                revoke_link_permissions=request.revoke_link_permissions
            )
            
            logger.info(f"Updated permissions for dashboard: {request.dashboard_id}")
            
            return UpdateDashboardPermissionsResponse(
                dashboard_arn=response['DashboardArn'],
                dashboard_id=response['DashboardId'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating dashboard permissions {request.dashboard_id}: {str(e)}")
            return UpdateDashboardPermissionsResponse(
                dashboard_arn="",
                dashboard_id=request.dashboard_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_dashboard",
        description=(
            "Permanently delete a dashboard. Pass version_number to delete only that one "
            "version instead of the whole dashboard. This cannot be undone."
        )
    )
    async def delete_dashboard(request: DeleteDashboardRequest) -> DeleteDashboardResponse:
        """Delete a dashboard or one of its versions"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.delete_dashboard(
                dashboard_id=request.dashboard_id,
                version_number=request.version_number
            )

            return DeleteDashboardResponse(
                dashboard_id=response.get('DashboardId', request.dashboard_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting dashboard: {str(e)}")
            return DeleteDashboardResponse(
                dashboard_id=request.dashboard_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )

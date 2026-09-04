"""Data source management tools for creating and updating QuickSight data sources"""

import logging
from quicksight_mcp.services.datasource import DatasourceService
from quicksight_mcp.models.tool_models import (
    ListDatasourcesRequest, ListDatasourcesResponse,
    DescribeDatasourceRequest, DescribeDatasourceResponse,
    CreateDatasourceRequest, CreateDatasourceResponse,
    UpdateDatasourceRequest, UpdateDatasourceResponse,
    UpdateDatasourcePermissionsRequest, UpdateDatasourcePermissionsResponse,
    PaginationInfo, ErrorInfo,
    DeleteDatasourceRequest, DeleteDatasourceResponse,
)

logger = logging.getLogger(__name__)


def register_datasource_tools(mcp):
    """Register all data source management tools with the MCP server"""
    
    @mcp.tool(
        name="list_datasources",
        description="List all data sources in the QuickSight account"
    )
    async def list_datasources(request: ListDatasourcesRequest) -> ListDatasourcesResponse:
        """List all data sources with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            all_datasources = service.list_datasources()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_datasources[start_idx:end_idx]
            
            # Format datasources
            formatted_datasources = [
                {'DataSourceId': d['DataSourceId'], 'Name': d['Name']}
                for d in paginated
            ]
            
            return ListDatasourcesResponse(
                datasources=formatted_datasources,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_datasources),
                    has_more=end_idx < len(all_datasources),
                    next_offset=end_idx if end_idx < len(all_datasources) else None
                ),
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error listing datasources: {str(e)}")
            return ListDatasourcesResponse(
                datasources=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_datasource",
        description="Get detailed information about a specific data source"
    )
    async def describe_datasource(request: DescribeDatasourceRequest) -> DescribeDatasourceResponse:
        """
        Get data source details including connection parameters
        
        Args:
            request: Request with datasource_id
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            datasource = service.describe_datasource(request.datasource_id)
            return DescribeDatasourceResponse(
                datasource=datasource,
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error describing datasource {request.datasource_id}: {str(e)}")
            return DescribeDatasourceResponse(
                datasource={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_data_source",
        description="Create a new QuickSight data source"
    )
    async def create_data_source(request: CreateDatasourceRequest) -> CreateDatasourceResponse:
        """
        Create a new data source in QuickSight
        
        Args:
            request: CreateDatasourceRequest with all data source configuration
            
        Returns:
            CreateDatasourceResponse with creation status and data source ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            response = service.create_datasource(
                datasource_id=request.datasource_id,
                name=request.name,
                type=request.type,
                data_source_parameters=request.data_source_parameters,
                credentials=request.credentials,
                vpc_connection_properties=request.vpc_connection_properties,
                ssl_properties=request.ssl_properties,
                permissions=request.permissions
            )
            
            logger.info(f"Created data source: {request.datasource_id}")
            
            return CreateDatasourceResponse(
                arn=response['Arn'],
                datasource_id=response['DataSourceId'],
                creation_status=response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating data source {request.datasource_id}: {str(e)}")
            return CreateDatasourceResponse(
                arn="",
                datasource_id=request.datasource_id,
                creation_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_data_source",
        description="Update an existing QuickSight data source"
    )
    async def update_data_source(request: UpdateDatasourceRequest) -> UpdateDatasourceResponse:
        """
        Update an existing data source configuration
        
        Args:
            request: UpdateDatasourceRequest with updated configuration
            
        Returns:
            UpdateDatasourceResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            response = service.update_datasource(
                datasource_id=request.datasource_id,
                name=request.name,
                data_source_parameters=request.data_source_parameters,
                credentials=request.credentials,
                vpc_connection_properties=request.vpc_connection_properties,
                ssl_properties=request.ssl_properties
            )
            
            logger.info(f"Updated data source: {request.datasource_id}")
            
            return UpdateDatasourceResponse(
                arn=response['Arn'],
                datasource_id=response['DataSourceId'],
                update_status=response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating data source {request.datasource_id}: {str(e)}")
            return UpdateDatasourceResponse(
                arn="",
                datasource_id=request.datasource_id,
                update_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_data_source_permissions",
        description="Update permissions for a QuickSight data source"
    )
    async def update_data_source_permissions(request: UpdateDatasourcePermissionsRequest) -> UpdateDatasourcePermissionsResponse:
        """
        Update permissions for a data source
        
        Args:
            request: UpdateDatasourcePermissionsRequest with permission changes
            
        Returns:
            UpdateDatasourcePermissionsResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            response = service.update_permissions(
                datasource_id=request.datasource_id,
                grant_permissions=request.grant_permissions,
                revoke_permissions=request.revoke_permissions
            )
            
            logger.info(f"Updated permissions for data source: {request.datasource_id}")
            
            return UpdateDatasourcePermissionsResponse(
                datasource_arn=response['DataSourceArn'],
                datasource_id=response['DataSourceId'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating data source permissions {request.datasource_id}: {str(e)}")
            return UpdateDatasourcePermissionsResponse(
                datasource_arn="",
                datasource_id=request.datasource_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_data_source",
        description="Permanently delete a data source. This cannot be undone, and any dataset built on it will break."
    )
    async def delete_data_source(request: DeleteDatasourceRequest) -> DeleteDatasourceResponse:
        """Delete a data source"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = DatasourceService(quicksight, config.aws_account_id)
            response = service.delete_datasource(datasource_id=request.datasource_id)

            return DeleteDatasourceResponse(
                datasource_id=response.get('DataSourceId', request.datasource_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting data source: {str(e)}")
            return DeleteDatasourceResponse(
                datasource_id=request.datasource_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )

"""Dataset management tools for creating and updating QuickSight datasets"""

import logging
from quicksight_mcp.services.dataset import DatasetService
from quicksight_mcp.models.tool_models import (
    ListDatasetsRequest, ListDatasetsResponse,
    DescribeDatasetRequest, DescribeDatasetResponse,
    CreateDatasetRequest, CreateDatasetResponse,
    UpdateDatasetRequest, UpdateDatasetResponse,
    UpdateDatasetPermissionsRequest, UpdateDatasetPermissionsResponse,
    PaginationInfo, ErrorInfo,
    DeleteDatasetRequest, DeleteDatasetResponse,
)

logger = logging.getLogger(__name__)


def register_dataset_tools(mcp):
    """Register all dataset management tools with the MCP server"""
    
    @mcp.tool(
        name="list_datasets",
        description="List all datasets in the QuickSight account"
    )
    async def list_datasets(request: ListDatasetsRequest) -> ListDatasetsResponse:
        """List all datasets with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasetService(quicksight, config.aws_account_id)
            all_datasets = service.list_datasets()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_datasets[start_idx:end_idx]
            
            # Format datasets
            formatted_datasets = [
                {'DataSetId': d['DataSetId'], 'Name': d['Name']}
                for d in paginated
            ]
            
            return ListDatasetsResponse(
                datasets=formatted_datasets,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_datasets),
                    has_more=end_idx < len(all_datasets),
                    next_offset=end_idx if end_idx < len(all_datasets) else None
                ),
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error listing datasets: {str(e)}")
            return ListDatasetsResponse(
                datasets=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_dataset",
        description="Get detailed information about a specific dataset"
    )
    async def describe_dataset(request: DescribeDatasetRequest) -> DescribeDatasetResponse:
        """
        Get dataset details including schema, tables, and columns
        
        Args:
            request: Request with dataset_id
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasetService(quicksight, config.aws_account_id)
            dataset = service.describe_dataset(request.dataset_id)
            return DescribeDatasetResponse(
                dataset=dataset,
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error describing dataset {request.dataset_id}: {str(e)}")
            return DescribeDatasetResponse(
                dataset={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_data_set",
        description="Create a new QuickSight dataset"
    )
    async def create_data_set(request: CreateDatasetRequest) -> CreateDatasetResponse:
        """
        Create a new dataset in QuickSight
        
        Args:
            request: CreateDatasetRequest with all dataset configuration
            
        Returns:
            CreateDatasetResponse with creation status and dataset ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasetService(quicksight, config.aws_account_id)
            response = service.create_dataset(
                dataset_id=request.dataset_id,
                name=request.name,
                physical_table_map=request.physical_table_map,
                import_mode=request.import_mode,
                logical_table_map=request.logical_table_map,
                column_groups=request.column_groups,
                field_folders=request.field_folders,
                row_level_permission_data_set=request.row_level_permission_data_set,
                column_level_permission_rules=request.column_level_permission_rules,
                permissions=request.permissions
            )
            
            logger.info(f"Created dataset: {request.dataset_id}")
            
            return CreateDatasetResponse(
                arn=response['Arn'],
                dataset_id=response['DataSetId'],
                ingestion_arn=response.get('IngestionArn'),
                ingestion_id=response.get('IngestionId'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating dataset {request.dataset_id}: {str(e)}")
            return CreateDatasetResponse(
                arn="",
                dataset_id=request.dataset_id,
                ingestion_arn=None,
                ingestion_id=None,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_data_set",
        description="Update an existing QuickSight dataset"
    )
    async def update_data_set(request: UpdateDatasetRequest) -> UpdateDatasetResponse:
        """
        Update an existing dataset configuration
        
        Args:
            request: UpdateDatasetRequest with updated configuration
            
        Returns:
            UpdateDatasetResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasetService(quicksight, config.aws_account_id)
            response = service.update_dataset(
                dataset_id=request.dataset_id,
                name=request.name,
                physical_table_map=request.physical_table_map,
                import_mode=request.import_mode,
                logical_table_map=request.logical_table_map,
                column_groups=request.column_groups,
                field_folders=request.field_folders,
                row_level_permission_data_set=request.row_level_permission_data_set,
                column_level_permission_rules=request.column_level_permission_rules
            )
            
            logger.info(f"Updated dataset: {request.dataset_id}")
            
            return UpdateDatasetResponse(
                arn=response['Arn'],
                dataset_id=response['DataSetId'],
                ingestion_arn=response.get('IngestionArn'),
                ingestion_id=response.get('IngestionId'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating dataset {request.dataset_id}: {str(e)}")
            return UpdateDatasetResponse(
                arn="",
                dataset_id=request.dataset_id,
                ingestion_arn=None,
                ingestion_id=None,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_data_set_permissions",
        description="Update permissions for a QuickSight dataset"
    )
    async def update_data_set_permissions(request: UpdateDatasetPermissionsRequest) -> UpdateDatasetPermissionsResponse:
        """
        Update permissions for a dataset
        
        Args:
            request: UpdateDatasetPermissionsRequest with permission changes
            
        Returns:
            UpdateDatasetPermissionsResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DatasetService(quicksight, config.aws_account_id)
            response = service.update_permissions(
                dataset_id=request.dataset_id,
                grant_permissions=request.grant_permissions,
                revoke_permissions=request.revoke_permissions
            )
            
            logger.info(f"Updated permissions for dataset: {request.dataset_id}")
            
            return UpdateDatasetPermissionsResponse(
                dataset_arn=response['DataSetArn'],
                dataset_id=response['DataSetId'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating dataset permissions {request.dataset_id}: {str(e)}")
            return UpdateDatasetPermissionsResponse(
                dataset_arn="",
                dataset_id=request.dataset_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_data_set",
        description="Permanently delete a dataset. This cannot be undone, and any analysis or dashboard built on it will break."
    )
    async def delete_data_set(request: DeleteDatasetRequest) -> DeleteDatasetResponse:
        """Delete a dataset"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = DatasetService(quicksight, config.aws_account_id)
            response = service.delete_dataset(dataset_id=request.dataset_id)

            return DeleteDatasetResponse(
                dataset_id=response.get('DataSetId', request.dataset_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting dataset: {str(e)}")
            return DeleteDatasetResponse(
                dataset_id=request.dataset_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )

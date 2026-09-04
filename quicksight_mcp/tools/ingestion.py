"""Data ingestion and refresh schedule tools for QuickSight SPICE datasets"""

import logging
from typing import Dict, Any
from quicksight_mcp.services.ingestion import IngestionService
from quicksight_mcp.models.tool_models import (
    CreateIngestionRequest, CreateIngestionResponse,
    DescribeIngestionRequest, DescribeIngestionResponse,
    CancelIngestionRequest, CancelIngestionResponse,
    ListRefreshSchedulesRequest, ListRefreshSchedulesResponse,
    CreateRefreshScheduleRequest, CreateRefreshScheduleResponse,
    UpdateRefreshScheduleRequest, UpdateRefreshScheduleResponse,
    ErrorInfo,
    DeleteRefreshScheduleRequest, DeleteRefreshScheduleResponse,
)

logger = logging.getLogger(__name__)


def register_ingestion_tools(mcp):
    """Register all data ingestion and refresh schedule tools with the MCP server"""
    
    @mcp.tool(
        name="create_ingestion",
        description="Create a data ingestion job for a SPICE dataset"
    )
    async def create_ingestion(request: CreateIngestionRequest) -> CreateIngestionResponse:
        """
        Create a data ingestion job to load data into SPICE
        
        Args:
            request: CreateIngestionRequest with ingestion configuration
            
        Returns:
            CreateIngestionResponse with ingestion status and ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.create_ingestion(
                dataset_id=request.dataset_id,
                ingestion_id=request.ingestion_id,
                ingestion_type=request.ingestion_type
            )
            
            logger.info(f"Created ingestion {request.ingestion_id} for dataset {request.dataset_id}")
            
            return CreateIngestionResponse(
                arn=response['Arn'],
                ingestion_id=response.get('IngestionId', request.ingestion_id),
                ingestion_status=response.get('IngestionStatus', 'INITIALIZED'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating ingestion {request.ingestion_id}: {str(e)}")
            return CreateIngestionResponse(
                arn="",
                ingestion_id=request.ingestion_id,
                ingestion_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_ingestion",
        description="Get details about a data ingestion job"
    )
    async def describe_ingestion(request: DescribeIngestionRequest) -> DescribeIngestionResponse:
        """
        Get status and details of an ingestion job
        
        Args:
            request: DescribeIngestionRequest with dataset_id and ingestion_id
            
        Returns:
            DescribeIngestionResponse with ingestion details and status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.describe_ingestion(
                dataset_id=request.dataset_id,
                ingestion_id=request.ingestion_id
            )
            
            ingestion = response.get('Ingestion', {})
            
            return DescribeIngestionResponse(
                arn=ingestion.get('Arn', ''),
                ingestion_id=ingestion.get('IngestionId', request.ingestion_id),
                ingestion_status=ingestion.get('IngestionStatus', 'UNKNOWN'),
                ingestion_type=ingestion.get('IngestionType', ''),
                created_time=str(ingestion.get('CreatedTime', '')),
                ingestion_time_in_seconds=ingestion.get('IngestionTimeInSeconds'),
                ingestion_size_in_bytes=ingestion.get('IngestionSizeInBytes'),
                row_info=ingestion.get('RowInfo', {}),
                error_info=ingestion.get('ErrorInfo', {}),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing ingestion {request.ingestion_id}: {str(e)}")
            return DescribeIngestionResponse(
                arn="",
                ingestion_id=request.ingestion_id,
                ingestion_status="FAILED",
                ingestion_type="",
                created_time="",
                ingestion_time_in_seconds=None,
                ingestion_size_in_bytes=None,
                row_info={},
                error_info={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="cancel_ingestion",
        description="Cancel a running data ingestion job"
    )
    async def cancel_ingestion(request: CancelIngestionRequest) -> CancelIngestionResponse:
        """
        Cancel a running ingestion job
        
        Args:
            request: CancelIngestionRequest with dataset_id and ingestion_id
            
        Returns:
            CancelIngestionResponse with cancellation status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.cancel_ingestion(
                dataset_id=request.dataset_id,
                ingestion_id=request.ingestion_id
            )
            
            logger.info(f"Cancelled ingestion {request.ingestion_id}")
            
            return CancelIngestionResponse(
                arn=response.get('Arn', ''),
                ingestion_id=response.get('IngestionId', request.ingestion_id),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error cancelling ingestion {request.ingestion_id}: {str(e)}")
            return CancelIngestionResponse(
                arn="",
                ingestion_id=request.ingestion_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="list_refresh_schedules",
        description="List all refresh schedules for a dataset"
    )
    async def list_refresh_schedules(request: ListRefreshSchedulesRequest) -> ListRefreshSchedulesResponse:
        """
        List all refresh schedules configured for a dataset
        
        Args:
            request: ListRefreshSchedulesRequest with dataset_id
            
        Returns:
            ListRefreshSchedulesResponse with list of refresh schedules
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            schedules = service.list_refresh_schedules(dataset_id=request.dataset_id)
            
            formatted_schedules = [
                {
                    'ScheduleId': s.get('ScheduleId'),
                    'ScheduleFrequency': s.get('ScheduleFrequency', {}),
                    'StartAfterDateTime': str(s.get('StartAfterDateTime', '')),
                    'RefreshType': s.get('RefreshType'),
                    'Arn': s.get('Arn')
                }
                for s in schedules
            ]
            
            return ListRefreshSchedulesResponse(
                dataset_id=request.dataset_id,
                refresh_schedules=formatted_schedules,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error listing refresh schedules for {request.dataset_id}: {str(e)}")
            return ListRefreshSchedulesResponse(
                dataset_id=request.dataset_id,
                refresh_schedules=[],
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_refresh_schedule",
        description="Create a new refresh schedule for a dataset"
    )
    async def create_refresh_schedule(request: CreateRefreshScheduleRequest) -> CreateRefreshScheduleResponse:
        """
        Create a refresh schedule for automatic data updates
        
        Args:
            request: CreateRefreshScheduleRequest with schedule configuration
            
        Returns:
            CreateRefreshScheduleResponse with creation status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.create_refresh_schedule(
                dataset_id=request.dataset_id,
                schedule_id=request.schedule_id,
                schedule_frequency=request.schedule_frequency,
                refresh_type=request.refresh_type
            )
            
            logger.info(f"Created refresh schedule {request.schedule_id} for dataset {request.dataset_id}")
            
            return CreateRefreshScheduleResponse(
                arn=response.get('Arn', ''),
                schedule_id=request.schedule_id,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating refresh schedule {request.schedule_id}: {str(e)}")
            return CreateRefreshScheduleResponse(
                arn="",
                schedule_id=request.schedule_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_refresh_schedule",
        description="Update an existing refresh schedule"
    )
    async def update_refresh_schedule(request: UpdateRefreshScheduleRequest) -> UpdateRefreshScheduleResponse:
        """
        Update an existing refresh schedule
        
        Args:
            request: UpdateRefreshScheduleRequest with updated schedule configuration
            
        Returns:
            UpdateRefreshScheduleResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.update_refresh_schedule(
                dataset_id=request.dataset_id,
                schedule_id=request.schedule_id,
                schedule_frequency=request.schedule_frequency,
                refresh_type=request.refresh_type
            )
            
            logger.info(f"Updated refresh schedule {request.schedule_id}")
            
            return UpdateRefreshScheduleResponse(
                arn=response.get('Arn', ''),
                schedule_id=request.schedule_id,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating refresh schedule {request.schedule_id}: {str(e)}")
            return UpdateRefreshScheduleResponse(
                arn="",
                schedule_id=request.schedule_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_refresh_schedule",
        description="Permanently delete a refresh schedule from a dataset. This cannot be undone."
    )
    async def delete_refresh_schedule(request: DeleteRefreshScheduleRequest) -> DeleteRefreshScheduleResponse:
        """Delete a dataset refresh schedule"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.delete_refresh_schedule(
                dataset_id=request.dataset_id,
                schedule_id=request.schedule_id
            )

            return DeleteRefreshScheduleResponse(
                dataset_id=request.dataset_id,
                schedule_id=response.get('ScheduleId', request.schedule_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting refresh schedule: {str(e)}")
            return DeleteRefreshScheduleResponse(
                dataset_id=request.dataset_id,
                schedule_id=request.schedule_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )

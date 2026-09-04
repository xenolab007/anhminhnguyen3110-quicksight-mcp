"""Ingestion service for QuickSight data ingestion and refresh operations"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class IngestionService:
    """Service for managing QuickSight data ingestion and refresh schedules"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize ingestion service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def create_ingestion(
        self,
        dataset_id: str,
        ingestion_id: str,
        ingestion_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """Create a data ingestion job"""
        try:
            response = self.client.create_ingestion(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                IngestionId=ingestion_id,
                IngestionType=ingestion_type
            )
            logger.info(f"Created ingestion {ingestion_id} for dataset {dataset_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating ingestion {ingestion_id}: {str(e)}")
            raise
    
    def describe_ingestion(self, dataset_id: str, ingestion_id: str) -> Dict[str, Any]:
        """Get status and details of an ingestion job"""
        try:
            response = self.client.describe_ingestion(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                IngestionId=ingestion_id
            )
            return response.get('Ingestion', {})
            
        except Exception as e:
            logger.error(f"Error describing ingestion {ingestion_id}: {str(e)}")
            raise
    
    def cancel_ingestion(self, dataset_id: str, ingestion_id: str) -> Dict[str, Any]:
        """Cancel a running ingestion job"""
        try:
            response = self.client.cancel_ingestion(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                IngestionId=ingestion_id
            )
            logger.info(f"Cancelled ingestion {ingestion_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error cancelling ingestion {ingestion_id}: {str(e)}")
            raise
    
    def list_refresh_schedules(self, dataset_id: str) -> List[Dict[str, Any]]:
        """List all refresh schedules for a dataset"""
        try:
            response = self.client.list_refresh_schedules(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id
            )
            schedules = response.get('RefreshSchedules', [])
            logger.info(f"Found {len(schedules)} refresh schedules for dataset {dataset_id}")
            return schedules
            
        except Exception as e:
            logger.error(f"Error listing refresh schedules for {dataset_id}: {str(e)}")
            raise
    
    def create_refresh_schedule(
        self,
        dataset_id: str,
        schedule_id: str,
        schedule_frequency: Dict[str, Any],
        refresh_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """Create a refresh schedule for automatic data updates"""
        try:
            response = self.client.create_refresh_schedule(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                Schedule={
                    'ScheduleId': schedule_id,
                    'ScheduleFrequency': schedule_frequency,
                    'RefreshType': refresh_type
                }
            )
            logger.info(f"Created refresh schedule {schedule_id} for dataset {dataset_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating refresh schedule {schedule_id}: {str(e)}")
            raise
    
    def update_refresh_schedule(
        self,
        dataset_id: str,
        schedule_id: str,
        schedule_frequency: Dict[str, Any],
        refresh_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """Update an existing refresh schedule"""
        try:
            response = self.client.update_refresh_schedule(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                Schedule={
                    'ScheduleId': schedule_id,
                    'ScheduleFrequency': schedule_frequency,
                    'RefreshType': refresh_type
                }
            )
            logger.info(f"Updated refresh schedule {schedule_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating refresh schedule {schedule_id}: {str(e)}")
            raise

    def delete_refresh_schedule(self, dataset_id: str, schedule_id: str) -> Dict[str, Any]:
        """Delete a refresh schedule from a dataset"""
        try:
            response = self.client.delete_refresh_schedule(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id,
                ScheduleId=schedule_id
            )
            logger.info(f"Deleted refresh schedule {schedule_id} on dataset {dataset_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting refresh schedule {schedule_id}: {str(e)}")
            raise

"""Dataset service for QuickSight dataset operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class DatasetService:
    """Service for managing QuickSight datasets"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize dataset service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_datasets(self) -> List[Dict[str, Any]]:
        """List all datasets in the account"""
        try:
            datasets = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_data_sets(**params)
                datasets.extend(response.get('DataSetSummaries', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasets)} datasets")
            return datasets
            
        except Exception as e:
            logger.error(f"Error listing datasets: {str(e)}")
            raise
    
    def describe_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Get detailed information about a dataset"""
        try:
            response = self.client.describe_data_set(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id
            )
            return response.get('DataSet', {})
            
        except Exception as e:
            logger.error(f"Error describing dataset {dataset_id}: {str(e)}")
            raise
    
    def create_dataset(
        self,
        dataset_id: str,
        name: str,
        physical_table_map: Dict[str, Any],
        logical_table_map: Optional[Dict[str, Any]] = None,
        import_mode: str = "SPICE",
        column_groups: Optional[List[Dict]] = None,
        field_folders: Optional[Dict] = None,
        row_level_security: Optional[Dict] = None,
        column_level_security: Optional[Dict] = None,
        permissions: Optional[List[Dict]] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create a new dataset"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSetId': dataset_id,
                'Name': name,
                'PhysicalTableMap': physical_table_map,
                'ImportMode': import_mode
            }
            
            if logical_table_map:
                params['LogicalTableMap'] = logical_table_map
            if column_groups:
                params['ColumnGroups'] = column_groups
            if field_folders:
                params['FieldFolders'] = field_folders
            if row_level_security:
                params['RowLevelPermissionDataSet'] = row_level_security
            if column_level_security:
                params['ColumnLevelPermissionRules'] = column_level_security
            if permissions:
                params['Permissions'] = permissions
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_data_set(**params)
            logger.info(f"Created dataset: {dataset_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating dataset {dataset_id}: {str(e)}")
            raise
    
    def update_dataset(
        self,
        dataset_id: str,
        name: str,
        physical_table_map: Dict[str, Any],
        logical_table_map: Optional[Dict[str, Any]] = None,
        import_mode: str = "SPICE",
        column_groups: Optional[List[Dict]] = None,
        field_folders: Optional[Dict] = None,
        row_level_security: Optional[Dict] = None,
        column_level_security: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Update an existing dataset"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSetId': dataset_id,
                'Name': name,
                'PhysicalTableMap': physical_table_map,
                'ImportMode': import_mode
            }
            
            if logical_table_map:
                params['LogicalTableMap'] = logical_table_map
            if column_groups:
                params['ColumnGroups'] = column_groups
            if field_folders:
                params['FieldFolders'] = field_folders
            if row_level_security:
                params['RowLevelPermissionDataSet'] = row_level_security
            if column_level_security:
                params['ColumnLevelPermissionRules'] = column_level_security
            
            response = self.client.update_data_set(**params)
            logger.info(f"Updated dataset: {dataset_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating dataset {dataset_id}: {str(e)}")
            raise
    
    def update_permissions(
        self,
        dataset_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Update dataset permissions"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSetId': dataset_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = self.client.update_data_set_permissions(**params)
            logger.info(f"Updated permissions for dataset: {dataset_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating dataset permissions {dataset_id}: {str(e)}")
            raise

    def delete_dataset(self, dataset_id: str) -> Dict[str, Any]:
        """Delete a dataset"""
        try:
            response = self.client.delete_data_set(
                AwsAccountId=self.account_id,
                DataSetId=dataset_id
            )
            logger.info(f"Deleted dataset: {dataset_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting dataset {dataset_id}: {str(e)}")
            raise

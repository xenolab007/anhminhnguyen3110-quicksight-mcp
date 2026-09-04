"""Data source service for QuickSight data source operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class DatasourceService:
    """Service for managing QuickSight data sources"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize datasource service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_datasources(self) -> List[Dict[str, Any]]:
        """List all data sources in the account"""
        try:
            datasources = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_data_sources(**params)
                datasources.extend(response.get('DataSources', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasources)} data sources")
            return datasources
            
        except Exception as e:
            logger.error(f"Error listing data sources: {str(e)}")
            raise
    
    def describe_datasource(self, datasource_id: str) -> Dict[str, Any]:
        """Get detailed information about a data source"""
        try:
            response = self.client.describe_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=datasource_id
            )
            return response.get('DataSource', {})
            
        except Exception as e:
            logger.error(f"Error describing data source {datasource_id}: {str(e)}")
            raise
    
    def create_datasource(
        self,
        datasource_id: str,
        name: str,
        type: str,
        data_source_parameters: Dict[str, Any],
        credentials: Optional[Dict] = None,
        vpc_connection_properties: Optional[Dict] = None,
        ssl_properties: Optional[Dict] = None,
        permissions: Optional[List[Dict]] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create a new data source"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSourceId': datasource_id,
                'Name': name,
                'Type': type,
                'DataSourceParameters': data_source_parameters
            }
            
            if credentials:
                params['Credentials'] = credentials
            if vpc_connection_properties:
                params['VpcConnectionProperties'] = vpc_connection_properties
            if ssl_properties:
                params['SslProperties'] = ssl_properties
            if permissions:
                params['Permissions'] = permissions
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_data_source(**params)
            logger.info(f"Created data source: {datasource_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating data source {datasource_id}: {str(e)}")
            raise
    
    def update_datasource(
        self,
        datasource_id: str,
        name: str,
        data_source_parameters: Optional[Dict[str, Any]] = None,
        credentials: Optional[Dict] = None,
        vpc_connection_properties: Optional[Dict] = None,
        ssl_properties: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Update an existing data source"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSourceId': datasource_id,
                'Name': name
            }
            
            if data_source_parameters:
                params['DataSourceParameters'] = data_source_parameters
            if credentials:
                params['Credentials'] = credentials
            if vpc_connection_properties:
                params['VpcConnectionProperties'] = vpc_connection_properties
            if ssl_properties:
                params['SslProperties'] = ssl_properties
            
            response = self.client.update_data_source(**params)
            logger.info(f"Updated data source: {datasource_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating data source {datasource_id}: {str(e)}")
            raise
    
    def update_permissions(
        self,
        datasource_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Update data source permissions"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DataSourceId': datasource_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = self.client.update_data_source_permissions(**params)
            logger.info(f"Updated permissions for data source: {datasource_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating data source permissions {datasource_id}: {str(e)}")
            raise

    def delete_datasource(self, datasource_id: str) -> Dict[str, Any]:
        """Delete a data source"""
        try:
            response = self.client.delete_data_source(
                AwsAccountId=self.account_id,
                DataSourceId=datasource_id
            )
            logger.info(f"Deleted data source: {datasource_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting data source {datasource_id}: {str(e)}")
            raise

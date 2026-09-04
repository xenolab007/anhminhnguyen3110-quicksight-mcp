"""Dashboard service for QuickSight dashboard operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class DashboardService:
    """Service for managing QuickSight dashboards"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize dashboard service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards in the account"""
        try:
            dashboards = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_dashboards(**params)
                dashboards.extend(response.get('DashboardSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(dashboards)} dashboards")
            return dashboards
            
        except Exception as e:
            logger.error(f"Error listing dashboards: {str(e)}")
            raise
    
    def describe_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """Get detailed information about a dashboard"""
        try:
            response = self.client.describe_dashboard(
                AwsAccountId=self.account_id,
                DashboardId=dashboard_id
            )
            return response.get('Dashboard', {})
            
        except Exception as e:
            logger.error(f"Error describing dashboard {dashboard_id}: {str(e)}")
            raise
    
    def create_dashboard(
        self,
        dashboard_id: str,
        name: str,
        source_entity: Dict[str, Any],
        permissions: Optional[List[Dict]] = None,
        version_description: Optional[str] = None,
        dashboard_publish_options: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create a new dashboard"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DashboardId': dashboard_id,
                'Name': name,
                'SourceEntity': source_entity
            }
            
            if permissions:
                params['Permissions'] = permissions
            if version_description:
                params['VersionDescription'] = version_description
            if dashboard_publish_options:
                params['DashboardPublishOptions'] = dashboard_publish_options
            if theme_arn:
                params['ThemeArn'] = theme_arn
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_dashboard(**params)
            logger.info(f"Created dashboard: {dashboard_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating dashboard {dashboard_id}: {str(e)}")
            raise
    
    def update_dashboard(
        self,
        dashboard_id: str,
        name: str,
        source_entity: Dict[str, Any],
        version_description: Optional[str] = None,
        dashboard_publish_options: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing dashboard"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DashboardId': dashboard_id,
                'Name': name,
                'SourceEntity': source_entity
            }
            
            if version_description:
                params['VersionDescription'] = version_description
            if dashboard_publish_options:
                params['DashboardPublishOptions'] = dashboard_publish_options
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            response = self.client.update_dashboard(**params)
            logger.info(f"Updated dashboard: {dashboard_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating dashboard {dashboard_id}: {str(e)}")
            raise
    
    def publish_version(self, dashboard_id: str, version_number: int) -> Dict[str, Any]:
        """Publish a specific dashboard version"""
        try:
            response = self.client.update_dashboard_published_version(
                AwsAccountId=self.account_id,
                DashboardId=dashboard_id,
                VersionNumber=version_number
            )
            logger.info(f"Published dashboard {dashboard_id} version {version_number}")
            return response
            
        except Exception as e:
            logger.error(f"Error publishing dashboard {dashboard_id}: {str(e)}")
            raise
    
    def describe_dashboard_definition(
        self,
        dashboard_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the definition of a dashboard"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DashboardId': dashboard_id
            }
            
            if version_number:
                params['VersionNumber'] = version_number
            if alias_name:
                params['AliasName'] = alias_name
            
            response = self.client.describe_dashboard_definition(**params)
            logger.info(f"Retrieved dashboard definition for {dashboard_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error describing dashboard definition {dashboard_id}: {str(e)}")
            raise
    
    def list_dashboard_versions(self, dashboard_id: str) -> List[Dict[str, Any]]:
        """List all versions of a dashboard"""
        try:
            versions = []
            next_token = None
            
            while True:
                params = {
                    'AwsAccountId': self.account_id,
                    'DashboardId': dashboard_id
                }
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_dashboard_versions(**params)
                versions.extend(response.get('DashboardVersionSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(versions)} versions for dashboard {dashboard_id}")
            return versions
            
        except Exception as e:
            logger.error(f"Error listing dashboard versions {dashboard_id}: {str(e)}")
            raise
    
    def update_dashboard_published_version(
        self,
        dashboard_id: str,
        version_number: int
    ) -> Dict[str, Any]:
        """Update the published version of a dashboard"""
        try:
            response = self.client.update_dashboard_published_version(
                AwsAccountId=self.account_id,
                DashboardId=dashboard_id,
                VersionNumber=version_number
            )
            logger.info(f"Published dashboard {dashboard_id} version {version_number}")
            return response
            
        except Exception as e:
            logger.error(f"Error publishing dashboard {dashboard_id}: {str(e)}")
            raise
    
    def update_permissions(
        self,
        dashboard_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None,
        grant_link_permissions: Optional[List[Dict]] = None,
        revoke_link_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Update dashboard permissions"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DashboardId': dashboard_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            if grant_link_permissions:
                params['GrantLinkPermissions'] = grant_link_permissions
            if revoke_link_permissions:
                params['RevokeLinkPermissions'] = revoke_link_permissions
            
            response = self.client.update_dashboard_permissions(**params)
            logger.info(f"Updated permissions for dashboard: {dashboard_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating dashboard permissions {dashboard_id}: {str(e)}")
            raise

    def delete_dashboard(
        self,
        dashboard_id: str,
        version_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """Delete a dashboard, or a single version of it"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'DashboardId': dashboard_id
            }

            if version_number:
                params['VersionNumber'] = version_number

            response = self.client.delete_dashboard(**params)
            logger.info(f"Deleted dashboard: {dashboard_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting dashboard {dashboard_id}: {str(e)}")
            raise

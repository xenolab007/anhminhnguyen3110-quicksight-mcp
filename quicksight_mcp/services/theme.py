"""Theme service for QuickSight theme operations"""

import logging
from typing import Dict, List, Any, Optional
from quicksight_mcp.models.theme import CreateThemeRequest, UpdateThemeRequest

logger = logging.getLogger(__name__)


class ThemeService:
    """Service for managing QuickSight themes"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize theme service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_themes(self) -> List[Dict[str, Any]]:
        """List all themes in the account"""
        try:
            themes = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_themes(**params)
                themes.extend(response.get('ThemeSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(themes)} themes")
            return themes
            
        except Exception as e:
            logger.error(f"Error listing themes: {str(e)}")
            raise
    
    def describe_theme(
        self, 
        theme_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a theme"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'ThemeId': theme_id
            }
            
            if version_number:
                params['VersionNumber'] = version_number
            if alias_name:
                params['AliasName'] = alias_name
            
            response = self.client.describe_theme(**params)
            return response.get('Theme', {})
            
        except Exception as e:
            logger.error(f"Error describing theme {theme_id}: {str(e)}")
            raise
    
    def create_theme(self, request: CreateThemeRequest) -> Dict[str, Any]:
        """Create a new theme"""
        try:
            params = request.to_api_params(self.account_id)
            response = self.client.create_theme(**params)
            logger.info(f"Created theme: {request.theme_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating theme {request.theme_id}: {str(e)}")
            raise
    
    def update_theme(self, request: UpdateThemeRequest) -> Dict[str, Any]:
        """Update an existing theme (creates new version)"""
        try:
            params = request.to_api_params(self.account_id)
            response = self.client.update_theme(**params)
            logger.info(f"Updated theme: {request.theme_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating theme {request.theme_id}: {str(e)}")
            raise

    def delete_theme(
        self,
        theme_id: str,
        version_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """Delete a theme, or a single version of it"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'ThemeId': theme_id
            }

            if version_number:
                params['VersionNumber'] = version_number

            response = self.client.delete_theme(**params)
            logger.info(f"Deleted theme: {theme_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting theme {theme_id}: {str(e)}")
            raise

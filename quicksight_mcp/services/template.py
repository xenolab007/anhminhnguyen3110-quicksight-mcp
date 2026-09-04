"""Template service for QuickSight template operations"""

import logging
from typing import Dict, List, Any, Optional
from quicksight_mcp.models.template import CreateTemplateRequest, UpdateTemplateRequest

logger = logging.getLogger(__name__)


class TemplateService:
    """Service for managing QuickSight templates"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize template service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """List all templates in the account"""
        try:
            templates = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_templates(**params)
                templates.extend(response.get('TemplateSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(templates)} templates")
            return templates
            
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            raise
    
    def describe_template(
        self, 
        template_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get detailed information about a template"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'TemplateId': template_id
            }
            
            if version_number:
                params['VersionNumber'] = version_number
            if alias_name:
                params['AliasName'] = alias_name
            
            response = self.client.describe_template(**params)
            return response.get('Template', {})
            
        except Exception as e:
            logger.error(f"Error describing template {template_id}: {str(e)}")
            raise
    
    def create_template(self, request: CreateTemplateRequest) -> Dict[str, Any]:
        """Create a new template"""
        try:
            params = request.to_api_params(self.account_id)
            response = self.client.create_template(**params)
            logger.info(f"Created template: {request.template_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating template {request.template_id}: {str(e)}")
            raise
    
    def update_template(self, request: UpdateTemplateRequest) -> Dict[str, Any]:
        """Update an existing template (creates new version)"""
        try:
            params = request.to_api_params(self.account_id)
            response = self.client.update_template(**params)
            logger.info(f"Updated template: {request.template_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating template {request.template_id}: {str(e)}")
            raise
    
    def describe_template_definition(
        self,
        template_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the definition of a template"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'TemplateId': template_id
            }
            
            if version_number:
                params['VersionNumber'] = version_number
            if alias_name:
                params['AliasName'] = alias_name
            
            response = self.client.describe_template_definition(**params)
            logger.info(f"Retrieved template definition for {template_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error describing template definition {template_id}: {str(e)}")
            raise

    def delete_template(
        self,
        template_id: str,
        version_number: Optional[int] = None
    ) -> Dict[str, Any]:
        """Delete a template, or a single version of it"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'TemplateId': template_id
            }

            if version_number:
                params['VersionNumber'] = version_number

            response = self.client.delete_template(**params)
            logger.info(f"Deleted template: {template_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting template {template_id}: {str(e)}")
            raise

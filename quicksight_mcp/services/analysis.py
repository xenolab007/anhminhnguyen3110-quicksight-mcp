"""Analysis service for QuickSight analysis operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for managing QuickSight analyses"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize analysis service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def list_analyses(self) -> List[Dict[str, Any]]:
        """List all analyses in the account"""
        try:
            analyses = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.list_analyses(**params)
                analyses.extend(response.get('AnalysisSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(analyses)} analyses")
            return analyses
            
        except Exception as e:
            logger.error(f"Error listing analyses: {str(e)}")
            raise
    
    def describe_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Get detailed information about an analysis"""
        try:
            response = self.client.describe_analysis(
                AwsAccountId=self.account_id,
                AnalysisId=analysis_id
            )
            return response.get('Analysis', {})
            
        except Exception as e:
            logger.error(f"Error describing analysis {analysis_id}: {str(e)}")
            raise
    
    def describe_analysis_definition(
        self,
        analysis_id: str
    ) -> Dict[str, Any]:
        """Get the definition of an analysis"""
        try:
            response = self.client.describe_analysis_definition(
                AwsAccountId=self.account_id,
                AnalysisId=analysis_id
            )
            logger.info(f"Retrieved analysis definition for {analysis_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error describing analysis definition {analysis_id}: {str(e)}")
            raise
    
    def create_analysis(
        self,
        analysis_id: str,
        name: str,
        definition: Optional[Dict[str, Any]] = None,
        source_entity: Optional[Dict[str, Any]] = None,
        permissions: Optional[List[Dict]] = None,
        theme_arn: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create a new analysis"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'AnalysisId': analysis_id,
                'Name': name
            }
            
            if definition:
                params['Definition'] = definition
            if source_entity:
                params['SourceEntity'] = source_entity
            if permissions:
                params['Permissions'] = permissions
            if theme_arn:
                params['ThemeArn'] = theme_arn
            if tags:
                params['Tags'] = tags
            
            response = self.client.create_analysis(**params)
            logger.info(f"Created analysis: {analysis_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error creating analysis {analysis_id}: {str(e)}")
            raise
    
    def update_analysis(
        self,
        analysis_id: str,
        name: str,
        definition: Optional[Dict[str, Any]] = None,
        source_entity: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update an existing analysis"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'AnalysisId': analysis_id,
                'Name': name
            }
            
            if definition:
                params['Definition'] = definition
            if source_entity:
                params['SourceEntity'] = source_entity
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            response = self.client.update_analysis(**params)
            logger.info(f"Updated analysis: {analysis_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating analysis {analysis_id}: {str(e)}")
            raise
    
    def update_permissions(
        self,
        analysis_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Update analysis permissions"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'AnalysisId': analysis_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = self.client.update_analysis_permissions(**params)
            logger.info(f"Updated permissions for analysis: {analysis_id}")
            return response
            
        except Exception as e:
            logger.error(f"Error updating analysis permissions {analysis_id}: {str(e)}")
            raise

    def delete_analysis(
        self,
        analysis_id: str,
        recovery_window_in_days: Optional[int] = 30,
        force_delete_without_recovery: bool = False
    ) -> Dict[str, Any]:
        """Delete an analysis, optionally skipping the recovery window"""
        try:
            params = {
                'AwsAccountId': self.account_id,
                'AnalysisId': analysis_id
            }

            # The two options are mutually exclusive in the QuickSight API
            if force_delete_without_recovery:
                params['ForceDeleteWithoutRecovery'] = True
            elif recovery_window_in_days:
                params['RecoveryWindowInDays'] = recovery_window_in_days

            response = self.client.delete_analysis(**params)
            logger.info(f"Deleted analysis: {analysis_id}")
            return response

        except Exception as e:
            logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
            raise

    def restore_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Restore an analysis that is still inside its recovery window"""
        try:
            response = self.client.restore_analysis(
                AwsAccountId=self.account_id,
                AnalysisId=analysis_id
            )
            logger.info(f"Restored analysis: {analysis_id}")
            return response

        except Exception as e:
            logger.error(f"Error restoring analysis {analysis_id}: {str(e)}")
            raise

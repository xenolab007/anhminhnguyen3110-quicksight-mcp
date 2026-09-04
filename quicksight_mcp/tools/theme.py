"""Theme management tools for QuickSight"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.theme import ThemeService
from quicksight_mcp.models.tool_models import (
    ListThemesRequest, ListThemesResponse,
    DescribeThemeRequest, DescribeThemeResponse,
    CreateThemeRequest as ThemeToolRequest, CreateThemeResponse as ThemeToolResponse,
    UpdateThemeRequest as ThemeToolUpdateRequest, UpdateThemeResponse as ThemeToolUpdateResponse,
    PaginationInfo, ErrorInfo,
    DeleteThemeRequest, DeleteThemeResponse,
)
from quicksight_mcp.models.theme import (
    CreateThemeRequest,
    UpdateThemeRequest,
    ThemeConfiguration
)

logger = logging.getLogger(__name__)


def register_theme_tools(mcp):
    """Register all theme management tools with the MCP server"""
    
    @mcp.tool(
        name="list_themes",
        description="List all themes in the QuickSight account"
    )
    async def list_themes(request: ListThemesRequest) -> ListThemesResponse:
        """List all themes with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = ThemeService(quicksight, config.aws_account_id)
            all_themes = service.list_themes()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_themes[start_idx:end_idx]
            
            # Format themes
            formatted_themes = [
                {'ThemeId': t['ThemeId'], 'Name': t.get('Name', t['ThemeId'])}
                for t in paginated
            ]
            
            return ListThemesResponse(
                themes=formatted_themes,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_themes),
                    has_more=end_idx < len(all_themes),
                    next_offset=end_idx if end_idx < len(all_themes) else None
                ),
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error listing themes: {str(e)}")
            return ListThemesResponse(
                themes=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_theme",
        description="Get detailed information about a specific theme"
    )
    async def describe_theme(request: DescribeThemeRequest) -> DescribeThemeResponse:
        """
        Get theme details including colors and typography
        
        Args:
            request: Request with theme_id, version_number, and alias_name
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = ThemeService(quicksight, config.aws_account_id)
            theme = service.describe_theme(
                request.theme_id,
                request.version_number,
                request.alias_name
            )
            return DescribeThemeResponse(
                theme=theme,
                status="SUCCESS"
            )
        except Exception as e:
            logger.error(f"Error describing theme {request.theme_id}: {str(e)}")
            return DescribeThemeResponse(
                theme={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_theme",
        description="Create a new QuickSight theme"
    )
    async def create_theme(request: ThemeToolRequest) -> ThemeToolResponse:
        """
        Create a new custom theme
        
        Args:
            request: ThemeToolRequest with all theme configuration
            
        Returns:
            ThemeToolResponse with creation status and theme ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = ThemeService(quicksight, config.aws_account_id)
            
            # Convert configuration dict to model if it's a dict
            config_model = ThemeConfiguration(
                data_color_palette=request.configuration.get('DataColorPalette') if isinstance(request.configuration, dict) else None,
                ui_color_palette=request.configuration.get('UIColorPalette') if isinstance(request.configuration, dict) else None,
                sheet=request.configuration.get('Sheet') if isinstance(request.configuration, dict) else None,
                typography=request.configuration.get('Typography') if isinstance(request.configuration, dict) else None
            ) if isinstance(request.configuration, dict) else request.configuration
            
            theme_request = CreateThemeRequest(
                theme_id=request.theme_id,
                name=request.name,
                base_theme_id=request.base_theme_id,
                configuration=config_model,
                permissions=request.permissions,
                version_description=request.version_description,
                tags=request.tags
            )
            
            response = service.create_theme(theme_request)
            
            logger.info(f"Created theme: {request.theme_id}")
            
            return ThemeToolResponse(
                arn=response.get('Arn', ''),
                theme_id=response.get('ThemeId', request.theme_id),
                version_arn=response.get('VersionArn', ''),
                creation_status=response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating theme {request.theme_id}: {str(e)}")
            return ThemeToolResponse(
                arn="",
                theme_id=request.theme_id,
                version_arn="",
                creation_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_theme",
        description="Update an existing QuickSight theme"
    )
    async def update_theme(request: ThemeToolUpdateRequest) -> ThemeToolUpdateResponse:
        """
        Update an existing theme (creates new version)
        
        Args:
            request: ThemeToolUpdateRequest with updated configuration
            
        Returns:
            ThemeToolUpdateResponse with update status and version number
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = ThemeService(quicksight, config.aws_account_id)
            
            # Convert configuration dict to model if provided
            config_model = None
            if request.configuration:
                config_model = ThemeConfiguration(
                    data_color_palette=request.configuration.get('DataColorPalette') if isinstance(request.configuration, dict) else None,
                    ui_color_palette=request.configuration.get('UIColorPalette') if isinstance(request.configuration, dict) else None,
                    sheet=request.configuration.get('Sheet') if isinstance(request.configuration, dict) else None,
                    typography=request.configuration.get('Typography') if isinstance(request.configuration, dict) else None
                ) if isinstance(request.configuration, dict) else request.configuration
            
            theme_request = UpdateThemeRequest(
                theme_id=request.theme_id,
                base_theme_id=request.base_theme_id,
                configuration=config_model,
                name=request.name,
                version_description=request.version_description
            )
            
            response = service.update_theme(theme_request)
            
            logger.info(f"Updated theme: {request.theme_id}")
            
            return ThemeToolUpdateResponse(
                arn=response.get('Arn', ''),
                theme_id=response.get('ThemeId', request.theme_id),
                version_arn=response.get('VersionArn', ''),
                update_status=response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating theme {request.theme_id}: {str(e)}")
            return ThemeToolUpdateResponse(
                arn="",
                theme_id=request.theme_id,
                version_arn="",
                update_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="delete_theme",
        description=(
            "Permanently delete a theme. Pass version_number to delete only that one "
            "version instead of the whole theme. This cannot be undone."
        )
    )
    async def delete_theme(request: DeleteThemeRequest) -> DeleteThemeResponse:
        """Delete a theme or one of its versions"""
        config = mcp.config
        quicksight = mcp.quicksight

        try:
            service = ThemeService(quicksight, config.aws_account_id)
            response = service.delete_theme(
                theme_id=request.theme_id,
                version_number=request.version_number
            )

            return DeleteThemeResponse(
                theme_id=response.get('ThemeId', request.theme_id),
                arn=response.get('Arn', ''),
                status="SUCCESS"
            )

        except Exception as e:
            logger.error(f"Error deleting theme: {str(e)}")
            return DeleteThemeResponse(
                theme_id=request.theme_id,
                arn="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
